import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
import keys
import io

# Base URL
URL = "https://api.edamam.com/api/recipes/v2"

class RecipeSearchApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.tkimg_lst = []
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
        self.calories_min_entry = tk.Entry(self, width=5)
        self.calories_min_entry.grid(row=2, column=1, padx=5, pady=10, sticky="w")
        self.calories_dash_label = tk.Label(self, text="-")
        self.calories_dash_label.grid(row=2, column=2, pady=10)
        self.calories_max_entry = tk.Entry(self, width=5)
        self.calories_max_entry.grid(row=2, column=3, padx=5, pady=10, sticky="e")

        # Sort By
        self.sort_by_label = tk.Label(self, text="Sort by:")
        self.sort_by_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.sort_by_entry = tk.Entry(self)
        self.sort_by_entry.grid(row=3, column=1, columnspan=2, padx=10, pady=10, sticky="ew")

        # Search Buttons
        self.search_by_meal_button = tk.Button(self, text="Search by Meal Type", command=lambda: self.start_search("meal"))
        self.search_by_meal_button.grid(row=4, column=0, padx=10, pady=10, sticky="ew")
        self.search_by_calories_button = tk.Button(self, text="Search by Calories", command=lambda: self.start_search("calories"))
        self.search_by_calories_button.grid(row=4, column=1, columnspan=2, padx=10, pady=10, sticky="ew")

        # Search Results Text
        self.result_text = tk.Text(self, height=10, width=50)
        self.result_text.grid(row=5, column=0, columnspan=4, padx=10, pady=10)

    def start_search(self, search_type):
        query = self.query_entry.get()
        meal_type = self.meal_type_var.get()
        calories_min = self.calories_min_entry.get()
        calories_max = self.calories_max_entry.get()
        sort_by = self.sort_by_entry.get()

        if search_type == "meal":
            recipes = self.search_edamam_recipes(query, meal_type=meal_type, sort_by=sort_by)
        elif search_type == "calories":
            recipes = self.search_edamam_recipes(query, meal_type=meal_type, calories=f"{calories_min}-{calories_max}", sort_by=sort_by)

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
                image_lst = recipe['recipe']["images"]
                img_small_url = image_lst["SMALL"]["url"]
                img_data = requests.get(img_small_url).content
                PILimg = Image.open(io.BytesIO(img_data))
                img_tk = ImageTk.PhotoImage(PILimg)
                self.tkimg_lst.append(img_tk)
                result_text = f"\nRecipe name: {label}\nCalories: {calories} kcal\nIngredients:\n"
                for ingredient in ingredients:
                    result_text += f"- {ingredient}\n"
                self.result_text.insert(tk.END, result_text)
                self.result_text.image_create(tk.END, image=img_tk) # "print" image into text widget
                #self.result_text.see(tk.END)
        else:
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, "No recipes found")


if __name__ == "__main__":
    app = RecipeSearchApp()
    app.mainloop()


### dropdown for sort by (reasonable dafualt)
### have only one search button
## "start search" instead of the two buttons 
## add scroll bar to the text area