import tkinter as tk
from tkinter import ttk
import requests
import keys
import tkinter.scrolledtext as scrolledtext
import urllib.parse 
from PIL import Image, ImageTk
import io
import pandas as pd


# Base URL
URL = "https://api.edamam.com/api/recipes/v2"

class RecipeSearchApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Recipe Search")

        # Search Query
        self.query_label = tk.Label(self, text="Search Query:")
        self.query_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.query_entry = tk.Entry(self)
        self.query_entry.grid(row=0, column=1, columnspan=2, padx=10, pady=10, sticky="ew")

        # Meal Type Dropdown
        self.meal_type_label = tk.Label(self, text="Meal Type:")
        self.meal_type_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.meal_type_var = tk.StringVar(self)
        self.meal_type_var.set("Any")  # Default value

        # CH set to read-only
        self.meal_type_dropdown = ttk.Combobox(self, textvariable=self.meal_type_var, state='readonly',
                                        values=["Any", "Breakfast", "Lunch", "Dinner"])
        self.meal_type_dropdown.grid(row=1, column=1, padx=10, pady=10, sticky="ew", columnspan=2)

        # Calories Range
        self.calories_label = tk.Label(self, text="Calories Range:")
        self.calories_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.calories_frame = tk.Frame(self)
        self.calories_frame.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        self.calories_min_entry = tk.Entry(self.calories_frame, width=5)
        self.calories_min_entry.pack(side="left", padx=0)

        self.calories_dash_label = tk.Label(self.calories_frame, text="-")
        self.calories_dash_label.pack(side="left", padx=0)

        self.calories_max_entry = tk.Entry(self.calories_frame, width=5)
        self.calories_max_entry.pack(side="left", padx=0)

        # Sort By Dropdown
        self.sort_by_label = tk.Label(self, text="Sort by:")
        self.sort_by_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.sort_by_var = tk.StringVar(self)
        self.sort_by_var.set("")  # Default value
        self.sort_by_dropdown = ttk.Combobox(self, textvariable=self.sort_by_var, values=["", "Meal type", "Ingredients", "Calories"])
        self.sort_by_dropdown.grid(row=3, column=1, padx=10, pady=10, sticky="ew", columnspan=2)

        # Search Button
        self.start_search_button = tk.Button(self, text="Start Search", command=self.start_search)
        self.start_search_button.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="ew")
        
        self.result_text = scrolledtext.ScrolledText(self, height=30, width=50, wrap="word") # CH: made taller
        self.result_text.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

    def start_search(self):
        query = self.query_entry.get()
        meal_type = self.meal_type_var.get()
        calories_min = self.calories_min_entry.get()
        calories_max = self.calories_max_entry.get()
        sort_by = self.sort_by_var.get()

        self.result_text.insert(tk.END, "Searching...\n")

        if calories_max != "" and calories_min == "": # CH: if max is not empty and min is empty
            calories_min = "0"

        def is_digit(n):
            try:
                int(n)
                return True
            except ValueError:
                return  False

        # if min >= max, or not all digits, raise error
        if calories_max != "" and calories_min != "":
            if not is_digit(calories_min) or not is_digit(calories_max):
                self.result_text.delete("1.0", tk.END)
                self.result_text.insert(tk.END, "Calories must be numbers\n")
                return
            if int(calories_min) >= int(calories_max):
                self.result_text.delete("1.0", tk.END)
                self.result_text.insert(tk.END, "Invalid calories range, min must be smaller than max\n")
                return

        calories_str = f"{calories_min}-{calories_max}" if calories_min != "" and calories_max != "" else "0-2000"  # maybe use ""?
        recipes = self.search_edamam_recipes(query, meal_type=meal_type, calories=calories_str, sort_by=sort_by)
    
        
        #if search_type == "meal":
        #    recipes = self.search_edamam_recipes(query, meal_type=meal_type, sort_by=sort_by)
        #elif search_type == "calories":
        #    recipes = self.search_edamam_recipes(query, meal_type=meal_type, calories=f"{calories_min}-{calories_max}", sort_by=sort_by)

        self.display_search_results(recipes)

    def search_edamam_recipes(self, query, meal_type="Any", calories="0-2000", sort_by=""):
        params = {
            "q": query,
            "app_id": keys.app_id,
            "app_key": keys.key,
            "type": "any",
            "field": ["label", "calories", "images", "ingredientLines", "mealType", "yield"],  # CH added mealType and yield 
            "mealType": meal_type,
            "calories": calories,
            "sort": sort_by
        }

        # Omit the "mealType" parameter if meal_type is "Any"
        if meal_type == "Any":
            del params["mealType"]

        url = f"{URL}?{urllib.parse.urlencode(params)}"
        print("API URL:", url)

        response = requests.get(URL, params=params)
        if response.status_code == 200:
            result = response.json()
            recipes = result.get('hits', [])
            return recipes
        else:
            return None

    def display_search_results(self, recipes):
        rows = []   # CH: create a list to store the rows
        if recipes:
            self.result_text.delete("1.0", tk.END)
            for recipe in recipes:
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
            sort_by = self.sort_by_var.get()
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
                
                result_text = f"Recipe name: {label}\nCalories per serving: {calories} kcal\nMeal Type: {meal_type}\nIngredients:\n"
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
