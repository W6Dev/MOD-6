import pandas as pd
import json
from CRUD import AnimalShelter

db = AnimalShelter()

df = pd.read_csv('aac_shelter_outcomes.csv', sep=',')

data = df.to_json('output.json', orient="records", indent= 1)

with open('output.json') as json_file:
    dat = json.load(json_file)


for lp in range(10000):
    print(dat[lp])
    db.Create(dat[lp])
    #print(type(dat))