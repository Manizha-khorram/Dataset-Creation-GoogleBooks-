

import requests
import pandas as pd
from sklearn.model_selection import train_test_split
from config import api_key


# Step 1: API key and query by title
query = 'Data Science Machine Learning'
url = f'https://www.googleapis.com/books/v1/volumes?q={query}&key={api_key}'

# Step 2: Fetch Data
response = requests.get(url)
data = response.json()

# Step 3: Check if 'items' key exists in data
if 'items' not in data:
    print("No books found in the API response.")
else:

# Step 3: Extract relevant information into a list of dictionaries
    books_data = []
    for book in data['items']:
        volume_info = book['volumeInfo']
        books_data.append({
            'title': volume_info.get('title', 'Unknown Title'),
            'authors': ', '.join(volume_info.get('authors', ['Unknown Author'])),
            'publisher': volume_info.get('publisher', 'Unknown Publisher'),
            'published_date': volume_info.get('publishedDate', 'Unknown Date'),
            'description': volume_info.get('description', 'No description available'),
            'categories': ', '.join(volume_info.get('categories', ['Uncategorized'])),
            'page_count': volume_info.get('pageCount', 'Unknown'),
            'average_rating': volume_info.get('averageRating', 'Not rated'),
            'ratings_count': volume_info.get('ratingsCount', '0'),
            'language': volume_info.get('language', 'Unknown'),
            'preview_link': volume_info.get('previewLink', ''),
            'info_link': volume_info.get('infoLink', ''),
            'isbn_13': next((identifier['identifier'] for identifier in volume_info.get('industryIdentifiers', []) if identifier['type'] == 'ISBN_13'), 'Unknown'),
        })

# Step 4: Convert to DataFrame
df = pd.DataFrame(books_data)

# Step 5: Split data into train, validation, and test sets
train_data, eval_data = train_test_split(df, test_size=0.2, random_state=42)
eval_data, test_data = train_test_split(eval_data, test_size=0.25, random_state=42)

# Step 6: Save each set as CSV
train_data.to_csv('train_books_data.csv', index=False)
eval_data.to_csv('eval_books_data.csv', index=False)
test_data.to_csv('test_books_data.csv', index=False)

print("Data has been split and saved into train_books_data.csv, eval_books_data.csv, and test_books_data.csv")
