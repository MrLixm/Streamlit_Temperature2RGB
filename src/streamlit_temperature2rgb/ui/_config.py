import streamlit

from streamlit_temperature2rgb._utils import UifiedEnum


class Colorspaces(UifiedEnum):
    sRGB = ("sRGB - BT.709", "sRGB")
    ACEScg = ("ACEScg", "ACEScg")
    AdobeWideGamut = ("Adobe Wide Gamut RGB", "Adobe Wide Gamut RGB")
    P3D65 = ("P3-D65", "P3-D65")
    BT2020 = ("ITU-R BT.2020", "ITU-R BT.2020")
    AdobeRGB = ("Adobe RGB (1998)", "Adobe RGB (1998)")


class Illuminants(UifiedEnum):
    colorspace = ("Same as Colorspace", None)
    D50 = ("D50", "D50")
    D55 = ("D55", "D55")
    D60 = ("D60", "D60")
    D65 = ("D65", "D65")
    D75 = ("D75", "D75")
    E = ("E", "E")


class ChromaticAdaptationTransforms(UifiedEnum):
    Bradford = ("Bradford", "Bradford")
    CAT02 = ("CAT02", "CAT02")
    VonKries = ("Von Kries", "Von Kries")
    XYZScaling = ("XYZ Scaling", "XYZ Scaling")
    Bianco2010 = ("Bianco 2010", "Bianco 2010")


class UserConfig:
    def __init__(self):
        if "USER_TEMPERATURE" not in streamlit.session_state:
            streamlit.session_state["USER_TEMPERATURE"] = 2500.0
        if "USER_DAYLIGHT_MODE" not in streamlit.session_state:
            streamlit.session_state["USER_DAYLIGHT_MODE"] = False
        if "USER_TINT" not in streamlit.session_state:
            streamlit.session_state["USER_TINT"] = 0.0
        if "USER_ILLUMINANT_NAME" not in streamlit.session_state:
            streamlit.session_state["USER_ILLUMINANT_NAME"] = Illuminants.colorspace
        if "USER_NDECIMALS" not in streamlit.session_state:
            streamlit.session_state["USER_NDECIMALS"] = 3
        if "USER_NORMALIZE" not in streamlit.session_state:
            streamlit.session_state["USER_NORMALIZE"] = True
        if "USER_CAT_NAME" not in streamlit.session_state:
            streamlit.session_state[
                "USER_CAT_NAME"
            ] = ChromaticAdaptationTransforms.Bradford
        if "USER_COLORSPACE_NAME" not in streamlit.session_state:
            streamlit.session_state["USER_COLORSPACE_NAME"] = Colorspaces.sRGB

    @property
    def USER_TEMPERATURE(self) -> float:
        return streamlit.session_state["USER_TEMPERATURE"]

    @USER_TEMPERATURE.setter
    def USER_TEMPERATURE(self, new_value: float):
        streamlit.session_state["USER_TEMPERATURE"] = new_value

    @property
    def USER_DAYLIGHT_MODE(self) -> bool:
        return streamlit.session_state["USER_DAYLIGHT_MODE"]

    @USER_DAYLIGHT_MODE.setter
    def USER_DAYLIGHT_MODE(self, new_value: bool):
        streamlit.session_state["USER_DAYLIGHT_MODE"] = new_value

    @property
    def USER_TINT(self) -> float:
        return streamlit.session_state["USER_TINT"]

    @USER_TINT.setter
    def USER_TINT(self, new_value: float):
        streamlit.session_state["USER_TINT"] = new_value

    @property
    def USER_ILLUMINANT_NAME(self) -> Illuminants:
        return streamlit.session_state["USER_ILLUMINANT_NAME"]

    @USER_ILLUMINANT_NAME.setter
    def USER_ILLUMINANT_NAME(self, new_value: Illuminants):
        streamlit.session_state["USER_ILLUMINANT_NAME"] = new_value

    @property
    def USER_NDECIMALS(self) -> int:
        return streamlit.session_state["USER_NDECIMALS"]

    @USER_NDECIMALS.setter
    def USER_NDECIMALS(self, new_value: int):
        streamlit.session_state["USER_NDECIMALS"] = new_value

    @property
    def USER_NORMALIZE(self) -> bool:
        return streamlit.session_state["USER_NORMALIZE"]

    @USER_NORMALIZE.setter
    def USER_NORMALIZE(self, new_value: bool):
        streamlit.session_state["USER_NORMALIZE"] = new_value

    @property
    def USER_CAT_NAME(self) -> ChromaticAdaptationTransforms:
        return streamlit.session_state["USER_CAT_NAME"]

    @USER_CAT_NAME.setter
    def USER_CAT_NAME(self, new_value: ChromaticAdaptationTransforms):
        streamlit.session_state["USER_CAT_NAME"] = new_value

    @property
    def USER_COLORSPACE_NAME(self) -> Colorspaces:
        return streamlit.session_state["USER_COLORSPACE_NAME"]

    @USER_COLORSPACE_NAME.setter
    def USER_COLORSPACE_NAME(self, new_value: Colorspaces):
        streamlit.session_state["USER_COLORSPACE_NAME"] = new_value


def config() -> UserConfig:
    """
    Return a user configuration instance.
    """
    return UserConfig()
