from ctypes import (
    byref,
    cdll,
    create_string_buffer,
    c_char_p,
    c_int,
    c_void_p,
    c_bool,
    POINTER,
    string_at,
    c_int32
)
import platform
from pathlib import Path

__all__ = ['lib']

system = platform.system()

if system == "Windows":
    lib = "renderer.dll"
else:
    lib = "librenderer.so"


lib = cdll.LoadLibrary(Path(__file__).parent / "libs" / lib)
lib.renderToPNG.argtypes = [c_char_p]
lib.renderToPNG.restype = c_bool

lib.initializeRenderer.argtypes = [c_int, c_int]
lib.initializeRenderer.restype = None

lib.updateRenderer.argtypes = []
lib.updateRenderer.restype = None

lib.loadHTML.argtypes = [c_char_p]
lib.loadHTML.restype = c_bool

lib.renderCroppedToImage.argtypes = [c_char_p, c_char_p]
lib.renderCroppedToImage.restype = c_bool
