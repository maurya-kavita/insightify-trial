import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings


# Suppress the warning about deprecated global pyplot use
warnings.filterwarnings("ignore", category=UserWarning, message="Matplotlib is currently using agg")

st.set_option('deprecation.showPyplotGlobalUse', False)

def visualize_data():
    

    data = pd.read_csv('visualise.csv')  # Replace "your_file.csv" with the actual path to your CSV file
    name = data['Name'].iloc[0]
    st.write("")
    # st.markdown("<h2 style='font-size: 24px; color: #222f3e;'>Visulaization for " + name + "</h2>", unsafe_allow_html=True)
    st.markdown("<h5 style='font-size: 24px; color: #222f3e;'>Visualization for " + name + "</h5>", unsafe_allow_html=True)

    # Interactive Selection: Allow users to select columns for visualization
    st.sidebar.write("")
    st.sidebar.write("")
    st.sidebar.write("")
    st.sidebar.write("")
    st.sidebar.write("")
    st.sidebar.write("")
    st.sidebar.write("")
    selected_columns = st.sidebar.multiselect("Select Columns for Visualization", ['Rating', 'sentiment', 'sentiment_score'])

    # Customization Options: Allow users to customize plot appearance
    plot_title = st.sidebar.text_input("Enter Plot Title", "Visualization")
    x_label = st.sidebar.text_input("Enter X-axis Label", "X-axis")
    y_label = st.sidebar.text_input("Enter Y-axis Label", "Y-axis")
    plot_color = st.sidebar.color_picker("Choose Plot Color", "#1E90FF")  # Default color: blue

    # Plot the selected columns
    if selected_columns:
        st.write(f"### {plot_title}")
        for column in selected_columns:
            sns.histplot(data[column], color=plot_color, kde=True)
            plt.xlabel(x_label)
            plt.ylabel(y_label)
            st.pyplot()

    # Display basic statistics
    st.write("")
    st.subheader("Data Preview:")
    st.dataframe(data.describe().style
                .set_table_styles([
                    {'selector': 'th', 'props': [('border', '1px solid #000000'), ('color', '#ffffff'), ('background-color', '#4CAF50')]},  # Header style
                    {'selector': 'td', 'props': [('border', '1px solid #000000'), ('color', '#000000')]},  # Cell style
                ])
                .format(precision=2)  # Set precision of numerical values
                )

    # Automatic Visualization Options
    st.write("")
    st.write("")
    st.subheader("Visualization:")

    # Plot the histogram
    fig, ax = plt.subplots()
    ax.hist(data['Rating'], bins=8, alpha=0.7, color="#6F224F", edgecolor='black')
    ax.set_xlabel('Rating')
    ax.set_ylabel('Frequency')
    ax.set_title('Histogram of Ratings')
    st.pyplot(fig)

    # Pie Chart for Ratings
    st.write("")
    st.subheader("Pie Chart for Ratings:")
    ratings_column = 'Rating'  # Assuming 'Rating' is the column name for ratings
    pie_data = data[ratings_column].value_counts()
    fig, ax = plt.subplots()
    ax.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    ax.set_title('Distribution of Ratings')
    st.pyplot(fig)

    # Plot the stacked bar chart
    rating_overall_rating_counts = pd.crosstab(data['Rating'], data['Overall_Rating'])
    color = '#9E4663'  # Choose your color
    ax = rating_overall_rating_counts.plot(kind='bar', stacked=True, color=color)
    ax.set_xlabel('Rating')
    ax.set_ylabel('Count')
    ax.set_title('Stacked Bar Chart for Rating and Overall Ratings')
    st.pyplot()

    # Dual-Axis Chart for Overall Rating and Sentiment Score
    st.write("")
    st.subheader("Dual-Axis Chart for Overall Rating and Sentiment Score:")
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    data['Review_Date'] = pd.to_datetime(data['Review_Date'])
    data = data.sort_values(by='Review_Date')
    ax1.plot(data['Review_Age'], data['Overall_Rating'], color='r')
    ax2.plot(data['Review_Age'], data['sentiment_score'], color='b')
    ax1.set_xlabel('Review_Age')
    ax1.set_ylabel('Overall Rating', color='r')
    ax2.set_ylabel('Sentiment Score', color='b')
    st.pyplot(fig)

    # Calculate sentiment counts
    sentiment_counts = data['sentiment'].value_counts()

    # Plot the column chart
    fig, ax = plt.subplots()
    ax.bar(sentiment_counts.index, sentiment_counts.values, color="#B14669")
    ax.set_xlabel('Sentiment')
    ax.set_ylabel('Count')
    ax.set_title('Column Chart for Sentiment')
    ax.set_xticks(range(len(sentiment_counts)))  # Set x-ticks to ensure 8 bins
    ax.set_xticklabels(sentiment_counts.index, rotation=0)  # Rotate x-axis labels for better readability
    st.pyplot(fig)


