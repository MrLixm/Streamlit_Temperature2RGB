import streamlit

from streamlit_temperature2rgb._utils import widgetify
from streamlit_temperature2rgb.ui import config


@widgetify
def widget_locus(key):
    config().USER_DAYLIGHT_MODE = streamlit.session_state[key] == "Daylight"


@widgetify
def widget_illuminant(key):
    value = streamlit.session_state[key]
    config().USER_ILLUMINANT_NAME = config().USER_ILLUMINANT_NAME.from_label(value)


@widgetify
def widget_ndecimals(key):
    config().USER_NDECIMALS = streamlit.session_state[key]


@widgetify
def widget_normalize(key):
    config().USER_NORMALIZE = streamlit.session_state[key]


@widgetify
def widget_cat_name(key):
    value = streamlit.session_state[key]
    config().USER_CAT_NAME = config().USER_CAT_NAME.from_label(value)


def create_sidebar():
    streamlit.header("Settings".upper())

    streamlit.selectbox(
        label="Locus",
        options=["Planckian", "Daylight"],
        index=int(config().USER_DAYLIGHT_MODE),
        help=(
            "- Planckian: pure incandescent black body\n"
            "- Daylight: same but viewed under daylight condition"
        ),
        key=str(widget_locus),
        on_change=widget_locus,
    )
    options = config().USER_ILLUMINANT_NAME.labels()
    streamlit.selectbox(
        label="Target Illuminant",
        options=options,
        index=options.index(config().USER_ILLUMINANT_NAME.as_label()),
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
    options = config().USER_CAT_NAME.labels()
    streamlit.selectbox(
        label="Chromatic Adaptation Transform",
        options=options,
        index=options.index(config().USER_CAT_NAME.as_label()),
        help="(C.A.T.) for whitepoint conversion.",
        key=str(widget_cat_name),
        on_change=widget_cat_name,
    )
