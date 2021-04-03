import streamlit

import interface


streamlit.set_page_config(
    page_title="Temperature2RGB",
    page_icon=":thermometer:",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Sidebar

streamlit.sidebar.header(":gear: Settings")
user_result_mode = streamlit.sidebar.selectbox(
    label='Locus',
    options=[
        "Planckian",
        "Daylight"
    ],
    index=0,
    help="Planckian: pure incandescent black body | "
         "Daylight: same but viewed under daylight condition"
)

# Build rest of the interface

if user_result_mode == "Planckian":
    interface.planckian.ui()
elif user_result_mode == "Daylight":
    interface.daylight.ui()


#  App footer
"""
-------------------------------------------------------------------------------
"""

streamlit.markdown(
    "_Usage permitted for commercial purposes._\n\n"
    "_Made by [Liam Collod](https://www.artstation.com/monsieur_lixm) "
    "using [colour-science](https://www.colour-science.org/) librairy._\n\n"
    "_Contact: monsieurlixm@gmail.com_"
)
