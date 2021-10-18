import requests

from PIL import Image
from io import BytesIO
import streamlit as st

from streamlit_app.navigation_radios import Introduction
from streamlit_app.navigation_manager.navigation_manager import NavigationManager

TSDS_ICON_URL = "https://raw.githubusercontent.com/thatscotdatasci/thatscotdatasci.github.io/master/assets/icons/tsds.ico"

# Get the TSDS icon
tsds_icon_data = requests.get(TSDS_ICON_URL)
tsds_icon = Image.open(BytesIO(tsds_icon_data.content))

# Set the page configuration
st.set_page_config(
    page_title="L48 Machine Learning and the Physical World",
    page_icon=tsds_icon,
    initial_sidebar_state="expanded",
    layout="wide"
)

# Display the TSDS logo in the sidebar
st.sidebar.image(tsds_icon)

# App title in sidebar
st.sidebar.markdown("""
# L48 Machine Learning and the Physical World

Labs from the [L48 Machine Learning and the Physical World](https://mlatcl.github.io/mlphysical/) course at the University of Cambridge.

Click on the radio buttons below to view different examples.
""")

# Instantiate navigation radio options
navigation_radio_options = (Introduction, )

# Content manager
content_manager = NavigationManager(navigation_radio_options, Introduction)