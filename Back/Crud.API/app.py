from fastapi import FastAPI
import uvicorn
from peewee import *
from dotenv import load_dotenv
from os.path import join, dirname
import os


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


credintials = {
    "host": os.environ.get("POSTGRES_HOST"),
    "port": os.environ.get("POSTGRES_PORT"),
    "user": os.environ.get("POSTGRES_USER"),
    "password": os.environ.get("POSTGRES_PASSWORD"),
    "database": os.environ.get("POSTGRES_DB")
}


db = PostgresqlDatabase(**credintials)
db.connect()


class document(Model):
    id = IntegerField(primary_key=True)
    name = TextField()
    path = TextField()
    status = IntegerField(null=True)
    class Meta:
        database = db
        database_table = 'document'


class document_type(Model):
    id = IntegerField(primary_key=True)
    name = TextField()
    class Meta:
        database = db
        database_table = 'document_type'


class predict(Model):
    id = IntegerField(primary_key=True)
    document_id = ForeignKeyField(document)
    type_id = ForeignKeyField(document_type)
    extra_info = TextField()
    class Meta:
        database = db
        database_table = 'predict'

print(os.environ.get('POSTGRES_DB'))

app = FastAPI(title="XMAS HACK - 'MISIS AI LAB' team")


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/savedoc")
async def save_doc(name: str, path: str):
    try:
        doc = document()
        doc.name = name
        doc.path = path
        doc.save()
    except:
        return {"status_code": 400, "describe": "Ошибка при сохранении"} 
    return {"status_code": 201, "id": doc.id}


@app.get("/changestatus")
async def change_status(id, status):
    try:
        doc = document()
        doc.id = id
        doc.status = status
        doc.save()
    except:
        return {"status_code": 400, "describe": "Ошибка при сохранении"} 
    return {"status_code": 201, "id": doc.id}


@app.get("/getalldocs")
async def get_all_docs():
    docs = document.select()
    data = []
    for doc in docs:
        print(doc.id, doc.name, doc.path, doc.status)
        pred = predict.select(document_type.name) \
            .join(document_type, on=(predict.type_id == document_type.id)) \
            .where(doc.id == predict.document_id)
        print(pred)
        data.append({'id': doc.id,
                     'name': doc.name,
                     'path': doc.path,
                     'status': doc.status})

    return {'documents': data}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)