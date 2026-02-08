import json
import os
import time

from PIL import Image, ImageGrab
from PIL.PngImagePlugin import PngInfo

import requests
import io
import pyperclip
from urllib.parse import urlparse

import server
import folder_paths

def get_image_from_url(text:str) -> Image:
    return Image.open(io.BytesIO(requests.get(text).content))

def get_image_from_clipboard() -> Image:
    value = ImageGrab.grabclipboard()
    if value is None:
        return False

    if isinstance(value, list):
        if len(value) == 0:
            return False
        image = Image.open(value[0])
    else:
        image = value
    
    return image

def save_image(image:Image, path:str, prompt=None, extra_pnginfo=None):
    path = str(path)
    metadata = PngInfo()

    if prompt is not None:
        metadata.add_text("prompt", json.dumps(prompt))

    if extra_pnginfo is not None:
        for k, v in extra_pnginfo.items():
            metadata.add_text(k, json.dumps(v))

    image.save(path, pnginfo=metadata, compress_level=4)

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def ensure_path_to_image(prompt=None, extra_pnginfo: dict = None) -> str|None:
    text = pyperclip.paste()
    img = None
    if text:
        stripped = text.strip('"')
        if os.path.exists(stripped):
            return stripped
        elif is_valid_url(stripped):
            img = get_image_from_url(stripped)
    else:
        img = get_image_from_clipboard()
    
    if img:
        input_dir = folder_paths.get_input_directory()
        filename = time.strftime(f'image_%Y-%m-%d_%H-%M-%S.png')
        path = os.path.join(input_dir, 'pasted', filename)
        save_image(img, path, prompt = prompt, extra_pnginfo = extra_pnginfo)
        return path
    else:
        return None

def append_path_to_extra_pnginfo(json_data):
    path = ensure_path_to_image(
        prompt = json_data["prompt"],
        extra_pnginfo = json_data['extra_data']['extra_pnginfo'])
    if path:
        json_data['extra_data']['extra_pnginfo'].setdefault('ts_utility_nodes', {})['path_to_input_image'] = path
    return json_data

def onprompt(json_data):
    json_data = append_path_to_extra_pnginfo(json_data)
    return json_data

def initialize():
    server.PromptServer.instance.add_on_prompt_handler(onprompt)
