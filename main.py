from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

patients = {}
# ex1

@app.get('/')
def hello_world():
	return {"message": "Hello World during the coronavirus pandemic!"}

# ex2

@app.get('/method/')
def get_method():
	return {"method": "GET"}

@app.post('/method/')
def get_method():
	return {"method": "POST"}

@app.put('/method/')
def get_method():
	return {"method": "PUT"}

@app.delete('/method/')
def get_method():
	return {"method": "DELETE"}

# ex3

class Name(BaseModel):
    name: str
    surename: str
	
class Patient(BaseModel):
    id: int
    patient: Name
	
@app.post('/patient/')
def add_person(name: Name):
	id_act = len(patients)
	patients[id_act] = name
	

	return Patient(id=id_act, patient=name)
	
# ex4

@app.get('/patient/{pk}')
def get_person(pk: int):
	if pk in patients.keys():
		return patients[pk]
	else:
		raise HTTPException(status_code=204, detail="Patient doesn't exists")

