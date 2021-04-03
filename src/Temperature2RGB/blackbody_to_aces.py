"""
Convert Kelvin Temperatures to RGB values with given colorspace primaries.

Author: Liam Collod
Last Modified: 02/02/2021

Require colour-science >= 0.3.16
"""

import colour
import numpy

colour.utilities.filter_warnings(colour_usage_warnings=True)


def temperature_to_RGB(temperature, colorspace, illuminants=None,
                       cctf_encoding=False, clip=True):
    """

    Args:
        clip(bool): If True value should be clipped between the 0-1 range
        illuminants: if specified this illuminant will be used instead
         of the colorspace whitepoint. ex: 'E'
        temperature(int): temperature in Kelvin to compute
        colorspace(str): colorspace model, ex: 'sRGB' or 'ACEScg'
        cctf_encoding(bool): apply the cttf encoding ?

    Returns:
        numpy.ndarray: 1D array

    """
    csm = colour.RGB_COLOURSPACES[colorspace]
    if illuminants:
        illuminant_lab = colour.CCS_ILLUMINANTS[
            'CIE 1931 2 Degree Standard Observer'][illuminants]
    else:
        illuminant_lab = csm.whitepoint

    XYZ = colour.sd_to_XYZ(colour.sd_blackbody(temperature), k=683)
    RGB = colour.XYZ_to_RGB(
        XYZ, illuminant_lab, csm.whitepoint, csm.matrix_XYZ_to_RGB)
    if cctf_encoding:
        colour.cctf_encoding(RGB, colorspace)

    if clip:
        RGB = colour.utilities.normalise_maximum(RGB, clip=clip)

    return RGB


def temperature_range_to_RGB(min_temp, max_temp, increment, colorspace, clip):
    """ Print the RGB values for the temparature in the given range.

    Args:
        min_temp(int): Kelvin temparature: beginning of range
        max_temp(int): Kelvin temparature: end of range
        increment(int): step of range
        colorspace(str): colorspace model, ex: 'sRGB' or 'ACEScg'

    Returns:
        None
    """
    output_result = []
    for temp in range(min_temp, max_temp, increment):
        rgb_result = temperature_to_RGB(
            temp, colorspace=colorspace, cctf_encoding=False, clip=clip)
        output_result.append((temp, rgb_result))

    return output_result

