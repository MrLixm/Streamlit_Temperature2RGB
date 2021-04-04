import pandas
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

streamlit.subheader(":book: Learning")


streamlit.markdown("""
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

""")

table_data = [
    ("1700K", "Match flame, low pressure sodium lamps."),
    ("1850K", "Candle flame, sunset/sunrise "),
    ("2400K", "Standard incandescent lamps  "),
    ("2550K", "Soft white incandescent lamps "),
    ("2700K", "'Soft white' compact fluorescent and LED lamps "),
    ("3000K", "Warm white compact fluorescent and LED lamps  "),
    ("5000K", ("Horizon daylight, cool white / daylight compact fluorescent "
               "lamps (CFL)")),
    ("6500K", "Daylight, overcast"),
    ("6500-9500K", "LCD or CRT screen "),
    ("15,000-27,000K", "Clear blue poleward sky "),
]
dataframe = pandas.DataFrame(table_data,
                             columns=("Temperature", "Source"))
streamlit.table(dataframe)
streamlit.write("Source: https://en.wikipedia.org/wiki/Color_temperature")