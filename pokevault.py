import tkinter as tk 
import requests
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from io import BytesIO



root  = tk.Tk()
root.title("Pokémon App")
root.geometry("1500x800")

def pokemon_data(name):#fetching specific name from the API
     url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"
     response = requests.get(url)
     if response.status_code == 200:
          data = response.json()
          return data
     else:  
          messagebox.showerror("Error to get Pokemon Data")
          return None

def pokemon_species(name):#fetching specific species data from the API
     url = f"https://pokeapi.co/api/v2/pokemon-species/{name.lower()}"
     response = requests.get(url)
     if response.status_code == 200:
          data = response.json()
          return data
     else:  
          messagebox.showerror("Error to get Pokemon Species Data")
          return None

def pokemon_characteristics(char_id):#fetching specific characteristics data from the API
    url = f"https://pokeapi.co/api/v2/characteristic/{char_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

def pokemons():#fetching all pokemon names from the API with a 1000 limit
     url = "https://pokeapi.co/api/v2/pokemon?limit=1000"
     response = requests.get(url)
     if response.status_code == 200:
        data = response.json()
        return [pokemon['name'] for pokemon in data['results']]
     else:
        messagebox.showerror("Error to get pokemon data ")
        return []
def pokemon_games():#fetching all pokemon games from the API
     url = "https://pokeapi.co/api/v2/version"
     response = requests.get(url)
     if response.status_code == 200:
        return response.json()['results']
     else:
        messagebox.showerror("Error to get Pokemon Games")
        return []

def pokemon_items():#fetching all pokemon items from the API with a 1000 limit
     url = "https://pokeapi.co/api/v2/item?limit=1000"
     response = requests.get(url)
     if response.status_code == 200:
        return response.json()['results']
     else:
        messagebox.showerror("Error to get Pokemon Items")
        return []

def pokemon_location():     
     url = "https://pokeapi.co/api/v2/location?limit=1000"#fetching all pokemon locations with a limit of 1000
     response = requests.get(url)
     if response.status_code == 200:
        return response.json()['results']
     else:
        messagebox.showerror("Error to get Pokemon Location")
        return []


def start_screen():#starting screen with a start button
     start_frame = tk.Frame(root)#starting screen frame
     start_frame.pack(fill="both", expand=True)

     start_img_path = "C:\\Users\\eriel\\Desktop\\pokemon app\\startbg.png"#image path
     start_bg = Image.open(start_img_path).resize((1500, 800))
     start_photo = ImageTk.PhotoImage(start_bg)


     start_label = tk.Label(start_frame, image=start_photo)
     start_label.image = start_photo  
     start_label.pack(fill="both", expand=True)#putting image as background

     start_button = tk.Button(start_frame, text="Start", font=("Cooper Black", 20),bg="#FFCC01",  fg="#0070B6", command=main_page, width=10)#start button
     start_button.place(relx=0.5, rely=0.8, anchor="center")#placing start button on the start frame


def main_page():#main frame with navigation bar and content
     for widget in root.winfo_children():
        widget.destroy()#destroying previous widgets in the main frame

     global main_frame#making main_frame global to use outisde the function


     nav_bar = tk.Frame(root, bg="#ff3131", height=50)#navigation bar
     nav_bar.pack(side="top", fill="x")#placing navigation bar on the top

     nav_btn = ["Pokemons", "Games", "Items", "Locations"]#link buttons for the navigation bar

     def navigation_click(click):#function when the navigation button is clicked
        navigation_btn(click)

     for btn in nav_btn:#creating navigation buttons and binding them for each button 
        nav_button = tk.Button(nav_bar, text=btn, bg="#ff3131", fg="#fff", font=("Cooper Black", 20), padx=10, pady=5, relief="flat")
        nav_button.pack(side="left", padx=105, pady=10)
        nav_button.bind("<Button-1>", lambda e, click=btn: navigation_click(click))

     main_frame = tk.Frame(root, bg="#fff")#main frame display
     main_frame.pack(fill="both", expand=True)#display whole frame
     navigation_btn("Pokemons")#show as the first page of the app after clicking start button

def navigation_btn(click):#function when navigation button is clicked
     if click == "Pokemons":
          search_pokemon()#go to search pokemon frame
     elif click == "Games":
          game_content()#go to pokemon games frame
     elif click == "Items":
          item_content()#go to pokemon items frame
     elif click == "Locations":
          location_content()#go to pokemon locations frame
     
