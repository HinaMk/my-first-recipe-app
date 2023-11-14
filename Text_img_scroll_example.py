import tkinter as tk
from PIL import Image, ImageTk

class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.button = tk.Button(self, text="Click me", command=self.insert_text_and_image)
        self.button.pack()

        self.text_widget = tk.Text(self)
        self.text_widget.pack(side="left")

        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.pack(side="right", fill="y")

        self.text_widget.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.text_widget.yview)

        # this has to be a list b/c we need to store any image we add to the text widget
        # and keep it around. If we just have a single attribute for a PhoteImage, the next 
        # image we read in will overwrite the previous one and make it disappear from the text widget 
        self.photo_list = []  

    def insert_text_and_image(self):
        self.text_widget.insert(tk.END, "\nThis is a test\n")

        # for you this would come from a URL!
        image = Image.open("test.jpg")
        photo_image = ImageTk.PhotoImage(image) # convert image for tkinter
        self.photo_list.append(photo_image) # store in permanent list for later
        self.text_widget.image_create(tk.END, image=photo_image) # "print" image into text widget
        self.text_widget.see(tk.END) # force text widget to scroll to the bottom

app = MyApp()
app.mainloop()