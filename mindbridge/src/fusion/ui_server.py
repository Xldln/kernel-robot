from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from collections import deque
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
import signal
import shutil
import subprocess
import threading
import time
from typing import Any
from urllib.parse import urlparse
from urllib.request import Request, urlopen

try:
    import zmq
except ImportError:  # pragma: no cover
    zmq = None


class FusionUiState:
    def __init__(self, *, retention_sec: float = 15.0, event_limit: int = 200) -> None:
        self.retention_sec = retention_sec
        self.video_streams: dict[str, dict[str, Any]] = {}
        self.events: deque[dict[str, Any]] = deque(maxlen=event_limit)
        self.lock = threading.RLock()

    def add_video_frame(self, payload: dict[str, Any]) -> None:
        now = time.time()
        title = str(payload.get("title") or "MindBridge Camera")
        item = {
            "title": title,
            "frame_base64": payload.get("frame_base64", ""),
            "mime_type": payload.get("mime_type") or "image/jpeg",
            "source": payload.get("source") or "MindBridge",
            "metadata": payload.get("metadata") or {},
            "timestamp": now,
        }
        with self.lock:
            self.video_streams[title] = item
            self._prune_locked(now)

    def add_event(self, topic: str, payload: Any) -> None:
        with self.lock:
            self.events.appendleft(
                {
                    "topic": topic,
                    "payload": payload,
                    "timestamp": time.time(),
                }
            )

    def snapshot(self) -> dict[str, Any]:
        now = time.time()
        with self.lock:
            self._prune_locked(now)
            return {
                "video_streams": list(self.video_streams.values()),
                "events": list(self.events),
                "server_time": now,
            }

    def _prune_locked(self, now: float) -> None:
        stale = [
            title
            for title, item in self.video_streams.items()
            if now - float(item.get("timestamp", 0.0)) > self.retention_sec
        ]
        for title in stale:
            self.video_streams.pop(title, None)


class FusionPipelineController:
    def __init__(
        self,
        *,
        ui_url: str,
        root_dir: str = "/workspace",
        service_controller: Any = None,
    ) -> None:
        self.ui_url = ui_url.rstrip("/")
        self.root_dir = root_dir
        self.service_controller = service_controller
        self.proc: subprocess.Popen | None = None
        self.mode = ""
        self.camera_mode = "single"
        self.started_at = 0.0
        self.lock = threading.RLock()

    def start(self, detector: str, camera_mode: str = "single") -> dict[str, Any]:
        detector = detector.lower()
        camera_mode = self._normalize_camera_mode(camera_mode)
        if detector not in {"sam3", "yolo"}:
            raise ValueError("detector must be sam3 or yolo")
        main_args = (
            f"--detector {detector} --pipeline full --show --fusion-pub --camera-mode {camera_mode} "
            "--fastfoundation-interval 3 --flowpose-interval 3 --siglip-interval 1 --fusion-ui-interval 3 "
            f"--fusion-ui-url {self.ui_url}"
        )
        return self._start_run(
            mode=f"{detector}-full",
            camera_mode=camera_mode,
            services=["realsense", "fastfoundation", detector, "flowpose", "siglip"],
            main_args=main_args,
        )

    def start_mode(self, mode: str, camera_mode: str = "single") -> dict[str, Any]:
        mode = mode.lower()
        camera_mode = self._normalize_camera_mode(camera_mode)
        modes = {
            "yolo-only": {
                "services": ["realsense", "yolo"],
                "main_args": f"--mode yolo-only --detector yolo --pipeline basic --show --fusion-pub --camera-mode {camera_mode} --fusion-ui-interval 3 --fusion-ui-url {self.ui_url}",
            },
            "sam3-only": {
                "services": ["realsense", "sam3"],
                "main_args": f"--mode sam3-only --detector sam3 --pipeline basic --show --fusion-pub --camera-mode {camera_mode} --fusion-ui-interval 3 --fusion-ui-url {self.ui_url}",
            },
            "siglip-only": {
                "services": ["realsense", "siglip"],
                "main_args": f"--mode siglip-only --pipeline basic --show --fusion-pub --camera-mode {camera_mode} --fusion-ui-interval 3 --fusion-ui-url {self.ui_url}",
            },
            "flowpose-only": {
                "services": ["realsense", "fastfoundation", "flowpose"],
                "main_args": f"--mode flowpose-only --pipeline full --show --fusion-pub --camera-mode {camera_mode} --fusion-ui-interval 3 --fusion-ui-url {self.ui_url}",
            },
        }
        if mode not in modes:
            raise ValueError("mode must be yolo-only, sam3-only, siglip-only, or flowpose-only")
        spec = modes[mode]
        return self._start_run(
            mode=mode,
            camera_mode=camera_mode,
            services=spec["services"],
            main_args=spec["main_args"],
        )

    def _start_run(self, *, mode: str, camera_mode: str, services: list[str], main_args: str) -> dict[str, Any]:
        with self.lock:
            self._reap_locked()
            if self.proc and self.proc.poll() is None:
                if self.mode == mode and self.camera_mode == camera_mode:
                    return self.status()
                self._stop_proc_locked()

            if self.service_controller:
                self.service_controller.start_group(services, camera_mode=camera_mode)
                service_cmd = "true"
            else:
                group = self._service_group(services)
                if group:
                    service_cmd = f"REALSENSE_MODE={camera_mode} bash {self.root_dir}/scripts/start_service.sh {group}"
                else:
                    service_cmd = " && ".join(
                        f"REALSENSE_MODE={camera_mode} bash {self.root_dir}/scripts/start_service.sh {name}"
                        for name in services
                    )
            cmd = (
                f"{service_cmd} && "
                "source $(conda info --base)/etc/profile.d/conda.sh && "
                "conda activate base && "
                "exec python -m mindbridge.src.main "
                f"{main_args}"
            )
            self.proc = subprocess.Popen(
                ["bash", "-lc", cmd],
                cwd=self.root_dir,
                start_new_session=True,
            )
            self.mode = mode
            self.camera_mode = camera_mode
            self.started_at = time.time()
            return self.status()

    @staticmethod
    def _service_group(services: list[str]) -> str:
        names = set(services)
        if names == {"realsense", "fastfoundation", "yolo", "flowpose", "siglip"}:
            return "yolo-full"
        if names == {"realsense", "fastfoundation", "sam3", "flowpose", "siglip"}:
            return "sam3-full"
        if names == {"realsense", "yolo", "siglip"}:
            return "basic-yolo"
        if names == {"realsense", "sam3", "siglip"}:
            return "basic-sam3"
        if names == {"realsense", "fastfoundation", "flowpose"}:
            return "flowpose-stack"
        return " ".join(services)

    def stop(self) -> dict[str, Any]:
        with self.lock:
            self._stop_proc_locked()
            self.proc = None
            self.mode = ""
            self.camera_mode = "single"
            self.started_at = 0.0
            return self.status()

    def status(self) -> dict[str, Any]:
        with self.lock:
            self._reap_locked()
            running = bool(self.proc and self.proc.poll() is None)
            return {
                "enabled": True,
                "running": running,
                "mode": self.mode if running else "",
                "camera_mode": self.camera_mode if running else "single",
                "pid": self.proc.pid if running and self.proc else None,
                "started_at": self.started_at if running else 0.0,
            }

    @staticmethod
    def _normalize_camera_mode(camera_mode: str) -> str:
        value = (camera_mode or "single").lower()
        if value not in {"single", "multi"}:
            raise ValueError("camera_mode must be single or multi")
        return value

    def _reap_locked(self) -> None:
        if self.proc and self.proc.poll() is not None:
            self.proc = None
            self.mode = ""
            self.camera_mode = "single"
            self.started_at = 0.0

    def _stop_proc_locked(self) -> None:
        if self.proc and self.proc.poll() is None:
            os.killpg(self.proc.pid, signal.SIGTERM)
            try:
                self.proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                os.killpg(self.proc.pid, signal.SIGKILL)
                self.proc.wait(timeout=5)
        self.proc = None
        self.mode = ""
        self.camera_mode = "single"
        self.started_at = 0.0


