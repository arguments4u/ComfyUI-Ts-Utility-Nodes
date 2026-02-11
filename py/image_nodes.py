import numpy as np
import torch
from PIL import Image
from abc import ABC, abstractmethod

from . import extra_pnginfo_interface

def load_image(path, mode:str)->torch.Tensor:
    image = Image.open(path).convert(mode)
    array = np.array(image).astype(np.float32) / 255.0
    tensor = torch.from_numpy(array).unsqueeze(0)
    return tensor
        
def get_color_and_mask(image:torch.Tensor)->tuple[torch.Tensor,torch.Tensor]:
    return (image[:, :, :, 0:3], image[0, :, :, 3])

class TsLoadImageClipSnapshotBase(ABC):
    CATEGORY = "image"
    FUNCTION = "execute"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": {
                "default_image": ("IMAGE",), 
            },
            "hidden":{"extra_pnginfo": "EXTRA_PNGINFO"}
            }
    
    def execute_impl(self,extra_pnginfo:dict, mode:str, default_image:torch.Tensor|None)->tuple[torch.Tensor,str]|tuple[torch.Tensor,torch.Tensor,str]:
        clip_snapshot = extra_pnginfo_interface.get_clip_snapshot(extra_pnginfo)
        
        path = clip_snapshot['path']
        message = clip_snapshot['message']

        if path:
            image = load_image(path, mode)
            if image is None:
                raise ValueError(f"Error:failed to load image from {path}")
        elif default_image is not None:
            image = default_image
        elif message:
            raise ValueError(message)
        else:
            raise ValueError("Error:failed to get path to image from extra_pnginfo['ts_utility_nodes']['path_to_input_image']")
        
        if mode == "RGBA":
            color, mask = get_color_and_mask(image)
            return (color, mask, path)
        else:
            return (image, path)
        
    @abstractmethod
    def execute(self, extra_pnginfo:dict, default_image=None):
        pass

    @classmethod
    def IS_CHANGED(cls, extra_pnginfo):
        # This value will be compared with previous 'IS_CHANGED' outputs
        # If inequal, then this node will be considered as modified
        clip_snapshot = extra_pnginfo_interface.get_clip_snapshot(extra_pnginfo)
        return (clip_snapshot['path'], clip_snapshot['message'])
    
class TsLoadImageRGBClipSnapshot(TsLoadImageClipSnapshotBase):
    """
    This node allow you to load images from the clipboard by capturing a snapshot at the exact moment of queueing.
    This ensures that the correct data is processed even if your clipboard is overwritten before the actual node execution.

    Inputs:
        default_image (IMAGE): the default image output when clipboard data cannot be imported as an image
    
    Outputs:
        image (IMAGE): the image loaded from snapshot
        filepath (STRING): path to the snapshot
    """
    RETURN_TYPES = ("IMAGE","STRING")
    RETURN_NAMES = ("image", "filepath")
    
    def execute(self, extra_pnginfo:dict, default_image:torch.Tensor|None):
        return super().execute_impl(extra_pnginfo, "RGB", default_image)

class TsLoadImageRGBAClipSnapshot(TsLoadImageClipSnapshotBase):
    """
    This node allow you to load images from the clipboard by capturing a snapshot at the exact moment of queueing.
    This ensures that the correct data is processed even if your clipboard is overwritten before the actual node execution.

    Inputs:
        default_image (IMAGE): the default image output when clipboard data cannot be imported as an image
    
    Outputs:
        image (IMAGE): the image loaded from color channel of snapshot
        mask (MASK): the mask loaded from alpha channel of snapshot
        filepath (STRING): path to the snapshot
    """
    RETURN_TYPES = ("IMAGE", "MASK", "STRING")
    RETURN_NAMES = ("image", "mask", "filepath")
    
    def execute(self, extra_pnginfo, default_image:torch.Tensor|None):
        return super().execute_impl(extra_pnginfo, "RGBA", default_image)

NODE_CLASS_MAPPINGS = {
    "TsLoadImageRGBClipSnapshot":TsLoadImageRGBClipSnapshot,
    "TsLoadImageRGBAClipSnapshot":TsLoadImageRGBAClipSnapshot
    }
NODE_DISPLAY_NAME_MAPPINGS = {
    "TsLoadImageRGBClipSnapshot":"Load Image RGB (Clip Snapshot)",
    "TsLoadImageRGBAClipSnapshot":"Load Image RGBA (Clip Snapshot)"
    }
