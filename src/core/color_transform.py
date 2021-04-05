"""
Convert Kelvin Temperatures to RGB values with given colorspace primaries.

Author: Liam Collod
Last Modified: 02/02/2021

Require colour-science >= 0.3.16
"""

import colour
import numpy

colour.utilities.filter_warnings(colour_usage_warnings=True)


def XYZ_to_colorspace(
    XYZ_values,
    colorspace_name,
    illuminant=None,
    CAT="Bradford"
):
    """

    Args:
        CAT(str): Chromatic Adaptation transform
        XYZ_values(ndarray):
        colorspace_name(str): ex: "sRGB"
        illuminant(:obj:`str`, optional):
            Colorspace whitepoint if None else this is a CIE 1931 2 Degree
            Standard Observer illuminant. ex: 'D60'

    Returns:
        ndarray: RGB values with the given colorpsace primaries.
    """

    csm = colour.RGB_COLOURSPACES[colorspace_name]
    if illuminant:
        source_illuminant = colour.CCS_ILLUMINANTS[
            'CIE 1931 2 Degree Standard Observer'][illuminant]
    else:
        source_illuminant = csm.whitepoint

    return colour.XYZ_to_RGB(
        XYZ_values,
        source_illuminant,
        csm.whitepoint,
        csm.matrix_XYZ_to_RGB,
        chromatic_adaptation_transform=CAT
    )


class Array:
    """
    Hold a numpy ndarray
    """
    def __init__(self, array_value):
        """
        Args:
            array_value(numpy.ndarray):
        """
        self._value = array_value

    @property
    def normalized(self):
        return colour.utilities.normalise_maximum(self._value, clip=True)

    def value(self, normalized):
        return self.normalized if normalized else self._value


class Planckian:
    def __init__(self, temperature):
        """

        Args:
            temperature(TemperatureObject):
        """
        self.temperature_object = temperature
        self._uv = None
        self._xy = None
        self._XYZ = None

    @property
    def uv(self):
        """
        Returns:
            numpy.ndarray: CIE UCS uv coordinates
        """
        if self._uv:
            return self._uv
        else:
            return colour.CCT_to_uv((self.temperature_object.CCT,
                                     self.temperature_object.tint))

    @property
    def xy(self):
        """
        Returns:
            numpy.ndarray: CIE xy chromaticity coordinates
        """
        if self._xy:
            return self._xy
        else:
            return colour.UCS_uv_to_xy(self.uv)

    @property
    def XYZ(self):
        """
        Returns:
            numpy.ndarray: CIE XYZ tristimulus values
        """
        if self._XYZ:
            return self._XYZ
        else:
            return colour.xy_to_XYZ(self.xy)

    def rgb(self, primaries, illuminant, CAT):
        """

        Args:
            primaries(str):
            illuminant(str):
            CAT(str):

        Returns:
            Array: Array object with RGB colorspace primaries
        """
        return Array(
            XYZ_to_colorspace(
                XYZ_values=self.XYZ,
                colorspace_name=primaries,
                illuminant=illuminant,
                CAT=CAT
            ))


class Daylight(Planckian):

    @property
    def xy(self):
        """
        Returns:
            numpy.ndarray: CIE xy chromaticity coordinates
        """
        if self._xy:
            return self._xy
        else:
            # rescale because of changes in the Planck's constant
            temperature = self.temperature_object.CCT * 1.4388 / 1.4380
            return colour.temperature.CCT_to_xy_CIE_D(temperature)


class TemperatureObject:
    def __init__(self,
                 CCT,
                 tint=0.0):
        """

        Args:
            tint(float): -0.05, 0.05 range
            CCT(int): Correlated Colour Temperature in Kelvin

        Returns:
            ndarray: RGB values with the given colorpsace primaries.
        """

        self.CCT = CCT
        self.tint = tint

    @property
    def planckian(self):
        return Planckian(self)

    @property
    def daylight(self):
        return Daylight(self)


