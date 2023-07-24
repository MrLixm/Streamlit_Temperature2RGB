import colour

from . import config
from streamlit_temperature2rgb.core import PlanckianCCTConversion
from streamlit_temperature2rgb.core import DaylightCCTConversion
from streamlit_temperature2rgb.core import rgb_array_to_image


_colorspace = config.USER_COLORSPACE_NAME.as_core()
_colorspace: colour.RGB_Colourspace = colour.RGB_COLOURSPACES[_colorspace]

_whitepoint = config.USER_ILLUMINANT_NAME.as_core()
if _whitepoint is None:
    _whitepoint = _colorspace.whitepoint
else:
    _whitepoint = colour.CCS_ILLUMINANTS["CIE 1931 2 Degree Standard Observer"]
    _whitepoint = _whitepoint[_whitepoint]

_tint = config.USER_TINT / 3000

if config.USER_DAYLIGHT_MODE:
    _conversion = DaylightCCTConversion(
        CCT=config.USER_TEMPERATURE,
        colorspace=_colorspace,
        illuminant=_whitepoint,
        cat=config.USER_CAT_NAME.as_core(),
    )
else:
    _conversion = PlanckianCCTConversion(
        CCT=config.USER_TEMPERATURE,
        colorspace=_colorspace,
        illuminant=_whitepoint,
        cat=config.USER_CAT_NAME.as_core(),
        tint=_tint,
    )


def get_preview_image(width: int, height: int):
    if config.USER_COLORSPACE_NAME == config.USER_COLORSPACE_NAME.sRGB:
        conversion_preview = _conversion
    else:
        conversion_preview = _conversion.with_colorspace(
            colour.RGB_COLOURSPACES["sRGB"]
        )

    array = conversion_preview.rgb
    array = colour.algebra.normalise_maximum(array, clip=True)
    array = rgb_array_to_image(array, width, height)
    return array


def get_rgb_array():
    array = _conversion.rgb
    if config.USER_NORMALIZE:
        array = colour.algebra.normalise_maximum(array, clip=True)
    return array


def get_xy_array():
    return _conversion.xy


def get_nuke_node_name():
    if config.USER_DAYLIGHT_MODE:
        nuke_node_name = f"Daylight_{config.USER_TEMPERATURE}K_{config.USER_COLORSPACE_NAME.as_label()}"
    else:
        nuke_node_name = f"Planckian_{config.USER_TEMPERATURE}K_{config.USER_COLORSPACE_NAME.as_label()}_{config.USER_TINT}"

    return nuke_node_name
