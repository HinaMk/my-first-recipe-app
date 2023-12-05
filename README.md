# my-first-recipe-app

A Python application built using Tkinter to search for recipes using the Edamam Recipe API.

## Features

- Search for recipes based on a query, meal type, calories range, and sorting options.
- Display recipe details including name, calories per serving, meal type, and ingredients.
- Use a read-only dropdown menu for meal types and a more flexible calories entry.
- Sort search results by meal type, number of ingredients, or calories per serving.
- Display search progress and handle invalid input gracefully.

## Prerequisites

Before running the application, make sure you have the following:

- Python 3 installed on your machine.
- The `requests`, `PIL`, and `pandas` libraries installed. You can install them using:

  ```bash
  pip install requests pillow pandas

# Getting Started

1. Clone this repository:
git clone <repository-url>

2. Navigate to the project directory:
cd recipe-search-app

3. Run the application:
python recipe_search_app.py

## Usage
1. Enter your search query in the "Search Query" field.
2. Select a meal type from the dropdown (optional).
3. Set the calorie range (optional).
4. Choose a sorting option from the "Sort By" dropdown (optional).
5. Click the "Start Search" button to initiate the recipe search.

## API Keys
This application requires API keys from Edamam. You'll need to get your own API key and application ID and replace them in the keys.py file.
  ### keys.py
```
app_id = "YOUR_EDAMAM_APP_ID"
key = "YOUR_EDAMAM_API_KEY"
```
# App Screenshots
<img width="388" alt="Screenshot 2023-12-05 at 12 39 53 PM" src="https://github.com/HinaMk/my-first-recipe-app/assets/143449380/62c2ab77-e2a5-4af5-9ee6-1419dc71cd46">

<img width="388" alt="Screenshot 2023-12-05 at 12 40 27 PM" src="https://github.com/HinaMk/my-first-recipe-app/assets/143449380/a4262eee-63c6-4197-bcbc-342e55c59fba">

<img width="387" alt="Screenshot 2023-12-05 at 2 29 55 PM" src="https://github.com/HinaMk/my-first-recipe-app/assets/143449380/1c7678a9-c6d0-4b7c-beb0-e73f39bac2b2">

<img width="386" alt="Screenshot 2023-12-05 at 2 30 37 PM" src="https://github.com/HinaMk/my-first-recipe-app/assets/143449380/1e85e9da-64ec-4590-b636-b2e322f6416e">

<img width="385" alt="Screenshot 2023-12-05 at 2 30 59 PM" src="https://github.com/HinaMk/my-first-recipe-app/assets/143449380/3d59466b-b098-4691-8355-243ccb288fb6">

<img width="387" alt="Screenshot 2023-12-05 at 2 31 31 PM" src="https://github.com/HinaMk/my-first-recipe-app/assets/143449380/f793c4a5-50be-41c1-9103-35eed7b3ce40">


# License
This project is licensed under the MIT License - see the LICENSE file for details.

