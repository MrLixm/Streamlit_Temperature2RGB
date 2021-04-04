"""
Convert Kelvin Temperatures to RGB values with given colorspace primaries.

Author: Liam Collod
Last Modified: 02/02/2021

Require colour-science >= 0.3.16
"""

import colour
import numpy

colour.utilities.filter_warnings(colour_usage_warnings=True)


def XYZ_to_colorspace(XYZ_values,
                      colorspace_name,
                      illuminant=None,
                      normalize=True,
                      CAT="Bradford"):
    """

    Args:
        CAT(str): Chromatic Adaptation transform
        XYZ_values(ndarray):
        colorspace_name(str): ex: "sRGB"
        illuminant(:obj:`str`, optional):
            Colorspace whitepoint if None else this is a CIE 1931 2 Degree
            Standard Observer illuminant. ex: 'D60'
        normalize(bool): normalize values to the 0-1 range

    Returns:
        ndarray: RGB values with the given colorpsace primaries.
    """

    csm = colour.RGB_COLOURSPACES[colorspace_name]
    if illuminant:
        source_illuminant = colour.CCS_ILLUMINANTS[
            'CIE 1931 2 Degree Standard Observer'][illuminant]
    else:
        source_illuminant = csm.whitepoint

    rgb = colour.XYZ_to_RGB(
        XYZ_values,
        source_illuminant,
        csm.whitepoint,
        csm.matrix_XYZ_to_RGB,
        chromatic_adaptation_transform=CAT
    )

    if normalize:
        rgb = colour.utilities.normalise_maximum(rgb, clip=True)

    return rgb


def cct_to_rgb_colorspace_planckian(
        temperature,
        colorspace,
        tint=0.0,
        illuminant=None,
        normalize=True,
        CAT = "Bradford",
):
    """

    Args:
        CAT(str): Chromatic Adaptation transform
        tint(float):
        temperature(int): Correlated Colour Temperature in Kelvin
        colorspace(str): ex: "sRGB"
        illuminant(:obj:`str`, optional):
            Colorspace whitepoint if None else this is a CIE 1931 2 Degree
            Standard Observer illuminant. ex: 'D60'
        normalize(bool): normalize values to the 0-1 range

    Returns:
        ndarray: RGB values with the given colorpsace primaries.
    """
    uv = colour.CCT_to_uv((temperature, tint))
    xy = colour.UCS_uv_to_xy(uv)
    XYZ = colour.xy_to_XYZ(xy)
    # XYZ = colour.sd_to_XYZ(colour.sd_blackbody(temperature), k=683)
    rgb = XYZ_to_colorspace(XYZ_values=XYZ,
                            colorspace_name=colorspace,
                            illuminant=illuminant,
                            normalize=normalize,
                            CAT=CAT)
    return rgb


def cct_range_to_rgb_colorspace_planckian(
        min_temp,
        max_temp,
        increment,
        colorspace,
        illuminant=None,
        normalize=True,
        CAT="Bradford",
):
    """ Print the RGB values for the temparature in the given range.

    Args:
        CAT(str): Chromatic Adaptation transform
        illuminant(:obj:`str`, optional):
            Colorspace whitepoint if None else this is a CIE 1931 2 Degree
            Standard Observer illuminant. ex: 'D60'
        normalize(bool): normalize values to the 0-1 range
        min_temp(int): Kelvin temparature: beginning of range
        max_temp(int): Kelvin temparature: end of range
        increment(int): step of range
        colorspace(str): ex: "sRGB"

    Returns:
        list of tuple: [( temperature(int), rgb_values(ndarray) ), ...]
    """
    output_result = []
    for temperature in range(min_temp, max_temp, increment):
        rgb_result = cct_to_rgb_colorspace_planckian(
            temperature,
            colorspace,
            illuminant=illuminant,
            normalize=normalize,
            CAT=CAT)
        output_result.append((temperature, rgb_result))

    return output_result


def cct_to_rgb_colorspace_daylight(
        temperature,
        colorspace,
        illuminant=None,
        normalize=True,
        CAT="Bradford",
):
    """

    Args:
        CAT(str): Chromatic Adaptation transform
        temperature(int): Correlated Colour Temperature in Kelvin
        colorspace(str): ex: "sRGB"
        illuminant(:obj:`str`, optional):
            Colorspace whitepoint if None else this is a CIE 1931 2 Degree
            Standard Observer illuminant. ex: 'D60'
        normalize(bool): normalize values to the 0-1 range

    Returns:
        ndarray: RGB values with the given colorpsace primaries.
    """
    # rescale because of changes in the Planck's constant
    temperature *= 1.4388 / 1.4380

    xy_CIED = colour.temperature.CCT_to_xy_CIE_D(temperature)
    XYZ = colour.xy_to_XYZ(xy_CIED)
    rgb = XYZ_to_colorspace(XYZ_values=XYZ,
                            colorspace_name=colorspace,
                            illuminant=illuminant,
                            normalize=normalize,
                            CAT=CAT)

    return rgb

