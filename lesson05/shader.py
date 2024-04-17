from abc import ABC, abstractmethod

from PIL import Image

from vector import Vec2, Vec4, Vec3


class IShader(ABC):
    @staticmethod
    def sample_2d(img: Image, uvf: Vec2):
        pixel = img.getpixel((uvf.x * img.width, uvf.y * img.height))
        return pixel

    @abstractmethod
    def vertex(self, iface: int, nthvert: int) -> Vec4:
        pass

    @abstractmethod
    def fragment(self, bar: Vec3):
        pass
