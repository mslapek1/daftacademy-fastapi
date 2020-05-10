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


# Wykład 3 - libraries
from hashlib import sha256
from fastapi import FastAPI, HTTPException, Depends, status, Response, Cookie, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import RedirectResponse
import secrets
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse

templates = Jinja2Templates(directory="html")

app.secret_key = "Mariusz"
security = HTTPBasic()
app.sessions = {}


# Wykład 3 - zadanie 1 i 4

@app.get('/welcome/')
def hi(request: Request, session_token: str = Cookie(None)):
	if session_token not in app.sessions:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Error", headers={"WWW-Authenticate": "Basic"},)

	return templates.TemplateResponse("hi.html", {"request": request, "user": "trudnY"})

# Wykład 3 - zadanie 2


@app.post("/login")
def ex2(cred: HTTPBasicCredentials = Depends(security)):
    username = secrets.compare_digest(cred.username, "trudnY")
    password = secrets.compare_digest(cred.password, "PaC13Nt")

    if not username or not password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong data", headers={"WWW-Authenticate": "Basic"},)

    session_token = sha256(bytes(f"{cred.username}{cred.password}{app.secret_key}", "utf8")).hexdigest()

    app.sessions[session_token] = cred.username

    response: RedirectResponse = RedirectResponse("/welcome", 302)
    response.set_cookie(key="session_token", value=session_token)

    return response


# Wykład 3 - zadanie 3

@app.post("/logout")
def ex3(response: Response, session_token: str = Cookie(None)):
	if session_token not in app.sessions:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Error", headers={"WWW-Authenticate": "Basic"},)

	response = RedirectResponse(url="/", status_code=302)
	response.delete_cookie(key="session_token", path="/")
	return response 

 # Wykład 3 - zadanie 5

app.list_patients = []

@app.post("/patient")
def patient_position(response: Response, pt: Name, session_token: str = Cookie(None)):
	if not session_token is None: 
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
	id = len(app.list_patients)
	app.list_patients.append(pt)
	response = RedirectResponse(f"/patient/{id}", status_code=status.HTTP_302_FOUND)
	return response

@app.get("/patient")
def all(session_token: str = Cookie(None)):
	if session_token is None:
		response.status_code = status.HTTP_401_UNAUTHORIZED
		return MESSAGE_UNAUTHORIZED
	if len(app.patients) != 0:
		return app.patients

	response.status_code = status.HTTP_204_NO_CONTENT

@app.get("/patient/{pk}")
def get(pk: int, session_token: str = Cookie(None)):
	if session_token is None:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Error", headers={"WWW-Authenticate": "Basic"},)
	if pk not in app.list_patients:
		response.status_code = status.HTTP_204_NO_CONTENT

	return app.list_patients[pk]

@app.delete("/patient/{pk}")
def del_patient(response: Response, pk: int, session_token: str = Cookie(None)):
	if session_token is None:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Error", headers={"WWW-Authenticate": "Basic"},)	
	if pk in app.list_patients:
		app.list_patients.pop(pk)
	
	response.status_code = status.HTTP_204_NO_CONTENT

# Wykład 4 - zadanie 1


import sqlite3
from fastapi import APIRouter, HTTPException, status, Response
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

@router.on_event("startup")
async def startup():
    router.db_connection = sqlite3.connect('chinook.db')
    router.db_connection.row_factory = sqlite3.Row

@router.on_event("shutdown")
async def shutdown():
    router.db_connection.close()


@router.get("/tracks")
async def tracks(page: int = 0, per_page: int = 10):
	offset = page * per_page
	cursor = router.db_connection.cursor()

	out  = cursor.execute(
    	"""SELECT * 
           FROM tracks 
           ORDER BY TrackId 
           LIMIT ? 
           OFFSET ?""", (per_page, offset)
    ).fetchall()

	return out