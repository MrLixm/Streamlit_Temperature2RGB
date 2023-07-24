import streamlit
import pandas

import streamlit_temperature2rgb.interface

streamlit.set_page_config(
    page_title="Temperature2RGB",
    page_icon=":thermometer:",
    layout="centered",
    initial_sidebar_state="expanded",
)


streamlit.title("Temperature to RGB color.".upper())

with streamlit.sidebar:
    streamlit.header("Settings".upper())
    user_locus = streamlit.selectbox(
        label="Locus",
        options=["Planckian", "Daylight"],
        index=0,
        help=(
            "- Planckian: pure incandescent black body\n"
            "- Daylight: same but viewed under daylight condition"
        ),
    )


# Build rest of the interface

if user_locus == "Planckian":
    streamlit_temperature2rgb.interface.planckian.ui()
elif user_locus == "Daylight":
    streamlit_temperature2rgb.interface.daylight.ui()


streamlit.subheader(":book: Learning")


streamlit.markdown(
    """
[Planckian Locus](https://en.wikipedia.org/wiki/Planckian_locus): path of the
color of the light emitted by a pure incandescent black-body.

**Daylight Locus**:  path of the color of the light emitted by a pure 
incandescent black-body under Daylight viewing conditions. 
Exemples: the sky, the sun, ... Defined from 4000K to 25000K

Depending on where you want to use this temperature, your source might not be
a pure black-body radiator (probably never) and further more , 
being affected by viewing conditions (ex: the sun by the atmosphere).
Using the Daylight Locus or the tint parameter on the Planckian locus might
help you achieve the right colour for your source. 
"""
)

table_data = [
    ("1700K", "Match flame, low pressure sodium lamps."),
    ("1850K", "Candle flame, sunset/sunrise "),
    ("2400K", "Standard incandescent lamps  "),
    ("2550K", "Soft white incandescent lamps "),
    ("2700K", "'Soft white' compact fluorescent and LED lamps "),
    ("3000K", "Warm white compact fluorescent and LED lamps  "),
    (
        "5000K",
        "Horizon daylight, cool white/daylight compact fluorescent lamps (CFL)",
    ),
    ("5900K", "Sunlight above the atmosphere (Space)"),
    ("6500K", "Daylight, overcast"),
    ("6500-9500K", "LCD or CRT screen "),
    ("10637K (Planckian)", "Bluest sky in the world.(Brazil)"),
    ("15,000-27,000K", "Clear blue poleward sky "),
]
dataframe = pandas.DataFrame(table_data, columns=["Temperature", "Source"])
streamlit.table(dataframe)
streamlit.subheader("References")
streamlit.markdown(
    "- [1] https://en.wikipedia.org/wiki/Color_temperature\n"
    "- [2] http://web.archive.org/web/20080517201411\n"
    "- [3] http://www.npl.co.uk/blueskies/"
)


streamlit.subheader("About")


streamlit.caption(
    "version `0.1.0` "
    "-- last-updated: `TODO` "
    "-- Made by [Liam Collod](https://mrlixm.github.io/)"
    "using [colour-science](https://www.colour-science.org/) librairy."
)
streamlit.caption("Usage permitted for commercial purposes.")
