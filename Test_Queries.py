from CRUD import AnimalShelter

db = AnimalShelter()

info = db.Read({'$and': [{'sex_upon_outcome': 'Intact Male'},
                         {'$or': [
                             {'breed': {"$regex": "Doberman Pinscher"}},
                             {'breed': {"$regex": "German Shepherd"}},
                             {'breed': {"$regex": "Golden Retriever"}},
                             {'breed': {"$regex": "Bloodhound"}},
                             {'breed': {"$regex": "Rottweiler"}},
                         ]
                         },
                         {
                             '$and': [{'age_upon_outcome_in_weeks': {'$gte': 20, '$lte': 300}}]
                         }]
                })

for i in info:
    print(i)

"""
info = db.Read({'$and': [{'sex_upon_outcome': 'Intact Female'},
                         {'$or': [
                             {'breed': {"$regex": "Newfoundland"}},
                             {'breed': {"$regex": "Chesa"}},
                             {'breed': {"$regex": "Labrador Retriever"}}]
                         },
                         {
                             '$and': [{'age_upon_outcome_in_weeks': {'$gte': 26, '$lte': 156}}]
                         }]
                })

"""
