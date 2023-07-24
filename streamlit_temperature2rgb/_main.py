import colour
import streamlit
import pandas

import streamlit_temperature2rgb.core
from streamlit_temperature2rgb import config
from streamlit_temperature2rgb._utils import widgetify


@widgetify
def widget_temperature_slider(key):
    config.USER_TEMPERATURE = streamlit.session_state[key]


@widgetify
def widget_temperature_box(key):
    config.USER_TEMPERATURE = streamlit.session_state[key]


@widgetify
def widget_locus(key):
    config.USER_DAYLIGHT_MODE = streamlit.session_state[key] == "Daylight"


@widgetify
def widget_illuminant(key):
    value = streamlit.session_state[key]
    config.USER_ILLUMINANT_NAME = config.USER_ILLUMINANT_NAME.from_label(value)


@widgetify
def widget_ndecimals(key):
    config.USER_NDECIMALS = streamlit.session_state[key]


@widgetify
def widget_normalize(key):
    config.USER_NORMALIZE = streamlit.session_state[key]


@widgetify
def widget_cat_name(key):
    value = streamlit.session_state[key]
    config.USER_CAT_NAME = config.USER_CAT_NAME.from_label(value)


@widgetify
def widget_colorspace_name(key):
    value = streamlit.session_state[key]
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

        if not config.USER_DAYLIGHT_MODE:
            streamlit.number_input(
                label="Tint",
                min_value=-150.0,
                max_value=150.0,
                value=config.USER_TINT,
                step=1.0,
                key=str(widget_tint_box),
                on_change=widget_tint_box,
            )

    with column2:
        streamlit.slider(
            label="",
            min_value=min_value,
            max_value=max_value,
            value=value,
            step=10.0,
            key=str(widget_temperature_slider),
            on_change=widget_temperature_slider,
        )

        if not config.USER_DAYLIGHT_MODE:
            streamlit.slider(
                label="",
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
            )


def body_display():
    if (
        config.USER_TEMPERATURE < 1900
        and config.USER_COLORSPACE_NAME == config.USER_COLORSPACE_NAME.sRGB
    ):
        streamlit.warning(
            "The lowest representable color temperature by the sRGB "
            "colorspace being 1900K, the result you are seeing is clamped."
        )

    colorspace = config.USER_COLORSPACE_NAME.as_core()
    colorspace: colour.RGB_Colourspace = colour.RGB_COLOURSPACES[colorspace]

    whitepoint = config.USER_ILLUMINANT_NAME.as_core()
    if whitepoint is None:
        whitepoint = colorspace.whitepoint
    else:
        whitepoint = colour.CCS_ILLUMINANTS["CIE 1931 2 Degree Standard Observer"]
        whitepoint = whitepoint[whitepoint]

    tint = config.USER_TINT / 3000

    if config.USER_DAYLIGHT_MODE:
        conversion = streamlit_temperature2rgb.core.DaylightCCTConversion(
            CCT=config.USER_TEMPERATURE,
            colorspace=colorspace,
            illuminant=whitepoint,
            cat=config.USER_CAT_NAME.as_core(),
        )
    else:
        conversion = streamlit_temperature2rgb.core.PlanckianCCTConversion(
            CCT=config.USER_TEMPERATURE,
            colorspace=colorspace,
            illuminant=whitepoint,
            cat=config.USER_CAT_NAME.as_core(),
            tint=tint,
        )

    column1, column2 = streamlit.columns(2)

    # IMAGE PREVIEW

    if config.USER_COLORSPACE_NAME == config.USER_COLORSPACE_NAME.sRGB:
        conversion_preview = conversion
    else:
        conversion_preview = conversion.with_colorspace(colour.RGB_COLOURSPACES["sRGB"])

    image_preview_array = conversion_preview.rgb
    image_preview_array = colour.algebra.normalise_maximum(
        image_preview_array, clip=True
    )
    image_preview_array = streamlit_temperature2rgb.core.rgb_array_to_image(
        image_preview_array, width=500, height=400
    )

    with column1:
        streamlit.image(
            image=image_preview_array,
            caption="sRGB preview with 2.2 power function",
            clamp=True,
        )

    # R-G-B values display

    result_rgb_array = conversion.rgb
    if config.USER_NORMALIZE:
        result_rgb_array = colour.algebra.normalise_maximum(result_rgb_array, clip=True)

    with column2:
        streamlit.code(
            streamlit_temperature2rgb.core.rgb_array_to_multi_line(
                result_rgb_array, config.USER_NDECIMALS
            ),
            language="text",
        )

        streamlit.code(
            streamlit_temperature2rgb.core.rgb_array_to_single_line(
                result_rgb_array, config.USER_NDECIMALS
            ),
            language="text",
        )

        streamlit.code(
            streamlit_temperature2rgb.core.xy_array_to_tuple(
                conversion.xy, config.USER_NDECIMALS
            ),
            language="text",
        )
        streamlit.caption("⬆ CIE xy chromaticity coordinates")

    if config.USER_DAYLIGHT_MODE:
        nuke_node_name = f"Daylight_{config.USER_TEMPERATURE}K_{config.USER_COLORSPACE_NAME.as_label()}"
    else:
        nuke_node_name = f"Planckian_{config.USER_TEMPERATURE}K_{config.USER_COLORSPACE_NAME.as_label()}_{config.USER_TINT}"

    streamlit.code(
        streamlit_temperature2rgb.core.rgb_array_to_nuke(
            result_rgb_array, config.USER_NDECIMALS, node_name=nuke_node_name
        ),
        language="text",
    )
    streamlit.caption("⬆ Nuke node")


def body_footer():
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


def sidebar():
    streamlit.header("Settings".upper())

    streamlit.selectbox(
        label="Locus",
        options=["Planckian", "Daylight"],
        index=int(config.USER_DAYLIGHT_MODE),
        help=(
            "- Planckian: pure incandescent black body\n"
            "- Daylight: same but viewed under daylight condition"
        ),
        key=str(widget_locus),
        on_change=widget_locus,
    )
    options = config.USER_ILLUMINANT_NAME.labels()
    streamlit.selectbox(
        label="Target Illuminant",
        options=options,
        index=options.index(config.USER_ILLUMINANT_NAME.as_label()),
        help="Illuminant from the CIE 1931 2 Degree Standard Observer",
        key=str(widget_illuminant),
        on_change=widget_illuminant,
    )
    streamlit.number_input(
        label="Number of decimals",
        min_value=1,
        max_value=9,
        value=3,
        step=1,
        key=str(widget_ndecimals),
        on_change=widget_ndecimals,
    )
    streamlit.checkbox(
        label="Normalize values",
        value=True,
        help="Remap values into the 0.0-1.0 range.",
        key=str(widget_normalize),
        on_change=widget_normalize,
    )
    options = config.USER_CAT_NAME.labels()
    streamlit.selectbox(
        label="Chromatic Adaptation Transform",
        options=options,
        index=options.index(config.USER_CAT_NAME.as_label()),
        help="(C.A.T.) for whitepoint conversion.",
        key=str(widget_cat_name),
        on_change=widget_cat_name,
    )


def create_main_interface():
    with streamlit.sidebar:
        sidebar()
    streamlit.title("Temperature to RGB color.".upper())
    body_header()
    body_display()
    body_footer()
