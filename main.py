from fastapi import FastAPI, HTTPException, Query 
from pydantic import BaseModel
from typing import Optional, Union
import json

app = FastAPI()

class Person(BaseModel):
	id: Optional[int] = None
	name: str
	age: int
	gender: str

with open('people.json', 'r') as f:
	people = json.load(f)

print(people)

@app.get('/person/{p_id}', status_code=200)
def get_person(p_id: int):
	person = [p for p in people if p['id'] == p_id]
	return person[0] if len(person) > 0 else {}

@app.get("/search", status_code=200)
def search_person(age: Optional[int] = Query(None, title="Age", description="The age to filter by"),
								  name: Optional[str] = Query(None, title="Age", description="The name to filter by")):
	if name is None and age is None:
		return people
	else:
		people_age_match = [p for p in people if p['age'] == age]
		people_name_match = [p for p in people if name.lower() in p['name'].lower()]
		return people_age_match + people_name_match

@app.post('/person', status_code=201)
def add_person(person: Person):
	p_id = max([p['id'] for p in people ]) + 1
	new_person = {
		"id": p_id,
		"name": person.name,
		"age": person.age,
		"gender": person.gender
	}
	people.append(new_person)

	with open('people.json', 'w') as f:
		json.dump(people, f)

@app.put('/changePerson', status_code=204)
def change_person(person: Person):
	print(person)
	new_person = {
		"id": person.id,
		"name": person.name,
		"age": person.age,
		"gender": person.gender
	}
	print(new_person)

	person_list = [p for p in people if p['id'] == person.id]
	if len(person_list) > 0:
		people.remove(person_list[0])
		people.append(new_person)
		with open('people.json', 'w') as f:
			json.dump(people, f)
		return new_person
	else:
		return HTTPException(status_code=404, detail=f"Person with id {person.id} does not exist")

@app.delete('/deletePerson/{p_id}', status_code=204)
def delete_person(p_id: int):
	person = [p for p in people if p['id'] == p_id]
	if len(person)> 0:
		people.remove(person[0])
		with open('people.json', 'w') as f:
			json.dump(people, f)
	else:
		return HTTPException(status_code=404, detail=f"Person with id {person.id} does not exist")