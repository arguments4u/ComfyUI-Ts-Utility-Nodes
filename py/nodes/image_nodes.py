import numpy as np
import torch
from PIL import Image

def load_image(path, mode:str)->torch.Tensor:
    image = Image.open(path).convert(mode)
    array = np.array(image).astype(np.float32) / 255.0
    tensor = torch.from_numpy(array).unsqueeze(0)
    return tensor

def get_image_path_from_extra_pnginfo(extra_pnginfo:dict):
    match extra_pnginfo:
        case {'ts_utility_nodes': {'path_to_input_image': path}}:
            return path
        case _:
            return None
        
def get_color_and_mask(image:torch.Tensor)->tuple[torch.Tensor,torch.Tensor]:
    return (image[:, :, :, 0:3], image[0, :, :, 3])

def execute_impl(extra_pnginfo:dict, mode:str)->tuple[torch.Tensor,str]|tuple[torch.Tensor,torch.Tensor,str]:
    path = get_image_path_from_extra_pnginfo(extra_pnginfo)
    if path:
        image = load_image(path, mode)
        if image is None:
            raise ValueError(f"failed to load image from {path}")
    else:
        raise ValueError(f"failed to get path to image from extra_pnginfo['ts_utility_nodes']['path_to_input_image']")
    
    if mode == "RGBA":
        color, mask = get_color_and_mask(image)
        return (color, mask, path)
    else:
        return (image, path)


class TsLoadImageRGBClipSnapshot:
    CATEGORY = "image"
    @classmethod
    def INPUT_TYPES(s):
        return {"hidden":{"extra_pnginfo": "EXTRA_PNGINFO"}}

    RETURN_TYPES = ("IMAGE","STRING")
    RETURN_NAMES = ("image", "filepath")
    FUNCTION = "execute"
    
    def execute(self, extra_pnginfo:dict):
        return execute_impl(extra_pnginfo, "RGB")

    def IS_CHANGED(self, extra_pnginfo):
        # This value will be compared with previous 'IS_CHANGED' outputs
        # If inequal, then this node will be considered as modified
        return get_image_path_from_extra_pnginfo(extra_pnginfo)

class TsLoadImageRGBAClipSnapshot:
    CATEGORY = "image"
    @classmethod
    def INPUT_TYPES(s):
        return {"hidden":{"extra_pnginfo": "EXTRA_PNGINFO"}}
    
    RETURN_TYPES = ("IMAGE", "MASK", "STRING")
    RETURN_NAMES = ("image", "mask", "filepath")
    FUNCTION = "execute"
    
    def execute(self, extra_pnginfo):
        return execute_impl(extra_pnginfo, "RGBA")

    def IS_CHANGED(self, extra_pnginfo):
        # This value will be compared with previous 'IS_CHANGED' outputs
        # If inequal, then this node will be considered as modified
        return get_image_path_from_extra_pnginfo(extra_pnginfo)

NODE_CLASS_MAPPINGS = {
    "TsLoadImageRGBClipSnapshot":TsLoadImageRGBClipSnapshot,
    "TsLoadImageRGBAClipSnapshot":TsLoadImageRGBAClipSnapshot
    }
NODE_DISPLAY_NAME_MAPPINGS = {
    "TsLoadImageRGBClipSnapshot":"Load Image RGB (Clip Snapshot)",
    "TsLoadImageRGBAClipSnapshot":"Load Image RGBA (Clip Snapshot)"
    }
