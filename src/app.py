import sys
from pathlib import Path

import colour.utilities
import streamlit

THIS_DIR = Path(__file__).parent
if str(THIS_DIR) not in sys.path:
    sys.path.append(str(THIS_DIR))

import streamlit_temperature2rgb

streamlit.set_page_config(
    page_title="Temperature2RGB",
    page_icon=":thermometer:",
    layout="centered",
    initial_sidebar_state="expanded",
)

colour.utilities.filter_warnings(colour_usage_warnings=True, python_warnings=True)
# we create a first instance of the config at startup
streamlit_temperature2rgb.ui.config(force_instance=True)
streamlit_temperature2rgb.create_main_interface()
