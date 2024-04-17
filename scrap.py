import streamlit as st
import csv
import re
import os
import pandas as pd
import urllib.request
import nltk
nltk.download('vader_lexicon')
from bs4 import BeautifulSoup
from datetime import datetime
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def sentiment_cal(combined_data):
    # Load the dataset
    df = pd.read_csv(combined_data)

    # Drop rows with missing values
    df.dropna(subset=['Reviews'], inplace=True)

    # Perform sentiment analysis
    sid = SentimentIntensityAnalyzer()
    df['sentiment_score'] = df['Reviews'].apply(lambda x: sid.polarity_scores(str(x))['compound'])

    # Classify sentiment into positive, negative, or neutral
    def get_sentiment_label(score):
        if score > 0.05:
            return 'Positive'
        elif score < -0.05:
            return 'Negative'
        else:
            return 'Neutral'

    df['sentiment'] = df['sentiment_score'].apply(get_sentiment_label)
    
    # Create a new column for sentiment scores
    df['sentiment_score_label'] = df.apply(lambda row: f"{row['sentiment']} ({row['sentiment_score']})", axis=1)
    
    # Convert the 'Review_Date' column to datetime format
    df['Review_Date'] = pd.to_datetime(df['Date'])
    
    # Calculate the age of each review
    current_date = datetime.now()
    df['Review_Age'] = (current_date - df['Review_Date']).dt.days
    
    # Save the DataFrame to a CSV file
    visualise_csv = 'visualise.csv'
    df.to_csv(visualise_csv, index=False)

def clean_csv(input_file, output_file):
    with open(input_file, 'r', newline='', encoding='utf-8') as infile, \
         open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        for row in reader:
            cleaned_row = [clean_value(value) for value in row]
            writer.writerow(cleaned_row)

def clean_value(value):
    # Remove any non-alphanumeric characters except for whitespace, hyphen, underscore, single quote and dot
    cleaned_value = re.sub(r'[^\w\s\-\'_.]', '', value)
    cleaned_value = cleaned_value.replace("The media could not be loaded.", "")
    return cleaned_value.strip()  # Strip leading and trailing whitespace

def my_logic(url):
    
    html_filename = "amazon.html"
    input_csv = "input.csv"
    append_csv = "append.csv"

    try:
        urllib.request.urlretrieve(url, html_filename)
        # st.success("HTML file saved successfully as amazon.html")

        try:
            with open(html_filename, "r", encoding="utf-8") as file:
                html_content = file.read()

            soup = BeautifulSoup(html_content, "html.parser")
            reviews = soup.find_all("div", class_="a-expander-content reviewText review-text-content a-expander-partial-collapse-content")
            dates = soup.find_all("span", class_="a-size-base a-color-secondary review-date")
            rates = soup.find_all("a", class_="a-size-base a-link-normal review-title a-color-base review-title-content a-text-bold")

            # Write data to input.csv file
            with open(input_csv, 'w', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(["Date", "Rating", "Reviews", "Name", "Price", "Overall_Rating"])

                for review, date, rate in zip(reviews, dates, rates):

                    # Find the product name
                    product_name_span = soup.find("span", class_="a-size-large product-title-word-break")
                    product_name = product_name_span.text.strip() if product_name_span else " "

                    # Find the price
                    product_price_span = soup.find("span", class_="a-price-whole")
                    product_price = product_price_span.text.strip() if product_price_span else " "

                    # Find the rating
                    overall_rating_element = soup.find("a", class_="a-popover-trigger a-declarative")
                    overall_rating_point_span = overall_rating_element.find("span", class_="a-icon-alt")
                    overall_rating_point_format = overall_rating_point_span.text.strip() if overall_rating_point_span else " "
                    overall_rating_point = overall_rating_point_format.split()[0]
                    
                    # Find the review date
                    review_date_span = date
                    review_date_string = review_date_span.text.strip() if review_date_span else " "
                    date_part = review_date_string.split("on")[1].strip()  # Extract the date part from the string
                    review_date_format = datetime.strptime(date_part, "%d %B %Y") # Parse the date string using datetime.strptime
                    review_date = review_date_format.strftime("%d %B %Y")  # Format the date as desired

                    # Find the review rating
                    rating_element = rate
                    rating_point_span = rating_element.find("span", class_="a-icon-alt")
                    rating_point_format = rating_point_span.text.strip() if rating_point_span else " "
                    rating_point = rating_point_format.split()[0]  # Split the string by whitespace and take the first part

                    # Find the product reviews
                    product_reviews_div = review
                    product_reviews = product_reviews_div.text.strip() if product_reviews_div else " "

                    # Write data to CSV
                    csv_writer.writerow([review_date, rating_point, product_reviews, product_name, product_price, overall_rating_point ])

            clean_csv("input.csv", "output.csv")
            if os.path.exists("input.csv"):
                os.remove("input.csv")
                # st.success("CSV file saved successfully as output.csv and deleted input.csv")

            # Read data from dummy.csv
            with open('dummy.csv', 'r', newline='') as dummy_file:
                dummy_reader = csv.reader(dummy_file)
                dummy_data = list(dummy_reader)

            # Modify or add new column data to the dummy_data
            for row in dummy_data:
                row.extend([product_name, product_price, overall_rating_point])

            # Read data from output.csv
            with open('output.csv', 'r', newline='') as output_file:
                output_reader = csv.reader(output_file)
                output_data = list(output_reader)

            # Write the combined data to a new CSV file
            with open('combined_data.csv', 'w', newline='') as combined_file:
                combined_writer = csv.writer(combined_file)
                combined_writer.writerows(output_data + dummy_data)

            clean_csv('combined_data.csv', 'combined.csv')
            if os.path.exists("combined_data.csv"):
                os.remove("combined_data.csv")
                # st.success("Combined data written to combined.csv and deleted combined_data.csv")
            
            # Creating append.csv
            if not os.path.exists(append_csv):
                # If the file doesn't exist, create it and write the header row
                with open(append_csv, 'w', newline='', encoding='utf-8') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerow(["Name", "Price", "Overall_Rating", "Avg_Rating"])  
                                        
            df = pd.read_csv("output.csv")
            # Calculate the average rating
            avg_rating = round(df['Rating'].mean(), 1)
            # Open the CSV file in append mode and write the new row
            with open(append_csv, 'a', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow([product_name, product_price, overall_rating_point, avg_rating])
            # st.success("CSV file saved successfully as append.csv")

        except Exception as e:
            st.markdown("<h3 style='color: #922724;'>Something went wrong during scraping!</h3>", unsafe_allow_html=True)

        sentiment_cal('combined.csv')

        # st.success("Visualizations saved successfully as visualise.csv")
        st.markdown("<h3 style='color: #22733D;'>Visualization is ready, please switch to visualization page!!!</h3>", unsafe_allow_html=True)


    except Exception as e:
        st.markdown("<h3 style='color: #922724;'>Oops! Amazon is tired of your demands!!!</h3>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: #922724;'>Try again if you wanna give another shot&#129393;</h3>", unsafe_allow_html=True)
        
    
