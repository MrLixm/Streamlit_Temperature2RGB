import colour.utilities
import streamlit
import streamlit_temperature2rgb

streamlit.set_page_config(
    page_title="Temperature2RGB",
    page_icon=":thermometer:",
    layout="centered",
    initial_sidebar_state="expanded",
)

colour.utilities.filter_warnings(colour_usage_warnings=True, python_warnings=True)
streamlit_temperature2rgb.create_main_interface()
