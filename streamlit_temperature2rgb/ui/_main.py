import streamlit
import pandas

from streamlit_temperature2rgb._utils import widgetify
from streamlit_temperature2rgb.core import rgb_array_to_multi_line
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
        min_value = 1000.0
        max_value = 25000.0
        value = max(min_value, config.USER_TEMPERATURE)
    else:
        min_value = 10.0
        max_value = 50000.0

    column1, column2 = streamlit.columns([0.25, 0.75])

    with column1:
        streamlit.number_input(
            label="Temperature in Kelvin (K)",
            min_value=min_value,
            max_value=max_value,
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

    column1, column2 = streamlit.columns([0.25, 0.75])

    with column1:
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

    with column2:
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
    if (
        config.USER_TEMPERATURE < 1900
        and config.USER_COLORSPACE_NAME == config.USER_COLORSPACE_NAME.sRGB
    ):
        streamlit.warning(
            "The lowest representable color temperature by the sRGB "
            "colorspace being 1900K, the result you are seeing is clamped."
        )

    column1, column2 = streamlit.columns(2)

    with column1:
        streamlit.image(
            image=result.get_preview_image(400, 285),
            caption="sRGB preview with 2.2 power function",
            clamp=True,
        )

    with column2:
        streamlit.code(
            rgb_array_to_multi_line(result.get_rgb_array(), config.USER_NDECIMALS),
            language="text",
        )

        streamlit.code(
            rgb_array_to_single_line(result.get_rgb_array(), config.USER_NDECIMALS),
            language="text",
        )

        streamlit.code(
            xy_array_to_tuple(result.get_xy_array(), config.USER_NDECIMALS),
            language="text",
        )
        streamlit.caption("⬆ CIE xy chromaticity coordinates")

    streamlit.code(
        rgb_array_to_nuke(
            result.get_rgb_array(),
            config.USER_NDECIMALS,
            node_name=result.get_nuke_node_name(),
        ),
        language="text",
    )
    streamlit.caption("⬆ Nuke node")


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
        ("10637K (Planckian)", "Bluest sky in the world.(Brazil)"),
        ("15,000-27,000K", "Clear blue poleward sky "),
    ]
    dataframe = pandas.DataFrame(table_data, columns=["Temperature", "Source"])
    streamlit.table(dataframe)
    streamlit.header("References")
    streamlit.markdown(
        "- [1] https://en.wikipedia.org/wiki/Color_temperature\n"
        "- [2] http://web.archive.org/web/20080517201411\n"
        "- [3] http://www.npl.co.uk/blueskies/"
    )

    streamlit.header("About")

    streamlit.caption(
        "version `0.1.0` "
        "-- last-updated: `TODO` "
        "-- Made by [Liam Collod](https://mrlixm.github.io/) "
        "using [colour-science](https://www.colour-science.org/) librairy."
    )
    streamlit.caption("Usage permitted for commercial purposes.")


def create_main_interface():
    with streamlit.sidebar:
        create_sidebar()
    streamlit.title("Temperature to RGB color.".upper())
    body_header()
    result = ConversionResult.from_active_context()
    body_display(result=result)
    body_footer()