def show_pokemon_data(data):#displaying pokemon details when searched
    for widget in main_frame.winfo_children():
        widget.destroy()#removing the widget from the main frame

    left_frame = tk.Frame(main_frame, bg="#fff")#left column to show the type, sprite, and name of the pokemon
    left_frame.grid(row=0, column=0, padx=20, pady=20, sticky="w") #using row to organize the widgets

    right_frame = tk.Frame(main_frame, bg="#fff")#right column for the other desciprtions of the pokemon
    right_frame.grid(row=0, column=1, padx=20, pady=20, sticky="e")  

    label_name = tk.Label(left_frame, text=f"{data['name'].capitalize()}", font=("Cooper Black", 18), bg="#fff")#displaying pokemon name
    label_name.grid(row=0, column=0, padx=10, pady=10)

    sprite_url = data['sprites']['front_default']#getting the spirte imge url
    if sprite_url:#using if statement to check if the sprite image is available or not
        response = requests.get(sprite_url)#getting the spirte image using request
        img_data = BytesIO(response.content)
        img = Image.open(img_data)
        img = img.resize((500, 500), Image.Resampling.LANCZOS)  
        sprite_image = ImageTk.PhotoImage(img)

        sprite_label = tk.Label(left_frame, image=sprite_image, bg="#fff")#displaying the sprite image
        sprite_label.image = sprite_image
        sprite_label.grid(row=1, column=0, padx=5, pady=5)#placing the sprite image in a grid

    types = ", ".join([type_info['type']['name'].capitalize() for type_info in data['types']])#getting the pokemon type
    types_label = tk.Label(left_frame, text=f"Type(s): {types}", font=("Cooper Black", 14), bg="#fff")#displaying the pokemon type as text
    types_label.grid(row=2, column=0, padx=10, pady=10)#placing the text

    species_data = pokemon_species(data['name'])#getting specites data from exsisting function
    if species_data:#checking if the species data is avialable
        flavor_text_entries = species_data.get("flavor_text_entries", [])
        description = next(
            (entry["flavor_text"].replace("\n", " ").replace("\f", " ")
             for entry in flavor_text_entries if entry["language"]["name"] == "en"),
            "No description available."
        )
        
        habitat = species_data.get("habitat", {}).get("name", "Unknown Habitat").capitalize()#gettind data from pokemons habitat
        color = species_data.get("color", {}).get("name", "Unknown Color").capitalize()#color of pokemon
        forms = [form['name'].capitalize() for form in species_data.get("forms", [])]#forms of pokemon
        location_habitat = species_data.get("location_area_encounters", [])#location where the pokemon is located

    else:#else if there is no data that is fetched
        description = "No description available."
        habitat = color = "Unknown"
        forms = []
        location_habitat = []

    description_label = tk.Label(right_frame, text=f"Description:\n{description}", font=("Cooper Black", 14), bg="#fff", wraplength=600, justify="left")#displaying the description of the pokemon
    description_label.grid(row=0, column=0, padx=10, pady=10)

    stats = "\n".join([f"{stat['stat']['name'].capitalize()}: {stat['base_stat']}" for stat in data['stats']])#fetching the stats of the pokemon
    stats_label = tk.Label(right_frame, text=f"Stats:\n{stats}", font=("Cooper Black", 14), bg="#fff")#displaying stats
    stats_label.grid(row=1, column=0, padx=10, pady=10)

    habitat_label = tk.Label(right_frame, text=f"Habitat: {habitat}", font=("Cooper Black", 14), bg="#fff", justify="left")#displaying habitat of the fetched pokemon
    habitat_label.grid(row=2, column=0, padx=10, pady=5)

    color_label = tk.Label(right_frame, text=f"Color: {color}", font=("Cooper Black", 14), bg="#fff", justify="left"  )#displaying color of the fetches pokemon
    color_label.grid(row=3, column=0, padx=10, pady=5)


    forms_label = tk.Label(right_frame, text=f"Forms: {', '.join(forms) if forms else 'No forms available.'}", font=("Cooper Black", 14), bg="#fff", justify="left"  )#displaying forms of the fetched pokemon
    forms_label.grid(row=4, column=0, padx=10, pady=5)
    if location_habitat:#if statement to check if location data is available for the fetched pokemon
        location_labels = "\n".join([f"Location: {loc['location_area']['name'].capitalize()}" for loc in location_habitat]) 
    else:
        location_labels = "No location data available."
    location_label = tk.Label(right_frame, text=f"Location Habitats: \n{location_labels}", font=("Cooper Black", 14), bg="#fff", justify="left")#displaying location data of the fetched pokemon
    location_label.grid(row=5, column=0, padx=10, pady=10)


    back_button = tk.Button(right_frame, text="Back", font=("Cooper Black", 20), bg="#FFCC01", fg="#0070B6", command=search_pokemon, width=10)#displaing back button
    back_button.grid(row=6, column=0, padx=10, pady=10)
          



