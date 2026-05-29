import requests


class MindBridgeClient:
    """Control Center 客户端，对接服务。"""

    def __init__(
        self,
        realsense_url: str = "http://127.0.0.1:8000",
        yolo_url: str = "http://127.0.0.1:8001",
        siglip_url: str = "http://127.0.0.1:8002",
    ):
        self.realsense_url = realsense_url.rstrip("/")
        self.yolo_url = yolo_url.rstrip("/")
        self.siglip_url = siglip_url.rstrip("/")

    def health(self) -> dict:
        result: dict = {}
        for name, url in [
            ("realsense", self.realsense_url),
            ("yolo", self.yolo_url),
            ("siglip", self.siglip_url),
        ]:
            try:
                r = requests.get(f"{url}/health", timeout=2)
                result[name] = r.json()
            except Exception as e:
                result[name] = {"status": "unreachable", "error": str(e)}
        return result

    def capture(self) -> dict:
        r = requests.post(f"{self.realsense_url}/realsense/capture", timeout=10)
        r.raise_for_status()
        return r.json()

    def predict(self, image_b64: str, request_id: str = "") -> dict:
        body = {
            "request_id": request_id,
            "image_b64": image_b64,
            "return_masks": False,
            "return_annotated_image": True,
        }
        r = requests.post(f"{self.yolo_url}/infer/predict", json=body, timeout=10)
        r.raise_for_status()
        return r.json()

    def classify_state(self, image_b64: str, request_id: str = "") -> dict:
        """调用 SigLIP 服务进行状态分类"""
        body = {
            "request_id": request_id,
            "image_b64": image_b64,
        }
        r = requests.post(f"{self.siglip_url}/infer/predict", json=body, timeout=10)
        r.raise_for_status()
        return r.json()
