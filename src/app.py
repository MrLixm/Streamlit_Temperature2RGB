import streamlit

import Temperature2RGB as api

#  ---------------------------------------------------------------------------
# Constants

app_title = "Black-body Temperatures (Kelvin) to RGB Colorspaces conversion"

colorspace_suggestions = [
    "sRGB",
    "ACEScg",
    "Adobe Wide Gamut RGB",
    "P3-D65",
    "ITU-R BT.2020"
]

illuminants_suggestions = [
    "Colorspace's one",  # has to be at index 0 (=None)
    'D50',
    'D55',
    'D60',
    'D65',
    'D75',
    'E',
]

#  ---------------------------------------------------------------------------
# Widgets

streamlit.title(app_title)

streamlit.sidebar.header(":gear: Settings")


user_temperature = streamlit.sidebar.number_input(
    label="Source Temperature in Kelvin (K)",
    min_value=1000,
    max_value=15000,
    value=6500,
    step=10
)

user_temperature = streamlit.sidebar.slider(
    label="Source Temperature in Kelvin (K)",
    min_value=1000,
    max_value=15000,
    value=user_temperature,
    step=10
)


user_colorspace = streamlit.sidebar.selectbox(
    label='Target Colorspace primaries',
    options=colorspace_suggestions,
    index=0
)

# Advanced Options
with streamlit.sidebar.beta_expander(label="Advanced Options"):
    user_illuminant = streamlit.selectbox(
        label='Target Illuminant',
        options=illuminants_suggestions,
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
if user_illuminant == illuminants_suggestions[0]:
    user_illuminant = None

if user_temperature < 1900 and user_colorspace == "sRGB":
    streamlit.warning("The lowest representable color temperature by the "
                      "sRGB colorspace being 1900K the current result is not"
                      " accurate.")

rgb_result = api.temperature_to_RGB(
    user_temperature,
    user_colorspace,
    illuminants=user_illuminant,
    clip=user_normalize
)
display_object = api.resultFormatting.Numpy2String(rgb_result, user_ndecimals)

# ---------------------------------------------------------------------------
# Displaying Results:

streamlit.header(
    f":thermometer: Results for {user_temperature}K and "
    f"{user_colorspace} primaries ")
streamlit.code(display_object.linebreak, language="text")
streamlit.text("Single line with alpha (float4):")
streamlit.code(display_object.singleline, language="text")
streamlit.text("Nuke node:")
streamlit.code(
    display_object.nuke(
        node_name=f"Temperature_{user_temperature}K_{user_colorspace}"),
    language="text"
)


"""
---
"""
streamlit.markdown(
    "_Usage permitted for commercial utilisation._"
)

streamlit.markdown(
    "_Made by [Liam Collod](https://www.artstation.com/monsieur_lixm) "
    "using [colour-science](https://www.colour-science.org/) librairy._"
)
streamlit.markdown(
    "_Contact: monsieurlixm@gmail.com_"
)