import os
from typing import IO
from PIL import Image

type ImageSource = str | bytes | os.PathLike[str] | os.PathLike[bytes] | IO[bytes]
type ImageWithMessage = tuple[Image.Image|None, str|None]

