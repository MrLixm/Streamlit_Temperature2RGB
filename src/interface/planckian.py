import numpy
import streamlit

import constants
import core


def ui():

    streamlit.title(
        "Planckian Black-body Temperature to RGB Colorspaces conversion")

    user_temperature = streamlit.sidebar.number_input(
        label="Source Temperature in Kelvin (K)",
        min_value=1000,
        max_value=25000,
        value=6500,
        step=10
    )

    user_temperature = streamlit.sidebar.slider(
        label="Source Temperature in Kelvin (K)",
        min_value=1000,
        max_value=25000,
        value=user_temperature,
        step=10
    )

    user_colorspace = streamlit.sidebar.selectbox(
        label='Target Colorspace primaries',
        options=constants.COLORSPACES_NAMES,
        index=0
    )

    user_tint = streamlit.sidebar.slider(
        label="Tint",
        min_value=-100.0,
        max_value=100.0,
        value=0.0,
        step=0.01,
        help="Skew the result along the iso-temperature lines. "
             "Basicaly add Green(+)/Magenta(-)"
    )
    user_tint = user_tint / 1000 / 2

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

    # Processing:
    if user_illuminant == constants.ILLUMINANTS_NAMES[0]:
        user_illuminant = None

    if user_temperature < 1900 and user_colorspace == "sRGB":
        streamlit.warning(
            "The lowest representable color temperature by the sRGB "
            "colorspace being 1900K the current result is clamped.")

    rgb_result = core.cct_to_rgb_colorspace_planckian(
        user_temperature,
        user_colorspace,
        tint=user_tint,
        illuminant=user_illuminant,
        normalize=user_normalize
    )
    display_object = core.utils.Numpy2String(rgb_result,
                                             user_ndecimals)

    # Calculate the image preview
    if user_normalize:
        if user_colorspace == "sRGB":
            rgb_preview = rgb_result
        else:
            rgb_preview = core.cct_to_rgb_colorspace_planckian(
                user_temperature,
                "sRGB",
                tint=user_tint,
                illuminant=user_illuminant,
                normalize=True
            )
    else:
        rgb_preview = core.cct_to_rgb_colorspace_planckian(
            user_temperature,
            "sRGB",
            tint=user_tint,
            illuminant=user_illuminant,
            normalize=True
        )

    # apply the 2.2 power function as transfer function and convert to 8bit
    rgb_preview = (rgb_preview ** 2.2 * 255).astype(numpy.uint8)
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
        display_object.nuke(
            node_name=f"Temperature_{user_temperature}K_{user_colorspace}"),
        language="text"
    )

    return
