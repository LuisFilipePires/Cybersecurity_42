
'''
from https://www.youtube.com/watch?v=JVQNywo4AbU
 Request API data using Python in 8 minutes!
chanel: Bro code
'''
#exmample site : https://pokeapi.co/


import requests

base_url = "https://pokeapi.co/api/v2/"

def get_pokemon_info(name):
    url = (f"{base_url}/pokemon/{name}")
    response = requests.get(url)
    #print (response)
    if response.status_code == 200:
        print (f"Data retrieved!")
        pokemon_data = response.json()
        #print(pokemon_data) #it prints a huge taill of information data
        #extremely large dictionary
        return(pokemon_data)
    else:
        print(f"Failed to retrieve data {response.status_code}")


pokemon_name = "pikachu"
pokemon_info = get_pokemon_info(pokemon_name)

if pokemon_info:
    print(f"Name: {pokemon_info['name'].capitalize()}")
    print(f"Id: {pokemon_info['id']}")
    print(f"Weight: {pokemon_info['weight']}")
    print(f"Height: {pokemon_info['height']}")