from ._utils import UifiedEnum


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


USER_TEMPERATURE = 2500.0
USER_DAYLIGHT_MODE = False
USER_TINT = 0.0
USER_ILLUMINANT_NAME: Illuminants = Illuminants.colorspace
USER_NDECIMALS = 3
USER_NORMALIZE = True
USER_CAT_NAME: ChromaticAdaptationTransforms = ChromaticAdaptationTransforms.Bradford
USER_COLORSPACE_NAME: Colorspaces = Colorspaces.sRGB
