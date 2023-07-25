import streamlit
import pandas

import streamlit_temperature2rgb
from streamlit_temperature2rgb._utils import widgetify
from streamlit_temperature2rgb.core import rgb_array_to_tuple
from streamlit_temperature2rgb.core import rgb_array_to_nuke
from streamlit_temperature2rgb.core import rgb_array_to_single_line
from streamlit_temperature2rgb.core import xy_array_to_tuple
from . import config
from ._sidebar import create_sidebar
from ._controller import ConversionResult


@widgetify
def widget_temperature_slider(key):
    config.USER_TEMPERATURE = streamlit.session_state[key]


@widgetify
def widget_temperature_box(key):
    config.USER_TEMPERATURE = streamlit.session_state[key]


@widgetify
def widget_colorspace_name(key):
    value = streamlit.session_state[key]
    print("widget_colorspace_name", value)
    config.USER_COLORSPACE_NAME = config.USER_COLORSPACE_NAME.from_label(value)


@widgetify
def widget_tint_slider(key):
    config.USER_TINT = streamlit.session_state[key]


@widgetify
def widget_tint_box(key):
    config.USER_TINT = streamlit.session_state[key]


def body_header():
    options = config.USER_COLORSPACE_NAME.labels()
    streamlit.selectbox(
        label="Target Colorspace Primaries",
        options=options,
        index=options.index(config.USER_COLORSPACE_NAME.as_label()),
        key=str(widget_colorspace_name),
        on_change=widget_colorspace_name,
    )

    value = config.USER_TEMPERATURE
    if config.USER_DAYLIGHT_MODE:
        min_value = 1667.0
        max_value = 10000.0
        value = max(min_value, config.USER_TEMPERATURE)
    else:
        min_value = 798.0  # Draper point
        max_value = 10000.0

    column1, column2, column3, column4 = streamlit.columns([0.25, 0.3, 0.2, 0.25])

    with column1:
        streamlit.number_input(
            label="Temperature (K)",
            min_value=min_value,
            max_value=max_value * 2,
            value=value,
            step=10.0,
            key=str(widget_temperature_box),
            on_change=widget_temperature_box,
        )

    with column2:
        streamlit.slider(
            label="Temperature Slider",
            min_value=min_value,
            max_value=max_value,
            value=value,
            step=10.0,
            key=str(widget_temperature_slider),
            on_change=widget_temperature_slider,
            label_visibility="hidden",
        )

    with column3:
        streamlit.number_input(
            label="Tint",
            min_value=-150.0,
            max_value=150.0,
            value=config.USER_TINT,
            step=1.0,
            key=str(widget_tint_box),
            on_change=widget_tint_box,
            disabled=config.USER_DAYLIGHT_MODE,
        )

    with column4:
        streamlit.slider(
            label="Tint Slider",
            min_value=-150.0,
            max_value=150.0,
            value=config.USER_TINT,
            step=1.0,
            help=(
                "How imperfect is this blackbody by biasing the colour along the "
                "ISO temperature lines where >0.0 add Green and <0.0 add Magenta"
            ),
            key=str(widget_tint_slider),
            on_change=widget_tint_slider,
            disabled=config.USER_DAYLIGHT_MODE,
            label_visibility="hidden",
        )


def body_display(result: ConversionResult):
    streamlit.subheader("Result")

    if (
        config.USER_TEMPERATURE < 1900
        and config.USER_COLORSPACE_NAME == config.USER_COLORSPACE_NAME.sRGB
    ):
        streamlit.warning(
            "The lowest representable color temperature by the sRGB "
            "colorspace being 1900K, the result you are seeing is clamped."
        )

    streamlit.caption("sRGB preview with 2.2 power function")
    streamlit.image(
        image=result.get_preview_image(1000, 190),
        caption="",  # "sRGB preview with 2.2 power function",
        clamp=True,
    )
    column1, column2, column3 = streamlit.columns(3)

    with column1:
        streamlit.code(
            rgb_array_to_tuple(result.get_rgb_array(), config.USER_NDECIMALS),
            language="text",
        )
        streamlit.caption("⬆ RGB tuple style")

    with column2:
        streamlit.code(
            rgb_array_to_single_line(result.get_rgb_array(), config.USER_NDECIMALS),
            language="text",
        )
        streamlit.caption("⬆ RGBA Katana style")

    with column3:
        streamlit.code(
            xy_array_to_tuple(result.get_xy_array(), config.USER_NDECIMALS),
            language="text",
        )
        streamlit.caption("⬆ CIE xy chromaticity coordinates")

    with streamlit.expander("As Nuke Node"):
        streamlit.code(
            rgb_array_to_nuke(
                result.get_rgb_array(),
                config.USER_NDECIMALS,
                node_name=result.get_nuke_node_name(),
                node_label=result.get_nuke_node_label(),
            ),
            language="text",
        )

    figure, axes = result.get_cct_plot()
    streamlit.pyplot(figure)


def body_footer():
    streamlit.markdown("---")
    streamlit.header(":book: Learning")

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
        ("10637K (Planckian)", "Bluest sky in the world.(Brazil) [2]"),
        ("15,000-27,000K", "Clear blue poleward sky "),
    ]
    dataframe = pandas.DataFrame(table_data, columns=["Temperature", "Source"])
    streamlit.table(dataframe)
    streamlit.header("References")
    streamlit.markdown(
        "- [1] https://en.wikipedia.org/wiki/Color_temperature\n"
        "- [2] http://web.archive.org/web/20160728054241/http://www.npl.co.uk/content/ConWebDoc/1053\n"
    )

    streamlit.header("About")

    streamlit.caption(
        "![GitHub last commit (branch)](https://img.shields.io/github/last-commit/MrLixm/Streamlit_Temperature2RGB/main?label=last%20updated) "
        f"![Static Badge](https://img.shields.io/badge/version-{streamlit_temperature2rgb.__version__}-lightgrey) "
        f"![GitHub Repo stars](https://img.shields.io/github/stars/MrLixm/Streamlit_Temperature2RGB?logo=github)"
    )
    streamlit.caption(
        "Made by [Liam Collod](https://mrlixm.github.io/) "
        "using [colour-science](https://www.colour-science.org/) librairy --"
        "Usage permitted for commercial purposes."
    )


def create_main_interface():
    with streamlit.sidebar:
        create_sidebar()
    streamlit.title("Temperature to RGB color.".upper())
    body_header()
    result = ConversionResult.from_active_context()
    body_display(result=result)
    body_footer()
