import abc
import dataclasses
import functools

import colour
import numpy


@dataclasses.dataclass(frozen=True)
class BaseCCTConversion:
    CCT: float
    colorspace: colour.RGB_Colourspace
    illuminant: numpy.ndarray
    cat: str

    @property
    @abc.abstractmethod
    def xy(self) -> numpy.ndarray:
        """
        Returns:
            CIE xy chromaticity coordinates
        """
        pass

    @functools.cached_property
    def XYZ(self) -> numpy.ndarray:
        """
        Returns:
           CIE XYZ tristimulus values
        """
        return colour.xy_to_XYZ(self.xy)

    @functools.cached_property
    def rgb(self):
        return colour.XYZ_to_RGB(
            self.XYZ,
            self.illuminant,
            self.colorspace.whitepoint,
            self.colorspace.matrix_XYZ_to_RGB,
            chromatic_adaptation_transform=self.cat,
        )

    def with_colorspace(self, new_colorspace: colour.RGB_Colourspace):
        return dataclasses.replace(self, colorspace=new_colorspace)


@dataclasses.dataclass(frozen=True)
class PlanckianCCTConversion(BaseCCTConversion):
    tint: float

    @functools.cached_property
    def uv(self) -> numpy.ndarray:
        """
        Returns:
            CIE UCS uv coordinates
        """
        return colour.CCT_to_uv((self.CCT, self.tint))

    @functools.cached_property
    def xy(self) -> numpy.ndarray:
        """
        Returns:
            CIE xy chromaticity coordinates
        """
        return colour.UCS_uv_to_xy(self.uv)


@dataclasses.dataclass(frozen=True)
class DaylightCCTConversion(BaseCCTConversion):
    @functools.cached_property
    def xy(self) -> numpy.ndarray:
        """
        Returns:
            CIE xy chromaticity coordinates
        """
        # rescale cause of changes in the Planck's constant
        CCT = self.CCT * 1.4388 / 1.4380
        return colour.temperature.CCT_to_xy_CIE_D(CCT)


def rgb_array_to_image(array: numpy.ndarray, width: int, height: int) -> numpy.ndarray:
    # apply the 2.2 power function as transfer function and convert to 8bit
    image = (array ** (1 / 2.2) * 255).astype(numpy.uint8)
    image = numpy.full((height, width, 3), image, dtype=numpy.uint8)
    return image
