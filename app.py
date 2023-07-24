import streamlit
import streamlit_temperature2rgb

streamlit.set_page_config(
    page_title="Temperature2RGB",
    page_icon=":thermometer:",
    layout="centered",
    initial_sidebar_state="expanded",
)

streamlit_temperature2rgb.create_main_interface()
