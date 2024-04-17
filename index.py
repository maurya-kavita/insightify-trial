import streamlit as st
import os
from scrap import my_logic
from visualization import visualize_data
from model import suggestion
from urllib.parse import urlparse, parse_qs
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Insightify", page_icon="📊")

page_bg_img = f"""<style> [data-testid="stAppViewContainer"] > .main {{ background-image: linear-gradient(rgba(0, 0, 0, 0.1), rgba(0, 0, 0, 0.1)), url("https://img.freepik.com/free-photo/vivid-blurred-colorful-background_58702-2655.jpg?t=st=1710070208~exp=1710073808~hmac=b36754fe44b1ef312651e415c5f1b3e81b3f7f20a2e7d6483c97e1b95b32632a&w=1800"); background-size: auto; background-attachment: local;; }} [data-testid="stSidebar"] > div:first-child {{ background-image: url("https://img.freepik.com/free-vector/gray-curve-frame-template-vector_53876-165854.jpg?t=st=1710078496~exp=1710082096~hmac=f1862be94ae1a6f132d74d0ee787b31a434f4b0bda1b4422f9dd0b263de5da6f&w=360");  background-size: cover; }} </style> """
st.markdown(page_bg_img, unsafe_allow_html=True)
hide_st_style = """<style>#MainMenu {visibility: hidden;}footer {visibility: hidden;}header {visibility: hidden;}</style>"""
st.markdown(hide_st_style, unsafe_allow_html=True)


def main():
    # Check if 'submit_count' and 'scrap_clicked' are in the session state
    if 'submit_count' not in st.session_state:
        st.session_state['submit_count'] = 0
    if 'scrap_clicked' not in st.session_state:
        st.session_state['scrap_clicked'] = False

    # with st.sidebar:
        # Sidebar menu
    menu_selection = option_menu(
        menu_title=None,
        menu_icon="cast",
        options=["Scrap Data", "Visualization", "Recommendation"],
        icons=["search", "bar-chart", "lightbulb"],
        default_index=0,
        orientation="horizontal",
        styles= { 
            "container": {
                # " background-image": "url(https://img.freepik.com/free-vector/gray-curve-frame-template-vector_53876-165854.jpg?t=st=1710078496~exp=1710082096~hmac=f1862be94ae1a6f132d74d0ee787b31a434f4b0bda1b4422f9dd0b263de5da6f&w=360)",
                # "background-position": "center",
                # "background-color": "grey",
                "border-radius": "0!important",
                "padding": "0!important",
                "background-size": "fill",
            },
            "icon": {"color": "orange", "font-size": "16px"},
            "nav-link": {
                "padding": "12px 24px !important",
                "border-radius": "0!important",
                "margin": "0!important",
                "font-size": "16px",
                "text-align": "center",  # Center-align text
                "--hover-color": "#E5E4E2", 
                "transition": "background-color 0.3s",  # Smooth transition on hover
            },
            "nav-link-selected": {
                "background-color": "#222f3e",
                "color": "white",  # White text for selected item
            },
            
        }
       
    )

    if menu_selection == "Scrap Data":
        st.markdown("<h1 style='color: #131921;'>INSIGHTIFY</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='font-size: 24px; color: #222f3e;'>Our app fetches data from Amazon,  visualizes the result and recommend the best product using customer ratings.  </h2>", unsafe_allow_html=True)
        st.write("")
        st.write("")
        st.write("")
        st.markdown("<h2 style='font-size: 20px; color: #222f3e3;'>Enter the URL of the product:</h2>", unsafe_allow_html=True)
        url = st.text_input("", placeholder="https://www.amazon.in/")
        parsed_url = urlparse(url)
        url_params = parse_qs(parsed_url.query)
        st.write("")
        st.write( """ <style> .stButton button { background-color: #222f3e; color: white; border: none; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; cursor: pointer; } </style> """, unsafe_allow_html=True )
        submit_button = st.button("Scrap Data", help="Click here to scrap data")
        if submit_button:
            if len(url_params) > 0 and "amazon.in" in url:
                my_logic(url)
                st.session_state['submit_count'] += 1  # Increment submit count
                st.session_state['scrap_clicked'] = True  # Set scrap_clicked to True
            elif len(url) == 0:
                st.markdown("<h3 style='color: #922724;'>Please enter product URL!!!</h3>", unsafe_allow_html=True)
            else:
                st.markdown("<h3 style='color: #922724;'>Please enter a valid URL!!!</h3>", unsafe_allow_html=True)
        

    elif menu_selection == "Visualization":
        st.markdown("<h1 style='color: #131921;'>Visualization Page</h1>", unsafe_allow_html=True)
        if st.session_state['submit_count'] == 0:
            st.write("")
            st.write("")
            st.markdown("<h4 style='color: #922724;'>Please scrap data first!!!</h4>", unsafe_allow_html=True)
        elif st.session_state['submit_count'] == 1:
            visualize_data()
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            col1, col2 = st.columns(2)
            st.write( """ <style> .stButton button { background-color: #222f3e; color: white; border: none; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; cursor: pointer; } </style> """, unsafe_allow_html=True )
            with col1:
                compare_button = st.button("Compare Between Two Products", help="Click here to scrap data again!", use_container_width=True)
                if compare_button:
                    st.session_state['compare_clicked'] = True
                    st.markdown("<h4 style='color: #22733D;'>Please scrap data again!</h4>", unsafe_allow_html=True)
            with col2:
                exit_button = st.button("Exit the application", help="Click here to exit", use_container_width=True)
                if exit_button:
                    if os.path.exists('append.csv'):
                        os.remove('append.csv')
                    st.markdown("<h4 style='color: #922724;'>Thank you for using our app! &#128522;</h4>", unsafe_allow_html=True)
        elif st.session_state['submit_count'] == 2:
            visualize_data()
            st.write("")
            st.write("")
            st.markdown("<h3 style='color: #22733D;'>Thank you for using the visualization dashboard!</h3>", unsafe_allow_html=True)
            st.write("")
            st.markdown("<h5 style='color: #22733D;'>Find the best product using Product Recommender</h5>", unsafe_allow_html=True)
            st.write("")
            st.write("")
            st.write( """ <style> .stButton button { background-color: #222f3e; color: white; border: none; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; cursor: pointer; } </style> """, unsafe_allow_html=True )
            exit_button = st.button("Exit the application", help="Click here to exit", use_container_width=True)
            if exit_button:
                if os.path.exists('append.csv'):
                    os.remove('append.csv')
                st.markdown("<h3 style='font-size: 30px; color: #922724; text-align: center; cursor: pointer;'><b>Thank you for using our app! &#128522;</b></h3> ", unsafe_allow_html=True)

    elif menu_selection == "Recommendation":
        st.markdown("<h1 style='color: #131921;'>Product Recommender Page</h1>", unsafe_allow_html=True)
        if st.session_state['submit_count'] == 2 and 'compare_clicked' in st.session_state:
            suggestion()
            st.write("")
            st.write("")
            exit_button = st.button("Exit the application", help="Click here to exit", use_container_width=True)
            if exit_button:
                if os.path.exists('append.csv'):
                    os.remove('append.csv')
                st.write("")
                st.write("")
                st.markdown("<h3 style='font-size: 46px; color: #922724; text-align: center; cursor: pointer;'><b>Thank you for using our app! &#128522;</b></h3> ", unsafe_allow_html=True)
        else:
            st.write("")
            st.write("")
            st.markdown("<h4 style='color: #922724;'>Please enter two product url link for comparing!!!</h4>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()