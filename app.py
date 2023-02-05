from fastapi.params import Form
from fastapi import FastAPI,Request, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from markupsafe import re
import starlette.status as status
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import RedirectResponse, Response
import starlette.status as status
from typing import Optional 
from dbcontroller import DBController

app = FastAPI()

app.mount("/static",StaticFiles(directory="static"),"static")

templates = Jinja2Templates("templates")

db = DBController("app.db")


@app.get("/", response_class=HTMLResponse)
def index(request:Request):
    return templates.TemplateResponse("page1.html",{"request":request})

@app.post("/Fregister",response_class=HTMLResponse)
def create_post(request:Request, name:str = Form(...),department:str = Form(...),contact_number:int = Form(...), date_of_birth:str = Form(...), email:str = Form(...), teachers_id:int = Form(...), password:str = Form(...), photo:str = Form(...)):
    data = {"name":name, "department":department, "contact_number":contact_number, "date_of_birth":date_of_birth, "email":email,"teachers_id":teachers_id, "password":password, "photo":photo}
    if(db.insert("addteachers",data=data)):
        return templates.TemplateResponse("Fregister.html",{"request":request,"msg":"Account created successfully!!"})
    return templates.TemplateResponse("Fregister.html",{"request":request,"msg":"Unable to create account"})

@app.post("/register",response_class=HTMLResponse)
def create_post(request:Request, name:str = Form(...),contact_number:str = Form(...), email:str = Form(...), date:str = Form(...), time:str = Form(...), whom_to_meet:str = Form(...),  purpose:str = Form(...), reason:str = Form(...), photo:str = Form(...)):
    data = {"name":name, "contact_number":contact_number, "email":email, "date":date, "time":time, "whom_to_meet":whom_to_meet,  "purpose":purpose, "reason":reason, "photo":photo}
    if(db.insert("register1",data=data)):
        return templates.TemplateResponse("register.html",{"request":request,"msg":"Registered successfully"})
    return templates.TemplateResponse("register.html",{"request":request,"msg":"Unable to register"})

@app.post("/",response_class=HTMLResponse)
def index_post(request:Request, email:str = Form(...), password:str=Form(...)):
    users = db.executeQueryWithParams("select * from users where email = ? and password = ?",[email,password])
    request.session.setdefault("isLogin", True)
    request.session.setdefault('email', users['email'])
    request.session.setdefault('uid', users['id'])
    return RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    if(len(row)==0):
        return templates.TemplateResponse("login2.html",{"request":request, "msg":"invalid email and password" })
    return RedirectResponse("/FFdashboard",status_code=status.HTTP_302_FOUND)


@app.get("/Tdashboard", response_class=HTMLResponse)
def create(request:Request, status:str=Query(None),id:int=Query(None)):
    print(status)
    if status != None:
        db.executeQueryWithParams("UPDATE register1 set status = ? where id =? ",[status,id])
    orders = db.executeQuery("select * from register1")
    return templates.TemplateResponse("Tdashboard.html",{"request":request, "orders": orders})



@app.get("/FFdashboard", response_class=HTMLResponse)
def create(request:Request, status:str=Query(None),id:int=Query(None)):
    print(status)
    if status != None:
        db.executeQueryWithParams("UPDATE register1 set status = ? where id =? ",[status,id])
    orders = db.executeQuery("select * from register1")
    return templates.TemplateResponse("FFdashboard.html",{"request":request, "orders": orders})


@app.get("/Fregister", response_class=HTMLResponse)
def create(request:Request):
    return templates.TemplateResponse("Fregister.html",{"request":request})

@app.get("/others", response_class=HTMLResponse)
def create(request:Request):
    return templates.TemplateResponse("others.html",{"request":request})

@app.get("/login2", response_class=HTMLResponse)
def create(request:Request):
    return templates.TemplateResponse("login2.html",{"request":request})

@app.get("/page1", response_class=HTMLResponse)
def create(request:Request):
    return templates.TemplateResponse("page1.html",{"request":request})

@app.get("/visitor1", response_class=HTMLResponse)
def create(request:Request):
    return templates.TemplateResponse("visitor1.html",{"request":request})

@app.get("/register", response_class=HTMLResponse)
def create(request:Request):
    teachers = db.executeQuery("select * from addteachers")
    return templates.TemplateResponse("register.html",{"request":request, "teachers": teachers})

@app.get("/FFdashboard#Apersonal", response_class=HTMLResponse)
def events(request: Request):
    orders =db.executeQuery("select * from register1 where {{orders.purpose}} = personal")
    return templates.TemplateResponse("FFdashboard.html", {"request": request, "orders":orders})








