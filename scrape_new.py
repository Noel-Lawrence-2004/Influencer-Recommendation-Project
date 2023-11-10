
import requests
from bs4 import BeautifulSoup
import csv
import pickle 
import re

def convert_to_numeric(string_with_suffix):
    #Converting the string of subscribers into integers
    suffixes = {
        'K': 1_000,
        'M': 1_000_000,
    }
    suffix = string_with_suffix[-1]
    numeric_part = string_with_suffix[:-1]

    # Check if the last character is a valid suffix
    if suffix in suffixes:
        try:
            numeric_value = float(numeric_part)
            numeric_value *= suffixes[suffix]
            return numeric_value
        except ValueError:
            return None
    else:
        try:
            numeric_value = float(string_with_suffix)
            return numeric_value
        except ValueError:
            return None

#getting the url of the page
main_page_url = "https://hypeauditor.com/top-youtube-humor-india/"

csv_filename = 'funny1.csv'

# Send an HTTP GET request to the main page
response = requests.get(main_page_url)
scraped_data = []

# Check if the request was successful
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    entry_containers = soup.find_all('div', class_='row youtube-row')
    count=0
    # Loop through each container to extract data
    for entry in entry_containers:
        #print("Entry found")
        count+=1
        if count==1:
            continue
        
        # Extract data from the main page
        title = entry.find('div', class_='contributor__name-content').text.strip()
        views = entry.find('div', class_='row-cell avg-views').text.strip()
        likes = entry.find('div', class_='row-cell avg-likes').text.strip()
        comments = entry.find('div', class_='row-cell avg-comments').text.strip()
        subscriber_count_span = entry.find('div',class_='row-cell subscribers')
        subscribers = subscriber_count_span.text if subscriber_count_span else "Subscriber count not found"

        description_link = entry.find('a', class_='contributor-link').get('href')       
        description_url = description_link + "/about"
        description_response = requests.get(description_url)

        if description_response.status_code == 200:
            description_soup = BeautifulSoup(description_response.text, 'html.parser')
            if description_soup.find("meta", itemprop="description"):
                channel_description_element = description_soup.find("meta", itemprop="description")['content']
            if channel_description_element:
                description = channel_description_element
            else:
                print("Description not found")
                description= "Description NA"
        else:
            print("Failed to retrieve the About page")
        # Create a dictionary to store the data
        entry_data = {
            "Title": title,
            "Subscribers": subscribers,
            "Views": views,
            "Likes": likes,
            "Comments": comments,
            "Description": description,
            "Engagement Ratio": 100*((convert_to_numeric(likes)+convert_to_numeric(comments))/convert_to_numeric(views)),
            "Video_titles": title
        }
        # Append the data to the list
        scraped_data.append(entry_data)
        if count >4:
            break

# Write the data to the CSV file
with open(csv_filename, 'w', newline='',encoding="utf-8") as csvfile:
    fieldnames = ["Title", "Subscribers", "Views", "Likes", "Comments", "Description",'Engagement Ratio','Video_titles']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader() # Write the header row
    for data in scraped_data:
        writer.writerow(data) # Write the data rows
    print(f"Data has been saved to {csv_filename}")
