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


# Wykład 3 - zadanie 1

@app.get('/')
@app.get('/welcome/')
def hello_world():
	return {"message": "Hello World during the coronavirus pandemic!"}

# Wykład 3 - zadanie 2

from hashlib import sha256
from fastapi import FastAPI, HTTPException, Depends, status, Response, Cookie
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import RedirectResponse
import secrets

app.secret_key = "Mariusz"
security = HTTPBasic()

@app.post('/login')
def login(cred: HTTPBasicCredentials = Depends(security)):
    username  = secrets.compare_digest(cred.username, 'trudnY')
	password = secrets.compare_digest(cred.password, 'PaC13Nt')

	if not (username and password):
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED, 
			detail='Wrong data', 
			headers={"WWW-Authenticate": "Basic"},
			)


	session_token = sha256(bytes(f"{cred.username}{cred.password}{app.secret_key}", encoding='utf8')).hexdigest()	

    response: RedirectResponse = RedirectResponse("/welcome", 302)
    response.set_cookie(key='session_token', value=session_token)

    return response