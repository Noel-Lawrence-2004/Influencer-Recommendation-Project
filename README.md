# Influencer-Recommendation-Project
An Influencer Recommendation System which recommends youtubers to sponsor a product based on the similarity between the products description and the youtubers description

This recommendation system is build by webscraping "HypeAuditor.com" a website to get the namesand average likes,views and comments of the top youtubers in many different categories such as Comedy,Education,Technology,etc, next we Scrape youtube to get the individual youtubers description by using Beautiful Soup and store all these data in csv files.
After Acquiring he dataset for the youtubers we perform data integration and combine all the individual csv files into one csv file.
Now we preprocess the textual descriptions by removing the null descriptions, removing any non-English description and emojis. We further preprocess the text by removing usernames,links, tokenizing, Lemmatizing the descriptions. Finally we use tf-idf vectorizer and Word2Vec on the youtuber and product descriptions and find the cosine similarity between them to give a similarity rating. 
Finally we assign weighted values to each individual youtubers subscriber count, engagement rate and the similarity rate to give a compatibility rating of a youtuber with their particular product.
