import colour
import numpy
import streamlit

import constants
import core


def ui():

    streamlit.title(
        "Planckian Black-body Temperature to RGB Colorspaces conversion")

    user_slider = streamlit.sidebar.checkbox(
        label="Use Sliders",
        value=False,
    )
    if user_slider:
        input_widget = streamlit.sidebar.slider
    else:
        input_widget = streamlit.sidebar.number_input

    user_temperature = input_widget(
        label="Source Temperature in Kelvin (K)",
        min_value=1000,
        max_value=25000,
        value=6500,
        step=10
    )

    user_colorspace = streamlit.sidebar.selectbox(
        label='Target Colorspace primaries',
        options=list(constants.COLORSPACES_NAMES.keys()),
        index=0
    )

    user_tint = input_widget(
        label="Tint",
        min_value=-150.0,
        max_value=150.0,
        value=0.0,
        step=0.01,
        help="How imperfect is this blackbody by biasing the colour along the"
             " ISO temperature lines \n"
             "Basicaly + add Green; - add Magenta"
    )

    # Advanced Options
    with streamlit.sidebar.beta_expander(label="Advanced Options"):
        user_illuminant = streamlit.selectbox(
            label='Target Illuminant',
            options=constants.ILLUMINANTS_NAMES,
            index=0,
            help="Illuminant from the CIE 1931 2 Degree Standard Observer"
        )
        user_ndecimals = streamlit.number_input(
            label="Number of decimals",
            min_value=1,
            max_value=9,
            value=3,
            step=1
        )
        user_normalize = streamlit.checkbox(
            label="Normalize values",
            value=True,
            help="Normalize values into the 0-1 range."
        )
        user_CAT = streamlit.selectbox(
            label='Chromatic Adaptation Transform',
            options=constants.CAT_NAMES,
            index=0,
            help="CAT, default is Bradford."
        )

    # User input operations:

    user_tint_interface = user_tint
    user_tint = user_tint / 3000
    user_colorspace = constants.COLORSPACES_NAMES[user_colorspace]

    if user_illuminant == constants.ILLUMINANTS_NAMES[0]:
        user_illuminant = None

    if user_temperature < 1900 and user_colorspace == "sRGB":
        streamlit.warning(
            "The lowest representable color temperature_object by the sRGB "
            "colorspace being 1900K the current result is clamped.")

    # Processing
    temperature_obj = core.TemperatureObject(CCT=user_temperature,
                                             tint=user_tint).planckian

    rgb_result = temperature_obj.rgb(
            primaries=user_colorspace,
            illuminant=user_illuminant,
            CAT=user_CAT
    )

    display_object = core.utils.RGBarray2String(
        numpy_ndarray=rgb_result.value(normalized=user_normalize),
        ndecimals=user_ndecimals
    )

    rgb_preview = temperature_obj.rgb(
        "sRGB",
        illuminant=user_illuminant,
        CAT=user_CAT
        ).value(normalized=True)

    # apply the 2.2 power function as transfer function and convert to 8bit
    rgb_preview = (rgb_preview ** (1/2.2) * 255).astype(numpy.uint8)
    print(rgb_preview)
    image_temp_preview = numpy.full(
        (100, 2048, 3), rgb_preview, dtype=numpy.uint8)

    # -------------------------------------------------------------------------
    # Displaying Results:

    streamlit.header(
        f":thermometer: Results for {user_temperature}K and "
        f"{user_colorspace} primaries ")

    streamlit.image(
        image=image_temp_preview,
        caption="sRGB preview with 2.2 power function",
        clamp=True
    )

    streamlit.code(display_object.linebreak, language="text")

    streamlit.text("Single line with alpha (float4):")
    streamlit.code(display_object.singleline, language="text")

    streamlit.text("Nuke node:")
    streamlit.code(
        body=display_object.nuke(
            node_name=f"Planckian_{user_temperature}K_{user_colorspace}"
                      f"_{user_tint_interface}"),
        language="text"
    )

    streamlit.text("CIE xy chromaticity coordinates:")
    streamlit.code(
        body=core.utils.CIExy2String(temperature_obj.xy,
                                     ndecimals=user_ndecimals).tuple,
        language="text"
    )

    return
