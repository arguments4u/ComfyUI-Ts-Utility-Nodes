import json
import os
import time
from typing import IO

from PIL import Image, ImageGrab, ImageFile
from PIL.PngImagePlugin import PngInfo

import requests
import io
import pyperclip
from urllib.parse import urlparse

import server
import folder_paths

from . import types_definition, extra_pnginfo_interface

def is_valid_image(image_source:types_definition.ImageSource)->bool:
    try:
        with Image.open(image_source) as image:
            image.verify() # 画像データが壊れていないか確認
        return True
    except Exception:
        return False

def get_image_from_url(text:str) -> types_definition.ImageWithMessage:
    bytes_io = io.BytesIO(requests.get(text).content)
    if is_valid_image(bytes_io):
        return (Image.open(bytes_io), None)
    else:
        return (None, f'Error:failed to get image from {text}')

def get_image_from_clipboard() -> types_definition.ImageWithMessage:
    value = ImageGrab.grabclipboard()
    error_message = 'Error:failed to get image from clipboard.'
    if value is None:
        return (None, error_message)
    if isinstance(value, list):
        if len(value) == 0:
            return (None, error_message)
        image = Image.open(value[0])
    else:
        image = value
    
    return (image, None)

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

def ensure_path_to_image(prompt, extra_pnginfo):
    text = pyperclip.paste()
    path:str|None = None
    image:Image.Image = None
    message:str|None = None

    if text:
        stripped = text.strip('"')
        if os.path.exists(stripped):
            if is_valid_image(stripped):
                path = stripped
            else:
                message = f'Error:{stripped} is not path to image.'
        elif is_valid_url(stripped):
            image, message = get_image_from_url(stripped)
    else:
        image, message = get_image_from_clipboard()
    
    if image:
        input_dir = folder_paths.get_input_directory()
        filename = time.strftime('image_%Y-%m-%d_%H-%M-%S.png')
        path = os.path.join(input_dir, 'pasted', filename)
        extra_pnginfo_interface.set_clip_snapshot(
            extra_pnginfo = extra_pnginfo, 
            path = path, 
            message = message)
        save_image(
            image = image, 
            path = path, 
            prompt = prompt, 
            extra_pnginfo = extra_pnginfo)
    else:
        extra_pnginfo_interface.set_clip_snapshot(
            extra_pnginfo = extra_pnginfo, 
            path = path, 
            message = message)

def append_snapshot_to_extra_pnginfo(json_data):
    ensure_path_to_image(
        prompt = json_data["prompt"],
        extra_pnginfo = json_data['extra_data']['extra_pnginfo'])
    return json_data

def onprompt(json_data):
    json_data = append_snapshot_to_extra_pnginfo(json_data)
    return json_data

def initialize():
    server.PromptServer.instance.add_on_prompt_handler(onprompt)
