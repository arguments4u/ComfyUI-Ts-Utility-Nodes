from .py import server
from .py.nodes import image_nodes

NODE_CLASS_MAPPINGS = image_nodes.NODE_CLASS_MAPPINGS
NODE_DISPLAY_NAME_MAPPINGS = image_nodes.NODE_DISPLAY_NAME_MAPPINGS
WEB_DIRECTORY = "./js"

server.initialize()