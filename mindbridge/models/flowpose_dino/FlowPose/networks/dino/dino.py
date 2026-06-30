import os
import torch

class DinoLoader:
    feat = None # static
    DEFAULT_LOCAL_REPO_PATH = '/workspace/model/facebookresearch_dinov2_main'

    def __init__(self, model_name: str = 'dinov2_vits14', device=None, local_repo_path=None, ckpt_path=None):
        self.model_name = model_name
        self.local_repo_path = local_repo_path
        self.ckpt_path = ckpt_path
        self.device = torch.device(device if device is not None else ('cuda' if torch.cuda.is_available() else 'cpu'))
        self._load_model()


    def _load_model(self):
        try:
            repo_path = self.local_repo_path or self.DEFAULT_LOCAL_REPO_PATH
            if os.path.isdir(repo_path):
                self.model = torch.hub.load(repo_path, self.model_name, source='local', pretrained=False).to(device=self.device)
            else:
                print(f"Warning: Local repository path '{repo_path}' does not exist. Attempting to load model from torch.hub.")
                self.model = torch.hub.load('facebookresearch/dinov2', self.model_name)

            # ===== load local weights =====
            ckpt_path = self.ckpt_path
            if not ckpt_path or not os.path.exists(ckpt_path):
                print(f"Warning: DINO ckpt path '{ckpt_path}' does not exist, using model without pretrained weights.")
            else:
                ckpt = torch.load(ckpt_path, map_location="cpu")
                if "model" in ckpt:
                    state_dict = ckpt["model"]
                else:
                    state_dict = ckpt
                self.model.load_state_dict(state_dict, strict=True)

            self.model.to(self.device)
            self.model.requires_grad_(False)
            self.model.eval()
        except Exception as e:
            raise RuntimeError(f"Failed to load DINO model '{self.model_name}': {e}")

    def extract_features(self, roi_rgb: torch.Tensor) -> torch.Tensor:
        with torch.no_grad():
            feat = self.model.get_intermediate_layers(roi_rgb)[0]
            self.__class__.feat = feat

    def get_feature(self) -> torch.Tensor:
        if self.__class__.feat is None:
            raise ValueError("No features extracted yet. Call extract_features() first.")
        return self.__class__.feat
