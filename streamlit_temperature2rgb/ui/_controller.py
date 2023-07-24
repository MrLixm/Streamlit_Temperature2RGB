import colour

from . import config
from streamlit_temperature2rgb.core import PlanckianCCTConversion
from streamlit_temperature2rgb.core import DaylightCCTConversion
from streamlit_temperature2rgb.core import rgb_array_to_image


class ConversionResult:
    def __init__(
        self,
        CCT,
        colorspace_name,
        illuminant_name,
        cat,
        tint,
        use_daylight,
        normalize,
    ):
        self._user_CCT = CCT
        self._user_colorspace_name = colorspace_name
        self._user_illuminant_name = illuminant_name
        self._user_cat = cat
        self._user_tint = tint
        self._user_use_daylight = use_daylight
        self._user_normalize = normalize

        _colorspace = colorspace_name.as_core()
        _colorspace: colour.RGB_Colourspace = colour.RGB_COLOURSPACES[_colorspace]

        _whitepoint = illuminant_name.as_core()
        if _whitepoint is None:
            _whitepoint = _colorspace.whitepoint
        else:
            _whitepoint = colour.CCS_ILLUMINANTS["CIE 1931 2 Degree Standard Observer"]
            _whitepoint = _whitepoint[_whitepoint]

        _tint = tint / 3000

        if use_daylight:
            _conversion = DaylightCCTConversion(
                CCT=CCT,
                colorspace=_colorspace,
                illuminant=_whitepoint,
                cat=cat.as_core(),
            )
        else:
            _conversion = PlanckianCCTConversion(
                CCT=CCT,
                colorspace=_colorspace,
                illuminant=_whitepoint,
                cat=cat.as_core(),
                tint=_tint,
            )

        self._rgb_array = _conversion.rgb
        if normalize:
            self._rgb_array = colour.algebra.normalise_maximum(
                self._rgb_array, clip=True
            )

        self._xy_array = _conversion.xy

    def get_preview_image(self, width: int, height: int):
        conversion_preview = self.__class__(
            self._user_CCT,
            # only change :
            self._user_colorspace_name.sRGB,
            self._user_illuminant_name,
            self._user_cat,
            self._user_tint,
            self._user_use_daylight,
            self._user_normalize,
        )

        array = conversion_preview.get_rgb_array()
        array = colour.algebra.normalise_maximum(array, clip=True)
        array = rgb_array_to_image(array, width, height)
        return array

    def get_rgb_array(self):
        return self._rgb_array

    def get_xy_array(self):
        return self._xy_array

    def get_nuke_node_name(self):
        if self._user_use_daylight:
            nuke_node_name = (
                f"Daylight_{self._user_CCT}K_{self._user_colorspace_name.as_label()}"
            )
        else:
            nuke_node_name = f"Planckian_{self._user_CCT}K_{self._user_colorspace_name.as_label()}_{self._user_tint}"

        return nuke_node_name

    @classmethod
    def from_active_context(cls):
        return cls(
            config.USER_TEMPERATURE,
            config.USER_COLORSPACE_NAME,
            config.USER_ILLUMINANT_NAME,
            config.USER_CAT_NAME,
            config.USER_TINT,
            config.USER_DAYLIGHT_MODE,
            config.USER_NORMALIZE,
        )
