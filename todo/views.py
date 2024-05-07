from models import users,todos

session={}                        #session

def login_required(fn):           #decorator function
    def wrapper(*args,**kwargs):
        if "user" in session:
            return fn(*args,**kwargs)
        else:
            print("u must log in")
    return wrapper
        
def authenticate(*args,**kwargs): #authenticate function
    username=kwargs.get("username")
    password=kwargs.get("password")
    user=[user for user in users if user["username"]==username and user["password"]==password]
    return user

class SignInview():               #view for log in
    def post(self,*args,**kwargs):
        username=kwargs.get("username")
        password=kwargs.get("password")
        user=authenticate(username=username,password=password)
        if user:
            user=user[0]
            session["user"]=user
            print("log in successfully")
        else:
            print("invalid credentials")

@login_required
def signout(*args,**kwargs):
    user=session.pop("user")
    print(f"{user['username']} has been loged out")

class ListTodosview():           #view for listing all todos
    @login_required
    def get(self,*args,**kwargs):
        return todos
    
class Newtodosview():            #view for creating new todos
    @login_required
    def post(self,*args,**kwargs):
        userid=session["user"]["id"]
        kwargs["userid"]=userid
        # print(kwargs)
        todos.append(kwargs)
        print(todos)

class Mytodosview():             #view for mytodos 
    @login_required
    def get(self,*args,**kwargs):
        userid=session["user"]["id"]
        todo=[todo for todo in todos if todo["userid"]==userid]
        return todo

class DetailsTodoview():         
    
    @login_required              
    def get_object(self,id):      #function to get specific todo
        todo=[todo for todo in todos if todo["todosid"]==id]
        if todo:
            todo=todo[0]
            return todo
        
    @login_required               
    def get(self,*args,**kwargs):  #view for specific todo
        todosid=kwargs.get("todosid")
        todo=self.get_object(todosid)
        return todo
    
    @login_required
    def put(self,*args,**kwargs):  #view to update a todo
        todosid=kwargs.get("todosid")
        data=kwargs.get("data")
        todo=self.get_object(todosid)
        todo.update(data)
        return todo
    
    @login_required
    def delete(self,*args,**kwargs): #view to delete a todo
        todosid=kwargs.get("todosid")
        todo=self.get_object(todosid)
        todos.remove(todo)
        print(todos)
        print(len(todos))

sign=SignInview()
sign.post(username="vinu",password="password@123")
# list_todos=ListTodosview()
# print(list_todos.get())
# newtodo=Newtodosview()
# newtodo.post(todoid=9,task="houseloanpay",completed=False)
# mytodo=Mytodosview()
# print(mytodo.get())
data={
    "task":'newspaperbill',
    "completed":True,
}
# detail=DetailsTodoview()
# print(detail.get(todosid=8))
# print(detail.put(todosid=5,data=data))
# detail.delete(todosid=7)
logout=signout()