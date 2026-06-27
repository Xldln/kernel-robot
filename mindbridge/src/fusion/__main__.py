from __future__ import annotations

import argparse
import threading
import time

from mindbridge.src.fusion.ui_server import serve_ui


def main() -> None:
    parser = argparse.ArgumentParser(description="Standalone MindBridge Fusion runner")
    subparsers = parser.add_subparsers(dest="command", required=True)

    ui_parser = subparsers.add_parser("serve-ui", help="Start the standalone Fusion UI")
    _add_ui_args(ui_parser)

    run_parser = subparsers.add_parser("run", help="Start Fusion UI and MindBridge main loop")
    _add_ui_args(run_parser)
    run_parser.add_argument("--detector", choices=["sam3", "yolo"], default="sam3")
    run_parser.add_argument("--pipeline", choices=["basic", "full"], default="full")
    run_parser.add_argument("--rgb-source", choices=["realsense", "usb"], default="realsense")
    run_parser.add_argument("--camera-mode", choices=["single", "multi"], default="single")
    run_parser.add_argument("--camera-index", type=int, default=0)
    run_parser.add_argument("--camera-width", type=int, default=None)
    run_parser.add_argument("--camera-height", type=int, default=None)
    run_parser.add_argument("--camera-fps", type=int, default=None)
    run_parser.add_argument("--sam3-prompts", type=str, default=None)
    run_parser.add_argument("--sam3-threshold", type=float, default=None)
    run_parser.add_argument("--show", action="store_true", help="Also show the OpenCV window")
    run_parser.add_argument("--max-frames", type=int, default=None)
    run_parser.add_argument("--log-interval", type=int, default=30)
    run_parser.add_argument("--fusion-ui-interval", type=int, default=3)
    run_parser.add_argument("--realsense-url", default="http://127.0.0.1:8000")
    run_parser.add_argument("--yolo-url", default="http://127.0.0.1:8001")
    run_parser.add_argument("--siglip-url", default="http://127.0.0.1:8002")
    run_parser.add_argument("--sam3-url", default="http://127.0.0.1:8005")
    run_parser.add_argument("--fastfoundation-url", default="http://127.0.0.1:8004")
    run_parser.add_argument("--flowpose-url", default="http://127.0.0.1:8006")

    args = parser.parse_args()

    if args.command == "serve-ui":
        serve_ui(
            host=args.ui_host,
            port=args.ui_port,
            zmq_sub_addr=args.zmq_sub_addr,
            control_enabled=args.control,
        )
        return

    if args.command == "run":
        _run_with_ui(args)
        return


def _add_ui_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--ui-host", default="127.0.0.1")
    parser.add_argument("--ui-port", type=int, default=8765)
    parser.add_argument("--zmq-pub-addr", default="tcp://0.0.0.0:8899")
    parser.add_argument("--zmq-sub-addr", default="tcp://127.0.0.1:8899")
    parser.add_argument("--control", action="store_true", help="Enable browser buttons to start/stop pipelines")


def _run_with_ui(args: argparse.Namespace) -> None:
    from mindbridge.src.main import run as run_mindbridge

    ui_thread = threading.Thread(
        target=serve_ui,
        kwargs={
            "host": args.ui_host,
            "port": args.ui_port,
            "zmq_sub_addr": args.zmq_sub_addr,
            "control_enabled": False,
        },
        daemon=True,
    )
    ui_thread.start()
    time.sleep(0.2)

    run_mindbridge(
        realsense_url=args.realsense_url,
        yolo_url=args.yolo_url,
        siglip_url=args.siglip_url,
        sam3_url=args.sam3_url,
        fastfoundation_url=args.fastfoundation_url,
        flowpose_url=args.flowpose_url,
        rgb_source=args.rgb_source,
        camera_mode=args.camera_mode,
        camera_index=args.camera_index,
        camera_width=args.camera_width,
        camera_height=args.camera_height,
        camera_fps=args.camera_fps,
        detector=args.detector,
        pipeline=args.pipeline,
        sam3_prompts=args.sam3_prompts,
        sam3_threshold=args.sam3_threshold,
        show=args.show,
        max_frames=args.max_frames,
        log_interval=args.log_interval,
        fusion_ui_interval=args.fusion_ui_interval,
        fusion_pub=True,
        fusion_pub_addr=args.zmq_pub_addr,
        fusion_ui_url=f"http://{args.ui_host}:{args.ui_port}",
    )


if __name__ == "__main__":
    main()
