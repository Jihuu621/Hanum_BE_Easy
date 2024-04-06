# 라이브러리 import하는 부분

from fastapi import FastAPI
from sqlalchemy import create_engine, Table, MetaData, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base
from pydantic import BaseModel
from typing import List, Optional

base = declarative_base()
app = FastAPI()


# 데이터베이스 URL
DATABASE_URL = "mysql://root:qwojomoq1004@localhost/todo_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

metadata = MetaData()

# DB에서 todos 테이블 가져오기
todos = Table('todos', metadata, autoload_with=engine)


# 모델 선언
class TodoBase(BaseModel):
    id: int
    content: str
    completed: bool

class TodoUpdate(BaseModel):
    completed: int

class TodoPost(BaseModel):
    id: Optional[int] = None # Int일수도 있고 None일수도 (아닐수도) 있습니다
    content: str

class AltTodo(base):
    __tablename__ = 'todos' # 테이블 이름은 todos

    id = Column(Integer, primary_key=True, index=True, autoincrement=True) # primary_key, 고유한 값을 가짐. index, 인덱스 생성함, audoincrement, 생성할때마다 자동으로 값 상승
    content = Column(String, index=True) 
    completed = Column(Boolean, default=False)



# 여기서부터 작동하는 부분

@app.get("/todos", response_model=List[TodoBase])
def get_todo():
    db = SessionLocal()
    try:
        # todos 테이블의 모든 항목 가져오기
        todo = db.query(todos).all()
        return todo
    finally:
        db.close()

@app.patch("/todos/{todoId}") 
def patch_todo(todoId: int, newtodo: TodoUpdate): # url에서 todoID값 받아오고, request로 newtod 받아오기
    db = SessionLocal()
    try:
        # todoId로 레코드 찾고 completed 필드 업데이트하기
        db.query(todos).filter_by(id=todoId).update({'completed': int(newtodo.completed)})
       
        db.commit()

        # 커밋 후 db 내에 new와 dirty값이 존재할 시 문제가 발생한 것. 없을 시 성공적으로 patch 완료.

        if not db.new and not db.dirty:
            success = True

        return {"success" : success} # succ 변수는 0과 1의 정수이므로 bool로 변환


    finally:
        db.close()

@app.post("/todos")
def post_todo(newtodo: TodoPost):
    db = SessionLocal()
    try:
        todo = AltTodo(
            content=newtodo.content, 
            completed=False
        )
        
        db.add(todo)

        db.commit()

         # 커밋 후 db 내에 new와 dirty값이 존재할 시 문제가 발생한 것. 없을 시 성공적으로 patch 완료.

        if not db.new and not db.dirty:
            success = True

        return {"success" : success} 

    finally:
        db.close()


@app.delete("/todos/{todoId}")
def delete_todo(todoId: int): # url에서 todoID값 받아오기
    db = SessionLocal()
    try:
        # db에서 todoId값으로 레코드 찾은 후 지워버리기
        db.query(todos).filter_by(id=todoId).delete()

       
        db.commit()

        # 커밋 후 db 내에 new와 dirty값이 존재할 시 문제가 발생한 것. 없을 시 성공적으로 patch 완료.

        if not db.new and not db.dirty:
            success = True

        return {"success" : success} # succ 변수는 0과 1의 정수이므로 bool로 변환


    finally:
        db.close()


# 끝났다!!!!!!!!!!!!!!!!!