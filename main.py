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

app.lists = []
app.counter = 0 
app.list_of_patient = []



@app.post("/patient",response_model=Name)
def patient_position(response: Response, pt: Name,session_token: str = Cookie(None)):
	if not session_token in app.sesion_keys: 
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
	app.list_of_patient.append(pt)
	response = RedirectResponse(url=f"/patient/{app.counter}", status_code=302)
	response.set_cookie(key="session_token", value=session_token)
	app.counter += 1
	return response