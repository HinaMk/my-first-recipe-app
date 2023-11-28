import tkinter as tk
from tkinter import ttk
import requests
import keys

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
        self.meal_type_dropdown = ttk.Combobox(self, textvariable=self.meal_type_var, values=["Any", "Breakfast", "Lunch", "Dinner"])
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

        # Sort By
        self.sort_by_label = tk.Label(self, text="Sort by:")
        self.sort_by_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.sort_by_entry = tk.Entry(self)
        self.sort_by_entry.grid(row=3, column=1, columnspan=2, padx=10, pady=10, sticky="ew")

        # Search Button
        self.start_search_button = tk.Button(self, text="Start Search", command=self.start_search)
        self.start_search_button.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        #Search Buttons [OLD Version]
        #self.search_by_meal_button = tk.Button(self, text="Search by Meal Type", command=lambda: self.start_search("meal"))
        #self.search_by_meal_button.grid(row=4, column=0, padx=10, pady=10, sticky="ew")
        #self.search_by_calories_button = tk.Button(self, text="Search by Calories", command=lambda: self.start_search("calories"))
        #self.search_by_calories_button.grid(row=4, column=1, columnspan=2, padx=10, pady=10, sticky="ew")

        # Search Results Text
        self.result_text = tk.Text(self, height=10, width=50)
        self.result_text.grid(row=5, column=0, columnspan=4, padx=10, pady=10)

    def start_search(self):
        query = self.query_entry.get()
        meal_type = self.meal_type_var.get()
        calories_min = self.calories_min_entry.get()
        calories_max = self.calories_max_entry.get()
        sort_by = self.sort_by_entry.get()

        # Determine the search type based on user input
        search_type = "meal" if meal_type != "Any" else "calories"

        recipes = self.search_edamam_recipes(query, meal_type=meal_type, calories=f"{calories_min}-{calories_max}", sort_by=sort_by)
    
    #def start_search(self, search_type): [OLD Version]
        #query = self.query_entry.get()
        #meal_type = self.meal_type_var.get()
        #calories_min = self.calories_min_entry.get()
        #calories_max = self.calories_max_entry.get()
        #sort_by = self.sort_by_entry.get()

        #if search_type == "meal":
            #recipes = self.search_edamam_recipes(query, meal_type=meal_type, sort_by=sort_by)
        #elif search_type == "calories":
            #recipes = self.search_edamam_recipes(query, meal_type=meal_type, calories=f"{calories_min}-{calories_max}", sort_by=sort_by)

        self.display_search_results(recipes)

    def search_edamam_recipes(self, query, meal_type="Any", calories="0-2000", sort_by=""):
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

    def display_search_results(self, recipes):
        if recipes:
            self.result_text.delete("1.0", tk.END)
            for recipe in recipes:
                label = recipe['recipe']['label']
                calories = recipe['recipe']['calories']
                ingredients = recipe['recipe']['ingredientLines']
                image = recipe['recipe'].get('image', 'No image available')

                result_text = f"Recipe name: {label}\nCalories: {calories} kcal\nIngredients:\n"
                for ingredient in ingredients:
                    result_text += f"- {ingredient}\n"
                result_text += f"Image: {image}\n\n"
                self.result_text.insert(tk.END, result_text)
        else:
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, "No recipes found")


if __name__ == "__main__":
    app = RecipeSearchApp()
    app.mainloop()