SERVICE_SPECS = [
    {"name": "realsense", "label": "RealSense", "port": 8000, "env": "realsense", "script": "mindbridge/src/core/launch/service_RealSense.py"},
    {"name": "yolo", "label": "YOLO", "port": 8001, "env": "yolo", "script": "mindbridge/src/core/launch/service_InsenceSeg.py"},
    {"name": "siglip", "label": "SigLIP", "port": 8002, "env": "siglip", "script": "mindbridge/src/core/launch/service_Siglip.py"},
    {"name": "fastfoundation", "label": "FastFoundation", "port": 8004, "env": "fastfoundation", "script": "mindbridge/src/core/launch/service_FastFoundation.py"},
    {"name": "sam3", "label": "SAM3", "port": 8005, "env": "sam3", "script": "mindbridge/src/core/launch/service_Sam3.py"},
    {"name": "flowpose", "label": "FlowPose", "port": 8006, "env": "flowpose", "script": "mindbridge/src/core/launch/service_FlowPose.py"},
]


class ServiceController:
    def __init__(self, *, root_dir: str = "/workspace", pid_dir: str = "/tmp/mindbridge") -> None:
        self.root_dir = root_dir
        self.pid_dir = pid_dir
        self.specs = {str(item["name"]): item for item in SERVICE_SPECS}
        self.lock = threading.RLock()

    def list_status(self) -> list[dict[str, Any]]:
        names = list(self.specs)
        with ThreadPoolExecutor(max_workers=max(1, len(names))) as pool:
            return list(pool.map(self.status, names))

    def start(self, name: str, camera_mode: str = "single") -> dict[str, Any]:
        self._require_name(name)
        with self.lock:
            env = os.environ.copy()
            if name == "realsense" and camera_mode in {"single", "multi"}:
                env["REALSENSE_MODE"] = camera_mode
            subprocess.Popen(
                ["bash", f"{self.root_dir}/scripts/start_service.sh", name],
                cwd=self.root_dir,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True,
                env=env,
            )
            return self.status(name)

    def start_group(self, services: list[str], camera_mode: str = "single") -> list[dict[str, Any]]:
        if "realsense" in services and camera_mode in {"single", "multi"}:
            current = self.status("realsense")
            current_mode = current.get("health", {}).get("mode")
            if current.get("running") and current_mode != camera_mode:
                self.stop("realsense")

        group = self._service_group(services)
        if group:
            with self.lock:
                subprocess.run(
                    ["bash", f"{self.root_dir}/scripts/start_service.sh", group],
                    cwd=self.root_dir,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    env={**os.environ, "REALSENSE_MODE": camera_mode},
                    check=False,
                )
            return [self.status(name) for name in services]

        return [self.start(name, camera_mode=camera_mode) for name in services]

    def wait_ready(self, services: list[str], *, timeout: float = 60.0) -> list[dict[str, Any]]:
        deadline = time.time() + timeout
        statuses = [self.status(name) for name in services]
        while any(not item.get("running") for item in statuses) and time.time() < deadline:
            if any(
                item.get("name") == "realsense"
                and item.get("health", {}).get("status") == "engine_missing"
                for item in statuses
            ):
                break
            time.sleep(1.0)
            statuses = [self.status(name) for name in services]
        return statuses

    def stop(self, name: str) -> dict[str, Any]:
        self._require_name(name)
        with self.lock:
            if name == "realsense":
                self._post_service(8000, "/realsense/shutdown", timeout=1.0)
                time.sleep(0.5)
            pid = self._read_pid(name)
            if pid and self._pid_alive(pid):
                try:
                    os.kill(pid, signal.SIGTERM)
                except ProcessLookupError:
                    pass
                deadline = time.time() + 5
                while time.time() < deadline and self._pid_alive(pid):
                    time.sleep(0.1)
                if self._pid_alive(pid):
                    try:
                        os.kill(pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
            self._pid_path(name).unlink(missing_ok=True)
            return self.status(name)

    def restart(self, name: str) -> dict[str, Any]:
        self.stop(name)
        return self.start(name)

    def restart_with_mode(self, name: str, camera_mode: str = "single") -> dict[str, Any]:
        self.stop(name)
        return self.start(name, camera_mode=camera_mode)

    def enable_flowpose_visualization(self) -> dict[str, Any]:
        deadline = time.time() + 15
        current = self.status("flowpose")
        while not current.get("running") and time.time() < deadline:
            time.sleep(0.5)
            current = self.status("flowpose")
        if not current.get("running"):
            return {"status": "pending", "message": "flowpose is still starting"}

        result = self._set_flowpose_visualization(True)
        if result.get("status") == "ok":
            return result

        # Older running FlowPose services do not expose the visualization API.
        # Restart once so new code is loaded and the config default is restored.
        self.restart("flowpose")
        return result

    def status(self, name: str) -> dict[str, Any]:
        spec = self._require_name(name)
        pid = self._read_pid(name)
        pid_alive = bool(pid and self._pid_alive(pid))
        health = self._health(int(spec["port"]))
        running = health.get("status") == "ok"
        stale = bool(pid and not pid_alive)
        if stale:
            self._pid_path(name).unlink(missing_ok=True)
        return {
            "name": spec["name"],
            "label": spec["label"],
            "port": spec["port"],
            "pid": pid if pid_alive else None,
            "running": running,
            "process_running": pid_alive,
            "health": health,
            "stale_pid": stale,
            "log": f"logs/{name}.log",
        }

    @staticmethod
    def _service_group(services: list[str]) -> str:
        names = set(services)
        if names == {"realsense", "fastfoundation", "yolo", "flowpose", "siglip"}:
            return "yolo-full"
        if names == {"realsense", "fastfoundation", "sam3", "flowpose", "siglip"}:
            return "sam3-full"
        if names == {"realsense", "yolo", "siglip"}:
            return "basic-yolo"
        if names == {"realsense", "sam3", "siglip"}:
            return "basic-sam3"
        if names == {"realsense", "fastfoundation", "flowpose"}:
            return "flowpose-stack"
        return ""

    def _health(self, port: int) -> dict[str, Any]:
        try:
            with urlopen(f"http://127.0.0.1:{port}/health", timeout=0.25) as response:
                payload = json.loads(response.read().decode("utf-8"))
            if not isinstance(payload, dict):
                payload = {"status": "ok", "raw": payload}
            if port == 8000 and payload.get("status") == "ok":
                try:
                    with urlopen("http://127.0.0.1:8000/realsense/info", timeout=0.25) as response:
                        info = json.loads(response.read().decode("utf-8"))
                    if isinstance(info, dict):
                        payload["mode"] = info.get("mode", "single")
                        payload["cameras"] = info.get("cameras", [])
                except Exception as exc:
                    return {"status": "engine_missing", "error": str(exc)}
            return payload
        except Exception as exc:
            return {"status": "unreachable", "error": str(exc)}

    def _set_flowpose_visualization(self, enabled: bool) -> dict[str, Any]:
        value = "true" if enabled else "false"
        try:
            req = Request(
                f"http://127.0.0.1:8006/infer/visualization?enabled={value}",
                data=b"",
                method="POST",
            )
            with urlopen(req, timeout=0.5) as response:
                payload = json.loads(response.read().decode("utf-8"))
            return payload if isinstance(payload, dict) else {"status": "ok", "raw": payload}
        except Exception as exc:
            return {"status": "error", "error": str(exc)}

    def _post_service(self, port: int, path: str, *, timeout: float = 0.5) -> dict[str, Any]:
        try:
            req = Request(f"http://127.0.0.1:{port}{path}", data=b"", method="POST")
            with urlopen(req, timeout=timeout) as response:
                raw = response.read().decode("utf-8")
            return json.loads(raw) if raw else {"status": "ok"}
        except Exception as exc:
            return {"status": "error", "error": str(exc)}

    def _read_pid(self, name: str) -> int | None:
        try:
            return int(self._pid_path(name).read_text().strip())
        except Exception:
            return None

    def _pid_alive(self, pid: int) -> bool:
        try:
            os.kill(pid, 0)
            return True
        except OSError:
            return False

    def _pid_path(self, name: str):
        from pathlib import Path
        return Path(self.pid_dir) / f"{name}.pid"

    def _require_name(self, name: str) -> dict[str, Any]:
        key = name.lower()
        if key not in self.specs:
            raise ValueError(f"unknown service: {name}")
        return self.specs[key]


class MarvinDockerController:
    def __init__(self, *, root_dir: str = "/workspace", robot_ip: str = "192.168.12.190") -> None:
        self.root_dir = root_dir
        self.robot_ip = robot_ip
        self.script = os.path.join(root_dir, "MarvinDocker", "run.sh")
        self.last_message = ""
        self.lock = threading.RLock()

    def start_base(self, robot_ip: str | None = None) -> dict[str, Any]:
        return self._run("base", robot_ip)

    def run_action(self, robot_ip: str | None = None) -> dict[str, Any]:
        return self._run("action", robot_ip)

    def stop_action(self) -> dict[str, Any]:
        if not self._docker_available():
            return self.status()
        self._docker([
            "exec", "marvin_dev", "bash", "-lc",
            "tmux send-keys -t marvin:0.6 C-c 2>/dev/null || true; "
            "pkill -f 'python3 /robotaction/robot_action.py' 2>/dev/null || true",
        ])
        return self.status()

    def stop_base(self) -> dict[str, Any]:
        if not self._docker_available():
            return self.status()
        self._docker(["stop", "marvin_dev"])
        return self.status()

    def status(self) -> dict[str, Any]:
        if not os.path.exists(self.script):
            return {
                "enabled": False,
                "running": False,
                "tmux": False,
                "robot_action": False,
                "message": f"missing {self.script}",
            }
        if not self._docker_available():
            return {
                "enabled": True,
                "docker_ready": False,
                "running": False,
                "tmux": False,
                "robot_action": False,
                "robot_ip": self.robot_ip,
                "message": (
                    "Docker is unavailable in this UI container. Run the web UI from TJfusion "
                    "or create the UI container with docker socket and docker CLI mounted."
                ),
            }
        docker = self._docker(["ps", "--filter", "name=^/marvin_dev$", "--format", "{{.Names}}"])
        running = docker["ok"] and docker["stdout"].strip() == "marvin_dev"
        tmux = False
        robot_action = False
        if running:
            tmux_result = self._docker(["exec", "marvin_dev", "bash", "-lc", "tmux has-session -t marvin"])
            tmux = tmux_result["ok"]
            action_result = self._docker([
                "exec", "marvin_dev", "bash", "-lc",
                "ps -eo comm,args | awk '$1 ~ /^python/ && $0 ~ /\\/robotaction\\/robot_action.py/ {found=1} END {exit !found}'",
            ])
            robot_action = action_result["ok"]
        return {
            "enabled": True,
            "docker_ready": True,
            "running": running,
            "tmux": tmux,
            "robot_action": robot_action,
            "robot_ip": self.robot_ip,
            "message": docker["stderr"] if not docker["ok"] else self.last_message,
        }

    def _run(self, mode: str, robot_ip: str | None = None) -> dict[str, Any]:
        ip = (robot_ip or self.robot_ip).strip() or self.robot_ip
        try:
            with self.lock:
                if not os.path.exists(self.script):
                    raise FileNotFoundError(self.script)
                if not self._docker_available():
                    self.robot_ip = ip
                    return self.status()
                os.makedirs(os.path.join(self.root_dir, "logs"), exist_ok=True)
                env = os.environ.copy()
                if env.get("HOST_WORKSPACE_ROOT") and not env.get("MARVIN_HOST_ROOT_DIR"):
                    env["MARVIN_HOST_ROOT_DIR"] = os.path.join(env["HOST_WORKSPACE_ROOT"], "MarvinDocker")
                proc = subprocess.run(
                    ["bash", self.script, ip, mode, "--no-attach"],
                    cwd=self.root_dir,
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=20,
                    check=False,
                    env=env,
                )
                output = "\n".join(part.strip() for part in (proc.stdout, proc.stderr) if part.strip())
                log_path = os.path.join(self.root_dir, "logs", "marvin-start.log")
                with open(log_path, "a", encoding="utf-8") as f:
                    f.write(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] mode={mode} ip={ip} rc={proc.returncode}\n")
                    if output:
                        f.write(output)
                        f.write("\n")
                self.robot_ip = ip
                self.last_message = output.splitlines()[-1] if output else f"started {mode}"
                if proc.returncode != 0:
                    status = self.status()
                    status["message"] = self.last_message
                    return status
                time.sleep(0.5)
                status = self.status()
                if not status.get("message"):
                    status["message"] = self.last_message
                return status
        except subprocess.TimeoutExpired as exc:
            self.robot_ip = ip
            self.last_message = f"MarvinDocker start timed out; see logs/marvin-start.log"
            log_path = os.path.join(self.root_dir, "logs", "marvin-start.log")
            os.makedirs(os.path.dirname(log_path), exist_ok=True)
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] mode={mode} ip={ip} timeout\n")
                if exc.stdout:
                    f.write(str(exc.stdout))
                if exc.stderr:
                    f.write(str(exc.stderr))
            status = self.status()
            status["message"] = self.last_message
            return status

    def _docker_available(self) -> bool:
        return (
            os.path.exists("/var/run/docker.sock")
            and shutil.which("docker") is not None
        )

    def _docker(self, args: list[str]) -> dict[str, Any]:
        try:
            proc = subprocess.run(
                ["docker", *args],
                cwd=self.root_dir,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=2,
                check=False,
            )
            return {
                "ok": proc.returncode == 0,
                "stdout": proc.stdout,
                "stderr": proc.stderr.strip(),
            }
        except Exception as exc:
            return {"ok": False, "stdout": "", "stderr": str(exc)}


HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>MindBridge Fusion</title>
  <style>
    :root { color-scheme: dark; font-family: Arial, sans-serif; }
    body { margin: 0; background: #0f1216; color: #eef2f7; }
    header { padding: 14px 18px; background: #151a21; border-bottom: 1px solid #2c3340; display: grid; grid-template-columns: minmax(140px, 1fr) auto minmax(140px, 1fr); align-items: center; gap: 16px; }
    header strong { font-size: 15px; }
    .controls { display: flex; align-items: center; justify-content: flex-end; gap: 8px; flex-wrap: wrap; }
    .service-quickbar { display: flex; gap: 8px; flex-wrap: wrap; padding: 10px 12px; background: #151a21; border-bottom: 1px solid #2c3340; }
    button { background: #222b36; color: #eef2f7; border: 1px solid #3c4858; border-radius: 6px; padding: 7px 11px; cursor: pointer; font-weight: 600; line-height: 1.2; box-shadow: inset 0 1px 0 rgba(255,255,255,0.05); transition: background 120ms ease, border-color 120ms ease, transform 80ms ease; }
    button:hover { background: #2b3644; border-color: #596779; }
    button:active { transform: translateY(1px); }
    button[data-start] { background: #17382f; border-color: #2d6d5d; color: #bff7df; }
    button[data-start]:hover { background: #1d493d; border-color: #3b8a76; }
    button.danger { background: #4a2630; border-color: #7d4355; color: #ffd5dc; }
    button.danger:hover { background: #5a2d39; border-color: #9a5368; }
    button.small { padding: 5px 8px; font-size: 12px; }
    main { display: grid; grid-template-columns: minmax(320px, 2fr) minmax(320px, 1fr); gap: 16px; padding: 16px; }
    section { background: #171b22; border: 1px solid #2c3340; border-radius: 6px; overflow: hidden; }
    h2 { font-size: 15px; margin: 0; padding: 11px 12px; background: #1b2029; border-bottom: 1px solid #2c3340; }
    .stack { display: grid; gap: 16px; }
    .service-table { width: 100%; border-collapse: collapse; font-size: 13px; }
    .service-table th, .service-table td { padding: 9px 10px; border-bottom: 1px solid #2c3340; text-align: center; vertical-align: middle; }
	    .service-table th { background: #11161d; color: #b6c0cf; font-size: 12px; font-weight: 700; text-transform: uppercase; }
	    .service-table tbody tr:hover { background: #1d232d; }
	    .service-table th:last-child, .service-table td:last-child { text-align: left; }
	    .marvin-panel { display: grid; grid-template-columns: minmax(150px, 1fr) auto; gap: 10px; align-items: end; padding: 12px; }
	    .marvin-actions { display: flex; gap: 8px; flex-wrap: wrap; justify-content: flex-end; }
	    .marvin-steps { display: grid; grid-template-columns: repeat(2, minmax(190px, 1fr)); gap: 10px; padding: 0 12px 12px; }
	    .marvin-step { background: #10151b; border: 1px solid #2c3340; border-radius: 6px; padding: 10px; display: grid; gap: 8px; }
	    .marvin-step strong { font-size: 13px; }
	    .field { display: grid; gap: 5px; }
	    .field label { color: #b6c0cf; font-size: 12px; font-weight: 700; text-transform: uppercase; }
	    input { background: #0f1217; color: #eef2f7; border: 1px solid #3c4858; border-radius: 6px; padding: 7px 9px; min-width: 0; }
	    select { background: #0f1217; color: #eef2f7; border: 1px solid #3c4858; border-radius: 6px; padding: 7px 9px; font-weight: 700; }
	    .badge { display: inline-block; min-width: 74px; padding: 3px 7px; border-radius: 999px; text-align: center; font-size: 12px; border: 1px solid #3b4656; }
	    .badge.ok { color: #8cffbe; border-color: #2f7655; background: #143425; }
    .badge.warn { color: #ffd56d; border-color: #6f5d2a; background: #342b14; }
    .badge.bad { color: #ff98a4; border-color: #714050; background: #341923; }
    .actions { display: flex; justify-content: flex-start; gap: 6px; flex-wrap: wrap; }
    .meta { padding: 8px 10px; font-size: 12px; color: #b6c0cf; display: flex; justify-content: space-between; gap: 8px; }
    .events { max-height: calc(100vh - 120px); overflow: auto; padding: 8px; }
    .event { border-bottom: 1px solid #2a2f3a; padding: 8px 4px; font-size: 12px; }
    .topic { color: #7cc7ff; font-weight: 700; }
    pre { margin: 6px 0 0; white-space: pre-wrap; word-break: break-word; color: #d9e2ef; }
	    .muted { color: #8b96a8; font-size: 12px; }
	    #status { color: #d9e2ef; font-size: 16px; font-weight: 700; text-align: center; white-space: nowrap; }
	    #marvinStatus { padding: 0 12px 12px; }
	    @media (max-width: 900px) { main { grid-template-columns: 1fr; } .marvin-steps { grid-template-columns: 1fr; } }
	  </style>
</head>
<body>
  <header>
    <strong>MindBridge Fusion</strong>
    <span id="status" class="muted">connecting...</span>
    <div class="controls">
      <label class="muted" for="cameraMode">Camera</label>
      <select id="cameraMode">
        <option value="single">Single</option>
        <option value="multi">Multi</option>
      </select>
      <button data-start="sam3">SAM3 Full</button>
      <button data-start="yolo">YOLO Full</button>
      <button id="stop" class="danger">Stop</button>
    </div>
  </header>
	  <main>
	    <div class="stack">
	      <section>
	        <h2>MarvinDocker</h2>
	        <div class="marvin-panel">
	          <div class="field">
	            <label for="marvinIp">Robot IP</label>
	            <input id="marvinIp" value="192.168.12.190" autocomplete="off">
	          </div>
	          <div id="marvinDockerReady" class="muted">checking docker...</div>
	        </div>
	        <div class="marvin-steps">
	          <div class="marvin-step">
	            <strong>1. Start Base</strong>
	            <span class="muted">planner, gripper, service call, task manager, TF bridge, SigLIP bridge</span>
	            <button data-marvin="start">Start Base</button>
	          </div>
	          <div class="marvin-step">
	            <strong>2. Run Robot Action</strong>
	            <span class="muted">starts robot_action.py in the ROBOT_ACTION tmux pane</span>
	            <button data-marvin="run">Run Action</button>
	            <button class="danger" data-marvin="stop-action">Stop Action</button>
	          </div>
	        </div>
	        <div class="marvin-actions" style="padding: 0 12px 12px; justify-content: flex-start;">
	          <button class="danger" data-marvin="stop-base">Stop Base</button>
	        </div>
	        <div id="marvinStatus" class="muted">checking...</div>
	      </section>
	      <section>
	        <h2>Services</h2>
        <div class="service-quickbar">
          <button data-service-quick="realsense">RealSense</button>
          <button data-service-quick="yolo">YOLO</button>
          <button data-service-quick="sam3">SAM3</button>
          <button data-service-quick="siglip">SigLIP</button>
          <button data-service-quick="fastfoundation">FastFoundation</button>
          <button data-service-quick="flowpose">FlowPose</button>
        </div>
        <table class="service-table">
          <thead>
            <tr><th>Model</th><th>Port</th><th>Status</th><th>PID</th><th>Health</th><th>Actions</th></tr>
          </thead>
          <tbody id="services"></tbody>
        </table>
      </section>
    </div>
    <div class="stack">
      <section>
        <h2>ZMQ Events</h2>
        <div id="events" class="events"></div>
      </section>
    </div>
  </main>
  <script>
    const eventsEl = document.getElementById("events");
	    const servicesEl = document.getElementById("services");
	    const statusEl = document.getElementById("status");
	    const marvinStatusEl = document.getElementById("marvinStatus");
	    const marvinDockerReadyEl = document.getElementById("marvinDockerReady");
	    const marvinIpEl = document.getElementById("marvinIp");
	    const cameraModeEl = document.getElementById("cameraMode");
    const viewModes = {
      yolo: "yolo-only",
      sam3: "sam3-only",
      siglip: "siglip-only",
      flowpose: "flowpose-only"
    };
    async function postJson(url, payload) {
      const res = await fetch(url, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(payload || {})
      });
      if (!res.ok) {
        let message = await res.text();
        try {
          const payload = JSON.parse(message);
          message = payload.message || payload.error || message;
        } catch (_) {}
        throw new Error(message);
      }
      return await res.json();
    }
    for (const button of document.querySelectorAll("[data-start]")) {
      button.addEventListener("click", async () => {
        statusEl.textContent = "starting " + button.dataset.start + "...";
        try {
          await postJson("/api/control/start", {
            detector: button.dataset.start,
            camera_mode: cameraModeEl.value
          });
        }
        catch (err) { statusEl.textContent = err.message || "start failed"; }
      });
    }
    async function startMode(mode) {
      statusEl.textContent = "starting " + mode + "...";
      try {
        await postJson("/api/control/start", {mode, camera_mode: cameraModeEl.value});
        await refresh();
      } catch (err) {
        statusEl.textContent = err.message || "start failed";
      }
    }
	    document.getElementById("stop").addEventListener("click", async () => {
	      statusEl.textContent = "stopping...";
	      try { await postJson("/api/control/stop", {}); }
	      catch (err) { statusEl.textContent = "stop failed"; }
	    });
	    for (const button of document.querySelectorAll("[data-marvin]")) {
	      button.addEventListener("click", async () => {
	        const action = button.dataset.marvin;
	        const labels = {
	          start: "starting marvin base...",
	          run: "running robot action...",
	          "stop-action": "stopping robot action...",
	          "stop-base": "stopping marvin base..."
	        };
	        statusEl.textContent = labels[action] || "running marvin command...";
	        try {
	          const endpoints = {
	            start: "/api/marvin/start",
	            run: "/api/marvin/run",
	            "stop-action": "/api/marvin/stop-action",
	            "stop-base": "/api/marvin/stop-base"
	          };
	          const result = await postJson(endpoints[action], {
	            robot_ip: marvinIpEl.value
	          });
	          if (result.message) {
	            marvinStatusEl.textContent = result.message;
	          }
	          await refresh();
	        } catch (err) {
	          statusEl.textContent = "marvin command failed";
	          marvinStatusEl.textContent = err.message || "marvin command failed";
	        }
	      });
	    }
    async function serviceAction(name, action) {
      statusEl.textContent = `${action} ${name}...`;
      try {
        await postJson(`/api/services/${name}/${action}`, {camera_mode: cameraModeEl.value});
        await refresh();
      } catch (err) {
        statusEl.textContent = `${action} failed`;
      }
    }
    for (const button of document.querySelectorAll("[data-service-quick]")) {
      button.addEventListener("click", () => serviceAction(button.dataset.serviceQuick, "start"));
    }
    function fmtTime(ts) {
      if (!ts) return "-";
      return new Date(ts * 1000).toLocaleTimeString();
    }
    async function refresh() {
      try {
        const res = await fetch("/api/state", {cache: "no-store"});
        const data = await res.json();
	        const control = data.control || {};
	        const marvin = data.marvin || {};
	        const runningServices = (data.services || []).filter((service) => service.running).length;
	        const totalServices = (data.services || []).length;
	        const cameraText = control.camera_mode ? ` | camera ${control.camera_mode}` : "";
	        const runText = control.running
	          ? `pipeline running ${control.mode.toUpperCase()}${cameraText}`
	          : (runningServices > 0 ? `pipeline idle | services ${runningServices}/${totalServices} running` : "idle");
	        statusEl.textContent = `${runText} | updated ${fmtTime(data.server_time)}`;
	        if (control.running && control.camera_mode && document.activeElement !== cameraModeEl) {
	          cameraModeEl.value = control.camera_mode;
	        }
	        if (marvin.robot_ip && document.activeElement !== marvinIpEl) {
	          marvinIpEl.value = marvin.robot_ip;
	        }
	        marvinDockerReadyEl.textContent = marvin.docker_ready ? "docker ready" : "docker unavailable";
	        if (!marvin.enabled) {
	          marvinStatusEl.textContent = marvin.message || "MarvinDocker control unavailable";
	        } else {
	          const container = marvin.running ? "container running" : "container stopped";
	          const tmux = marvin.tmux ? "tmux ready" : "tmux not ready";
	          const action = marvin.robot_action ? "robot action running" : "robot action idle";
	          const message = marvin.message ? ` | ${marvin.message}` : "";
	          marvinStatusEl.textContent = `${container} | ${tmux} | ${action}${message}`;
	        }
	        servicesEl.innerHTML = "";
        for (const service of data.services || []) {
          const row = document.createElement("tr");
          const healthStatus = (service.health && service.health.status) || "unknown";
          const statusClass = service.running ? "ok" : (service.process_running ? "warn" : "bad");
          const statusText = service.running ? "running" : (service.process_running ? "booting" : "stopped");
          const healthClass = healthStatus === "ok" ? "ok" : (healthStatus === "unreachable" ? "bad" : "warn");
          const viewButton = viewModes[service.name]
            ? `<button class="small" data-view-mode="${viewModes[service.name]}">View</button>`
            : "";
          row.innerHTML = `
            <td>${service.label || service.name}</td>
            <td>${service.port || ""}</td>
            <td><span class="badge ${statusClass}">${statusText}</span></td>
            <td>${service.pid || "-"}</td>
            <td><span class="badge ${healthClass}">${healthStatus}</span></td>
            <td>
              <div class="actions">
                <button class="small" data-service="${service.name}" data-action="start">Start</button>
                <button class="small" data-service="${service.name}" data-action="restart">Restart</button>
                ${viewButton}
                <button class="small" data-service="${service.name}" data-action="refresh">Refresh</button>
                <button class="small danger" data-service="${service.name}" data-action="stop">Stop</button>
              </div>
            </td>`;
          servicesEl.appendChild(row);
        }
        for (const button of servicesEl.querySelectorAll("button[data-service]")) {
          button.addEventListener("click", () => serviceAction(button.dataset.service, button.dataset.action));
        }
        for (const button of servicesEl.querySelectorAll("button[data-view-mode]")) {
          button.addEventListener("click", () => startMode(button.dataset.viewMode));
        }
        eventsEl.innerHTML = "";
        for (const event of data.events || []) {
          const row = document.createElement("div");
          row.className = "event";
          const payload = JSON.stringify(event.payload, null, 2);
          row.innerHTML = `<div><span class="topic">${event.topic}</span> <span class="muted">${fmtTime(event.timestamp)}</span></div><pre></pre>`;
          row.querySelector("pre").textContent = payload;
          eventsEl.appendChild(row);
        }
      } catch (err) {
        statusEl.textContent = "offline";
      }
    }
    refresh();
    setInterval(refresh, 500);
  </script>
</body>
</html>
"""


def make_handler(
    state: FusionUiState,
    controller: FusionPipelineController | None = None,
    service_controller: ServiceController | None = None,
    marvin_controller: MarvinDockerController | None = None,
) -> type[BaseHTTPRequestHandler]:
    class FusionUiHandler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            path = urlparse(self.path).path
            if path == "/":
                self._send_bytes(HTML.encode("utf-8"), "text/html; charset=utf-8")
                return
            if path in {"/api/state", "/api/video-streams", "/api/events"}:
                payload = state.snapshot()
                payload["control"] = (
                    controller.status()
                    if controller
                    else {"enabled": False, "running": False, "mode": ""}
                )
                payload["services"] = service_controller.list_status() if service_controller else []
                payload["marvin"] = (
                    marvin_controller.status()
                    if marvin_controller
                    else {"enabled": False, "running": False, "tmux": False, "robot_action": False}
                )
                self._send_json(payload)
                return
            self.send_error(HTTPStatus.NOT_FOUND, "Not found")

        def do_POST(self) -> None:
            path = urlparse(self.path).path
            parts = [item for item in path.split("/") if item]
            if len(parts) == 3 and parts[0] == "api" and parts[1] == "services":
                if service_controller is None:
                    self.send_error(HTTPStatus.NOT_FOUND, "Service control is not enabled")
                    return
                service_name = parts[2]
                self.send_error(HTTPStatus.NOT_FOUND, f"Missing action for {service_name}")
                return
            if len(parts) == 4 and parts[0] == "api" and parts[1] == "services":
                if service_controller is None:
                    self.send_error(HTTPStatus.NOT_FOUND, "Service control is not enabled")
                    return
                service_name = parts[2]
                action = parts[3]
                try:
                    payload = self._read_json()
                    camera_mode = str(payload.get("camera_mode", "single"))
                    if action == "start":
                        result = service_controller.start(service_name, camera_mode=camera_mode)
                    elif action == "stop":
                        result = service_controller.stop(service_name)
                    elif action == "restart":
                        result = service_controller.restart_with_mode(service_name, camera_mode=camera_mode)
                    elif action == "refresh":
                        result = service_controller.status(service_name)
                    else:
                        raise ValueError(f"unknown action: {action}")
                    self._send_json(result)
                except Exception as exc:
                    self._send_error_json(HTTPStatus.BAD_REQUEST, str(exc))
                return
            if path == "/api/control/start":
                if controller is None:
                    self.send_error(HTTPStatus.NOT_FOUND, "Control is not enabled")
                    return
                try:
                    payload = self._read_json()
                    camera_mode = str(payload.get("camera_mode", "single"))
                    if payload.get("mode"):
                        self._send_json(controller.start_mode(str(payload["mode"]), camera_mode=camera_mode))
                    else:
                        self._send_json(controller.start(str(payload.get("detector", "sam3")), camera_mode=camera_mode))
                except Exception as exc:
                    self._send_error_json(HTTPStatus.BAD_REQUEST, str(exc))
                return
            if path == "/api/control/stop":
                if controller is None:
                    self.send_error(HTTPStatus.NOT_FOUND, "Control is not enabled")
                    return
                self._send_json(controller.stop())
                return
            if path in {
                "/api/marvin/start",
                "/api/marvin/run",
                "/api/marvin/stop-action",
                "/api/marvin/stop-base",
            }:
                if marvin_controller is None:
                    self.send_error(HTTPStatus.NOT_FOUND, "MarvinDocker control is not enabled")
                    return
                try:
                    payload = self._read_json()
                    robot_ip = str(payload.get("robot_ip") or "").strip() or None
                    if path == "/api/marvin/start":
                        self._send_json(marvin_controller.start_base(robot_ip))
                    elif path == "/api/marvin/run":
                        self._send_json(marvin_controller.run_action(robot_ip))
                    elif path == "/api/marvin/stop-action":
                        self._send_json(marvin_controller.stop_action())
                    else:
                        self._send_json(marvin_controller.stop_base())
                except Exception as exc:
                    self._send_error_json(HTTPStatus.BAD_REQUEST, str(exc))
                return
            if path != "/api/video-stream":
                self.send_error(HTTPStatus.NOT_FOUND, "Not found")
                return
            try:
                payload = self._read_json()
                state.add_video_frame(payload)
                self._send_json({"status": "ok"})
            except Exception as exc:
                self._send_error_json(HTTPStatus.BAD_REQUEST, str(exc))

        def log_message(self, format: str, *args: Any) -> None:
            return

        def _read_json(self) -> dict[str, Any]:
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length)
            payload = json.loads(raw.decode("utf-8"))
            if not isinstance(payload, dict):
                raise ValueError("JSON root must be an object")
            return payload

        def _send_json(self, payload: dict[str, Any]) -> None:
            self._send_bytes(
                json.dumps(payload, ensure_ascii=False).encode("utf-8"),
                "application/json; charset=utf-8",
            )

        def _send_error_json(self, status: HTTPStatus, message: str) -> None:
            payload = json.dumps(
                {"status": "error", "message": message},
                ensure_ascii=False,
            ).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(payload)

        def _send_bytes(self, payload: bytes, content_type: str) -> None:
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(payload)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(payload)

    return FusionUiHandler


def start_zmq_listener(state: FusionUiState, addr: str) -> threading.Thread | None:
    if not addr:
        return None
    if zmq is None:
        state.add_event("fusion.listener.warning", {"message": "pyzmq is not installed; ZMQ events disabled"})
        return None

    def _worker() -> None:
        context = zmq.Context.instance()
        sock = context.socket(zmq.SUB)
        sock.setsockopt(zmq.RCVHWM, 100)
        sock.setsockopt(zmq.LINGER, 0)
        sock.connect(addr)
        sock.setsockopt_string(zmq.SUBSCRIBE, "")
        while True:
            try:
                message = sock.recv_string()
                topic, _, raw_payload = message.partition(" ")
                try:
                    payload = json.loads(raw_payload) if raw_payload else {}
                except json.JSONDecodeError:
                    payload = raw_payload
                state.add_event(topic or "message", payload)
            except Exception as exc:
                state.add_event("fusion.listener.error", {"message": str(exc)})
                time.sleep(0.5)

    thread = threading.Thread(target=_worker, daemon=True)
    thread.start()
    return thread


def serve_ui(
    *,
    host: str = "127.0.0.1",
    port: int = 8765,
    zmq_sub_addr: str = "tcp://127.0.0.1:8899",
    control_enabled: bool = False,
) -> None:
    state = FusionUiState()
    service_controller = ServiceController() if control_enabled else None
    marvin_controller = MarvinDockerController() if control_enabled else None
    controller = (
        FusionPipelineController(
            ui_url=f"http://127.0.0.1:{port}",
            service_controller=service_controller,
        )
        if control_enabled
        else None
    )
    start_zmq_listener(state, zmq_sub_addr)
    server = ThreadingHTTPServer(
        (host, port),
        make_handler(state, controller, service_controller, marvin_controller),
    )
    print(f"[FusionUI] http://{host}:{port}")
    print(f"[FusionUI] ZMQ SUB {zmq_sub_addr}")
    if control_enabled:
        print("[FusionUI] Pipeline control enabled")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        if controller:
            controller.stop()
        server.server_close()
