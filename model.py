import streamlit as st
import pandas as pd

# Load data from CSV file
def load_data(filename):
    df = pd.read_csv(filename)
    return df

# Streamlit UI
def suggestion():

    try:

        # Load data
        df = load_data("append.csv")

        # Display product information
        st.write("")
        st.markdown("<h5 style='font-size: 24px; color: #222f3e;'>Products Information:</h5>", unsafe_allow_html=True)
        st.write(df)
        st.write("")
        st.write("")

        # Selecting products
        st.markdown("<h5 style='font-size: 24px; color: #222f3e;'>Select Products:</h5>", unsafe_allow_html=True)
        selected_product_1 = st.selectbox("Select Product 1:", df['Name'])
        selected_product_2 = st.selectbox("Select Product 2:", df['Name'])

        # Get information of selected products
        product_1_info = df[df['Name'] == selected_product_1].iloc[0]
        product_2_info = df[df['Name'] == selected_product_2].iloc[0]

        # Check which product is better based on criteria
        st.write( """ <style> .stButton button { background-color: #222f3e; font-size: 30px; color: white; border: none; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; cursor: pointer; } </style> """, unsafe_allow_html=True )
        recommend_button = st.button("Recommend", help="Click here for product recommendation", use_container_width=True)
        st.write("")
        if recommend_button:
            if (product_1_info['Price'] <= product_2_info['Price']) and \
            (product_1_info['Overall_Rating'] >= product_2_info['Overall_Rating']) and \
            (product_1_info['Avg_Rating'] >= product_2_info['Avg_Rating']):
                st.markdown("<h5 style='font-size: 24px; color: #222f3e;'>Recommended Product:</h5>", unsafe_allow_html=True)
                st.markdown("<h6 style='font-size: 20px; color: #22733D'> " + selected_product_1 + "</h6>", unsafe_allow_html=True)
            elif (product_2_info['Price'] <= product_1_info['Price']) and \
                (product_2_info['Overall_Rating'] >= product_1_info['Overall_Rating']) and \
                (product_2_info['Avg_Rating'] >= product_1_info['Avg_Rating']):
                st.markdown("<h5 style='font-size: 24px; color: #222f3e;'>Recommended Product:</h5>", unsafe_allow_html=True)
                st.markdown("<h6 style='font-size: 20px; color: #22733D'> " + selected_product_2 + "</h6>", unsafe_allow_html=True)
            else:
                st.markdown("<h5 style='font-size: 24px; color: #222f3e;'>Recommended Product:</h5>", unsafe_allow_html=True)
                st.markdown("<h6 style='font-size: 20px; color: #22733D;'>Both products are equally good</h6>", unsafe_allow_html=True)

            # Closing message
            # st.write("")
            # st.write("")
            # st.markdown("<h3 style='font-size: 46px; color: #922724; text-align: center; cursor: pointer;'><b>Thank you for using our app! &#128522;</b></h3> ", unsafe_allow_html=True)
        
    except Exception as e:
        st.markdown("<h3 style='color: #922724;'>Please enter two product url link for comparing!!!</h3>", unsafe_allow_html=True)


