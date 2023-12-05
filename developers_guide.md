# Developer's Guide

## Overview 
Welcome to the developer's guide for my Recipe Search App. This document will give you a comprehensive understanding of the project's architecture, deployment process, user interaction flow, known issues, future work, and ongoing development considerations.

## Condensed Version of Planning Specs
The Recipe Search App is designed to allow users to search for recipes using the Edamam Recipe API. Key features include searching based on a query, meal type, calorie range, sorting options, and displaying detailed recipe information.

## Install/Deployment/Admin Issues
Assuming the developer has already read the user's guide, the following steps detail additional considerations for deployment and administration:

1. Install Dependencies:
Ensure that Python 3 is installed on the machine.
Install required libraries using:
pip install -r requirements.txt

2. API Keys:
Obtain API keys from Edamam and replace them in the keys.py file.

### User Interaction and Flow Through Code (Walkthrough)
#### 1. Search Parameters:

- Enter a search query in the "Search Query" field.
- Select a meal type from the dropdown (optional).
- Set the calorie range (optional).
- Choose a sorting option from the "Sort By" dropdown (optional).

#### 2. Initiating Search:

- Click the "Start Search" button to initiate the recipe search.

#### 3. Code Flow:
##### RecipeSearchApp Class:
- ##### Inheritance:
  - Inherits from the tk.Tk class.
- ##### Initialization:
  - The constructor (__init__) sets up the main application window titled "Recipe Search."
- ##### Widgets:
  - Query Entry:
    - A tk.Entry widget for entering the search query.
- ##### Meal Type Dropdown:
  - A ttk.Combobox widget for selecting the meal type (e.g., Breakfast, Lunch, Dinner).
- ##### Calories Range:
  - Two tk.Entry widgets for entering minimum and maximum calories, with a dash label in between.
- ##### Sort By Dropdown:
  - A ttk.Combobox widget for selecting the sorting criteria (e.g., Meal type, Ingredients, Calories).
- ##### Start Search Button:
  - A tk.Button widget triggering the search functionality.
- ##### Result Text:
  - A scrolledtext.ScrolledText widget for displaying the search results.
- ##### Methods:
  - start_search:
    - Retrieves input values (query, meal type, calories range, sort criteria) and initiates the recipe search.
  - search_edamam_recipes:
    - Constructs a URL with parameters for the Edamam API, makes a request, and returns a list of recipes.
  - display_search_results:
    - Takes a list of recipes, processes and sorts the data, and displays the results in the ScrolledText widget.

### Main Code:
- ##### Execution:
  - Creates an instance of the RecipeSearchApp class.
  - Invokes the mainloop method to start the GUI event loop.
#### External Libraries:
- ##### tkinter:
  - Used for creating the GUI components.
- ##### requests:
  - Used for making HTTP requests to the Edamam API.
- ##### keys:
  - Assumes the existence of a module or file named keys containing API credentials.
- ##### PIL (Pillow):
  - Used for working with images.
- ##### io:
  - Used for handling input/output operations.
- ##### pandas:
  - Used for creating and manipulating dataframes.

#### API Integration:
- ##### Edamam API:
  - Utilizes the Edamam API for recipe search based on user input.
  - Retrieves information such as recipe label, calories, images, ingredient lines, meal type, and yield.
#### User Input Handling:
- Validates user inputs, handles errors related to calories, and provides feedback to the user.
#### Data Processing:
- Creates a Pandas dataframe to organize and sort recipe data.
- Sorts recipes based on specified criteria (Meal type, Ingredients, Calories).
#### GUI Design:
- A simple and intuitive GUI design for entering search parameters and displaying search results.


#### 4. API Keys:

- The keys.py file contains API key and application ID. Ensure they are valid and up-to-date.

#### Known Issues
Minor Issues
- None reported.

Major Issues
The app originally displayed recipe images, which are no longer available.


### Future Work
Unimplemented Features:
The Recipe Search App has the potential to include several features outlined in the initial project specifications that were not yet implemented during the current development phase. Some of these features may include:

#### 1. Advanced Search Filters:

- Implement more sophisticated search filters to allow users to refine their queries further.
- For example, filters based on dietary preferences, cuisine types, or specific ingredients.

#### 2. User Authentication:

- Introduce user authentication functionality to enable features like saving favorite recipes or creating personalized recipe lists.

#### 3. Recipe Ratings and Reviews:

- Allow users to rate and review recipes, enhancing the community aspect of the application.

Enhancements:
The Recipe Search App can be enhanced to provide a more robust and user-friendly experience. Potential enhancements may include:

#### 1. Improved User Interface (UI):

- Redesign the UI to make it more intuitive and visually appealing.
- Consider incorporating user-friendly elements such as tooltips or interactive elements for a seamless user experience.

#### 2. Recipe Recommendations:

- Implement a recommendation system that suggests recipes based on user preferences, search history, or trending recipes.

#### 3. Integration with Cooking Timers:

- Allow users to set cooking timers directly from the app for each recipe, providing a more integrated cooking experience.

## Conclusion
This developer's guide is a comprehensive resource for anyone tasked with maintaining or extending the Recipe Search App. Following the outlined information, developers can understand the project's architecture, handle deployment, and plan for ongoing development and improvements.
