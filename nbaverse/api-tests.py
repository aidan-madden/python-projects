import json
import requests

url = "https://api-nba-v1.p.rapidapi.com/players/league/standard"

headers = {
    'x-rapidapi-host': "api-nba-v1.p.rapidapi.com",
    'x-rapidapi-key': "4c35093009mshbfaeb92ef632ff8p108b6ejsnbce105f84548"
    }

response = requests.get(url, headers=headers)
jsonResponse = response.json()

for player in jsonResponse["api"]["players"]:
    if player["teamId"] != None and player["dateOfBirth"] >= '1977-01-01' and player["yearsPro"] >= '1' and player["leagues"]["standard"]["active"]=='1':
        print(f'{player["firstName"]} \n')
        print(f'{player["lastName"]} \n')
        print(f'{player["weightInKilograms"]} \n')
        json_height = player["heightInMeters"]
        print(f'{json_height}')
        height_str = str(json_height)
        print(f'{height_str}')
        height = float(height_str)
        print(f'{height}')
        print(f'{player["country"]} \n')
        print(f'{player["collegeName"]} \n')
        print(f'{player["yearsPro"]} \n')
        print(f'{player["leagues"]["standard"]["pos"]} \n')
        print(f'{player["leagues"]["standard"]["jersey"]} \n')
        print(f'{player["teamId"]}\n')
