import tkinter as tk #library for GUI
from tkinter import ttk #library for GUI
import requests #library to make HTTP requests
import keys #file with API keys
import tkinter.scrolledtext as scrolledtext #library for GUI
import urllib.parse #library to parse URL strings
from PIL import Image, ImageTk #library to display images
import io #library to handle file-like objects
import pandas as pd #library to handle dataframes


# Base URL
URL = "https://api.edamam.com/api/recipes/v2"

class RecipeSearchApp(tk.Tk): #class for the main application window
    def __init__(self): #constructor
        super().__init__() #call the constructor of the parent class
        self.title("Recipe Search") #set the title of the window

        # Search Query
        self.query_label = tk.Label(self, text="Search Query:") #create a label widget
        self.query_label.grid(row=0, column=0, padx=10, pady=10, sticky="e") #position the label widget in the window
        self.query_entry = tk.Entry(self) #create an entry widget
        self.query_entry.grid(row=0, column=1, columnspan=2, padx=10, pady=10, sticky="ew") #position the entry widget in the window

        # Meal Type Dropdown
        self.meal_type_label = tk.Label(self, text="Meal Type:") #create a label widget
        self.meal_type_label.grid(row=1, column=0, padx=10, pady=10, sticky="e") #position the label widget in the window
        self.meal_type_var = tk.StringVar(self) #create a string variable to store the selected meal type
        self.meal_type_var.set("Any") #set the default value of the meal type variable

        # CH set to read-only
        self.meal_type_dropdown = ttk.Combobox(self, textvariable=self.meal_type_var, state='readonly', #create a dropdown widget
                                        values=["Any", "Breakfast", "Lunch", "Dinner"]) #set the values of the dropdown widget
        self.meal_type_dropdown.grid(row=1, column=1, padx=10, pady=10, sticky="ew", columnspan=2) #position the dropdown widget in the window

        # Calories Range
        self.calories_label = tk.Label(self, text="Calories Range:") #create a label widget
        self.calories_label.grid(row=2, column=0, padx=10, pady=10, sticky="e") #position the label widget in the window
        self.calories_frame = tk.Frame(self) #create a frame widget
        self.calories_frame.grid(row=2, column=1, padx=10, pady=10, sticky="ew") #position the frame widget in the window
        self.calories_min_entry = tk.Entry(self.calories_frame, width=5)   #create an entry widget
        self.calories_min_entry.pack(side="left", padx=0) #position the entry widget in the frame widget

        self.calories_dash_label = tk.Label(self.calories_frame, text="-") #create a label widget
        self.calories_dash_label.pack(side="left", padx=0) #position the label widget in the frame widget

        self.calories_max_entry = tk.Entry(self.calories_frame, width=5) #create an entry widget
        self.calories_max_entry.pack(side="left", padx=0) #position the entry widget in the frame widget

        # Sort By Dropdown
        self.sort_by_label = tk.Label(self, text="Sort by:") #create a label widget
        self.sort_by_label.grid(row=3, column=0, padx=10, pady=10, sticky="e") #position the label widget in the window
        self.sort_by_var = tk.StringVar(self) #create a string variable to store the selected sort by value
        self.sort_by_var.set("")  #set the default value of the sort by variable
        self.sort_by_dropdown = ttk.Combobox(self, textvariable=self.sort_by_var, values=["", "Meal type", "Ingredients", "Calories"]) #create a dropdown widget
        self.sort_by_dropdown.grid(row=3, column=1, padx=10, pady=10, sticky="ew", columnspan=2) #position the dropdown widget in the window

        # Search Button
        self.start_search_button = tk.Button(self, text="Start Search", command=self.start_search) #create a button widget
        self.start_search_button.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="ew") #position the button widget in the window
        
        self.result_text = scrolledtext.ScrolledText(self, height=30, width=50, wrap="word") #create a scrolled text widget
        self.result_text.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky="nsew") #position the scrolled text widget in the window

    def start_search(self): #method to handle the button click event
        query = self.query_entry.get() #get the value of the query entry widget
        meal_type = self.meal_type_var.get() #get the value of the meal type dropdown widget
        calories_min = self.calories_min_entry.get() #get the value of the calories min entry widget
        calories_max = self.calories_max_entry.get() #get the value of the calories max entry widget
        sort_by = self.sort_by_var.get() #get the value of the sort by dropdown widget

        self.result_text.insert(tk.END, "Searching...\n") #insert text at the end of the scrolled text widget

        if calories_max != "" and calories_min == "": # if max is set but min is not, set min to 0
            calories_min = "0" # set min to 0

        def is_digit(n): # check if a string is a number
            try: 
                int(n) # try to convert the string to an integer
                return True # if successful, return True
            except ValueError: # if an exception is raised, return False
                return  False

        # if min >= max, or not all digits, raise error
        if calories_max != "" and calories_min != "": # if both min and max are set
            if not is_digit(calories_min) or not is_digit(calories_max): # if either min or max is not a number
                self.result_text.delete("1.0", tk.END) # delete the text in the scrolled text widget
                self.result_text.insert(tk.END, "Calories must be numbers\n") # insert text at the end of the scrolled text widget
                return
            if int(calories_min) >= int(calories_max): 
                self.result_text.delete("1.0", tk.END) # delete the text in the scrolled text widget
                self.result_text.insert(tk.END, "Invalid calories range, min must be smaller than max\n") # insert text at the end of the scrolled text widget
                return

        calories_str = f"{calories_min}-{calories_max}" if calories_min != "" and calories_max != "" else "0-2000"  # if min and max are set, use them, otherwise use the default range
        recipes = self.search_edamam_recipes(query, meal_type=meal_type, calories=calories_str, sort_by=sort_by) # call the search_edamam_recipes method
    

        self.display_search_results(recipes) # call the display_search_results method

    def search_edamam_recipes(self, query, meal_type="Any", calories="0-2000", sort_by=""): #method to search for recipes using the Edamam API
        params = { #dictionary of query parameters
            "q": query,
            "app_id": keys.app_id,
            "app_key": keys.key,
            "type": "any",
            "field": ["label", "calories", "images", "ingredientLines", "mealType", "yield"],  
            "mealType": meal_type,
            "calories": calories,
            "sort": sort_by
        }

        # Omit the "mealType" parameter if meal_type is "Any"
        if meal_type == "Any":
            del params["mealType"]

        url = f"{URL}?{urllib.parse.urlencode(params)}" #create the URL with the query parameters
        print("API URL:", url) #print the URL to the console

        response = requests.get(URL, params=params) #send a GET request to the API
        if response.status_code == 200: 
            result = response.json()
            recipes = result.get('hits', [])
            return recipes
        else:
            return None

    def display_search_results(self, recipes): #method to display the search results
        rows = []   # create an empty list to store the recipe data
        if recipes: # if recipes is not empty
            self.result_text.delete("1.0", tk.END) # delete the text in the scrolled text widget
            for recipe in recipes: # loop through the recipes
                label = recipe['recipe']['label']
                calories = recipe['recipe']['calories']
                ingredients = recipe['recipe']['ingredientLines']
                meal_type_list = recipe['recipe']['mealType'] 
                meal_type = ", ".join(meal_type_list) 
                num_servings = recipe['recipe']['yield']  
                
                # add the recipe data in form of a dict to the list  
                rows.append({'label': label, 'calories': int(calories / num_servings), 
                    'mealType': meal_type, 'ingredients': ingredients, 
                    'num_ingredients': len(ingredients)})
            df = pd.DataFrame(rows) # create a dataframe from the list of rows
            
            # Sort the dataframe by the sort_by_var widget value
            sort_by = self.sort_by_var.get() # get the value of the sort by dropdown widget
            if sort_by == "Meal type":
                df = df.sort_values(by=['mealType'])
            elif sort_by == "Ingredients":
                df = df.sort_values(by=['num_ingredients'], ascending=True) # small to high
            elif sort_by == "Calories":
                df = df.sort_values(by=['calories'], ascending=True) # small to high

            # Loop through the dataframe, get the cell values for each row and print the results
            for index, row in df.iterrows(): # grab each row as a Series called row
                label = row['label']
                calories = row['calories']
                ingredients = row['ingredients']
                meal_type = row['mealType']
                 
                result_text = f"Recipe name: {label}\nCalories per serving: {calories} kcal\nMeal Type: {meal_type}\nIngredients:\n" # create a string with the recipe data
                for ingredient in ingredients: 
                    result_text += f"- {ingredient}\n"
                self.result_text.insert(tk.END, result_text)
                self.result_text.insert(tk.END, "\n")
        else:
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, "No recipes found") 


if __name__ == "__main__":
    app = RecipeSearchApp()
    app.mainloop()