def search_pokemon():#search pokemon page as a function
     for widget in main_frame.winfo_children():
        widget.destroy()#removing the widgets from the main frame to reset

     logo_img_path = "C:\\Users\\eriel\\Desktop\\pokemon app\\searchbg.png"#image path
     logo_bg = Image.open(logo_img_path).resize((1500, 800))
     logo_photo = ImageTk.PhotoImage(logo_bg)

     logo_label = tk.Label(main_frame, image=logo_photo)
     logo_label.image = logo_photo
     logo_label.pack()#placing the logo image in the main frame

     label = tk.Label(main_frame, text="Search for a Pokemon:", font=("Cooper Black", 20), bg="#fff",  fg="#0070B6")#text display for searching pokemon
     label.place(x=600, y=250)

    # Fetch the Pokémon names
     pokemon_names = pokemons()#fetching all the pokemon names
     if not pokemon_names:
        return

     selected_pokemon = tk.StringVar()#making all the pokemon names as string
     search_option = ttk.Combobox(main_frame, textvariable=selected_pokemon, values=pokemon_names, state="readonly")#dropdown menu with all the pokemon names
     search_option.place(x=600, y=300,width=280)

     def options():#function to get the selected pokemon
        pokemon_name = selected_pokemon.get()#storing selected pokemon
        if pokemon_name:
            data = pokemon_data(pokemon_name)
            if data:
                show_pokemon_data(data)
            else:
                messagebox.showerror("Failed to get Pokemon data")
        else:
            messagebox.showwarning("Please Select another Pokemon")

     search_button = tk.Button(main_frame, text="Search", font=("Cooper Black", 20), bg="#FFCC01", fg="#0070B6", command=options, width=10)#search button will lead you to the option function
     search_button.place(x=600, y=350)


def game_content():#pokemon games page as function
    for widget in main_frame.winfo_children():
        widget.destroy()

    game_img_path = "C:\\Users\\eriel\\Desktop\\pokemon app\\gamebg.png"#image path of the backgrounnd image
    game_bg = Image.open(game_img_path).resize((1500, 800))
    game_photo = ImageTk.PhotoImage(game_bg)

    game_label = tk.Label(main_frame, image=game_photo)
    game_label.image = game_photo  
    game_label.place(x=0, y=0, relwidth=1, relheight=1) #setting it as the background


    canvas = tk.Canvas(main_frame, bg="#FFCC01", bd=0, highlightthickness=0, relief="flat")#canvas to add scrollable content
    scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)#scrollbar to add all the data of the game
    scrollable_frame = tk.Frame(canvas, bg="#FFCC01")#placing scrollable content in the canvas

    scrollable_frame.bind(#resizing the scrollabbble frame which allows the scrollbar to adjst
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")#addin scollable frame to the canvas position
    canvas.configure(yscrollcommand=scrollbar.set)#adding a scrollbar

    games = pokemon_games()#storing game from the fetched data
    if not games:
        return

    for game in games:
        game_name = game['name'].replace("-", " ").capitalize()#getting the games and removing the comma from the data
        game_label = tk.Label(scrollable_frame, text=game_name, font=("Cooper Black", 30), bg="#FFCC01", fg="#0070B6")#displaying the game data
        game_label.pack(anchor="w", padx=10, pady=5)#placing the games

    canvas.place(relx=0.5, rely=0.72, height=700, width=700, anchor="center")#placement and size of the canvas
    scrollbar.place(relheight=1, relx=1, anchor="ne")#size of the scrollbar frame



def item_content():#same code as the games_content
    for widget in main_frame.winfo_children():
        widget.destroy()
        
    item_img_path = "C:\\Users\\eriel\\Desktop\\pokemon app\\itembg.png"
    item_bg = Image.open(item_img_path).resize((1500, 800))
    item_photo = ImageTk.PhotoImage(item_bg)

    item_label = tk.Label(main_frame, image=item_photo)
    item_label.image = item_photo  
    item_label.place(x=0, y=0, relwidth=1, relheight=1) 

    canvas = tk.Canvas(main_frame, bg="#FFCC01", bd=0, highlightthickness=0, relief="flat")
    scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#FFCC01")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    items = pokemon_items()
    if not items:
        return

    for item in items:
        item_name = item['name'].replace("-", " ").capitalize()  
        item_label = tk.Label(scrollable_frame, text=item_name, font=("Cooper Black", 30), bg="#FFCC01", fg="#0070B6")
        item_label.pack(anchor="w", padx=10, pady=5)

    canvas.place(relx=0.5, rely=0.72, height=700, width=700, anchor="center") 
    scrollbar.place(relheight=1, relx=1, anchor="ne") 



def location_content():#same code as the games_content
    for widget in main_frame.winfo_children():
        widget.destroy()

    location_img_path = "C:\\Users\\eriel\\Desktop\\pokemon app\\locationbg.png"
    location_bg = Image.open(location_img_path).resize((1500, 800))
    location_photo = ImageTk.PhotoImage(location_bg)


    location_label = tk.Label(main_frame, image=location_photo)
    location_label.image = location_photo  
    location_label.place(x=0, y=0, relwidth=1, relheight=1)  


    canvas = tk.Canvas(main_frame, bg="#FFCC01", bd=0, highlightthickness=0, relief="flat")
    scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#FFCC01")

 
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )


    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)


    locations = pokemon_location()
    if not locations:
        return


    for location in locations:
        location_name = location['name'].replace("-", " ").capitalize()
        location_label = tk.Label(scrollable_frame, text=location_name, font=("Cooper Black", 30), bg="#FFCC01", fg="#0070B6")
        location_label.pack(anchor="w", padx=10, pady=5)


    canvas.place(relx=0.5, rely=0.72, height=700, width=700, anchor="center")  
    scrollbar.place(relheight=1, relx=1, anchor="ne") 

start_screen() #calling the start_screen function to start the application

root.mainloop()

