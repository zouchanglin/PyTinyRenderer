from abc import ABC, abstractmethod

from PIL import Image

from color import Color
from vector import Vec2, Vec3


class IShader(ABC):
    @staticmethod
    def sample_2d(img: Image, uvf: Vec2):
        pixel = img.getpixel((uvf.x * img.width, uvf.y * img.height))
        return pixel

    @abstractmethod
    def vertex(self, iface: int, n: int):
        pass

    @abstractmethod
    def fragment(self, bar: Vec3) -> (bool, Color):
        pass
