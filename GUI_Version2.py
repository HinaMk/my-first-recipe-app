import tkinter as tk # GUI library
import requests # HTTP library
import keys # API keys

# Base URL
URL = "https://api.edamam.com/api/recipes/v2"

class RecipeSearchApp(tk.Tk): # Inherit from tk.Tk class
    def __init__(self): # Constructor
        super().__init__() # Call the constructor of the parent class
        self.title("Recipe Search") # Set the title of the window

        # Create labels and entry fields for user input
        self.query_label = tk.Label(self, text="Search Query:") # Create a label
        self.query_label.pack() # Add the label to the window
        self.query_entry = tk.Entry(self) # Create an entry field
        self.query_entry.pack() # Add the entry field to the window

        self.meal_type_label = tk.Label(self, text="Meal Type:") # Create a label
        self.meal_type_label.pack() # Add the label to the window
        self.meal_type_entry = tk.Entry(self) # Create an entry field
        self.meal_type_entry.pack() # Add the entry field to the window

        self.calories_label = tk.Label(self, text="Calories Range:") # Create a label
        self.calories_label.pack() # Add the label to the window
        self.calories_entry = tk.Entry(self) # Create an entry field
        self.calories_entry.pack() # Add the entry field to the window

        self.sort_by_label = tk.Label(self, text="Sort by:") # Create a label
        self.sort_by_label.pack() # Add the label to the window
        self.sort_by_entry = tk.Entry(self) # Create an entry field
        self.sort_by_entry.pack() # Add the entry field to the window

        # Create a "Search" button
        self.search_button = tk.Button(self, text="Search", command=self.start_search) # Create a button
        self.search_button.pack() # Add the button to the window

        # Create a text area to display search results
        self.result_text = tk.Text(self, height=10, width=50) # Create a text area
        self.result_text.pack() # Add the text area to the window
 
    def start_search(self): # Callback function for the "Search" button
        # Get user input from entry fields
        query = self.query_entry.get() # Get the text from the entry field
        meal_type = self.meal_type_entry.get() # Get the text from the entry field
        calories = self.calories_entry.get() # Get the text from the entry field
        sort_by = self.sort_by_entry.get() # Get the text from the entry field

        # Perform the recipe search using the provided criteria
        recipes = self.search_edamam_recipes(query, meal_type, calories, sort_by) # Call the search function

        # Display the search results in the text area
        if recipes: # If recipes were found
            self.result_text.delete("1.0", tk.END)  # Clear previous results
            for recipe in recipes: # Iterate over the recipes
                label = recipe['recipe']['label'] # Get the recipe name
                calories = recipe['recipe']['calories'] # Get the calories
                ingredients = recipe['recipe']['ingredientLines'] # Get the ingredients
                image = recipe['recipe'].get('image', 'No image available') # Get the image URL
 
                # Append the recipe details to the text area
                result_text = f"Recipe name: {label}\nCalories: {calories} kcal\nIngredients:\n" # Create a string
                for ingredient in ingredients: # Iterate over the ingredients
                    result_text += f"- {ingredient}\n" # Append the ingredient to the string
                result_text += f"Image: {image}\n\n" # Append the image URL to the string
                self.result_text.insert(tk.END, result_text) # Add the string to the text area
        else:
            self.result_text.delete("1.0", tk.END) # Clear previous results
            self.result_text.insert(tk.END, "No recipes found") # Display a message

    def search_edamam_recipes(self, query, meal_type, calories, sort_by): # Function to search for recipes
        params = {
            "q": query,
            "app_id": keys.app_id,
            "app_key": keys.key,
            "type": "any",
            "field": ["label", "calories", "images", "ingredientLines", "totalCO2Emissions", "yield", "totalTime"],
            "mealType": meal_type,
            "calories": calories,
            "sort": sort_by
        }

        response = requests.get(URL, params=params)
        if response.status_code == 200:
            result = response.json()
            recipes = result.get('hits', [])
            return recipes
        else:
            return None

if __name__ == "__main__": # If the script is executed directly
    app = RecipeSearchApp() # Create an instance of the RecipeSearchApp class
    app.mainloop() # Run the main loop
