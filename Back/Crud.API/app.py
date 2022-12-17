from fastapi import FastAPI
from dotenv import load_dotenv
from os.path import join, dirname
from peewee import *
import uvicorn
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
    extra_info = TextField(null=True)

    class Meta:
        database = db
        database_table = 'predict'


app = FastAPI(title="XMAS HACK - 'MISIS AI LAB' team")


@app.post("/insert_doctype",
          description="Создать новый тип документа в базе данных")
def insert_doctype(type_name: str):
    try:
        document_type.delete().where(document_type == type_name).execute()
        doctype = document_type()
        doctype.name = type_name
        doctype.save()
    except Exception as e:
        return {"Error": str(e)}
    return {
        "Message": "Successful",
        "doctype_id": doctype.id, "type_name": type_name
    }


@app.post("/save_predict", description=("Сохранить предсказание модели"
                                        "(указывается ID типа либо имя типа)"
                                        "для документа"))
def save_predict(document_id, extra_info: str,
                 type_id=None, type_name: str = None):
    try:
        predict.delete().where(predict.document_id == document_id).execute()
        pred = predict()
        pred.document_id = document_id
        pred.extra_info = extra_info
        if type_name:
            pred.type_id = document_type.select(document_type.id) \
                .where(document_type.name == type_name)
        elif type_id:
            pred.type_id = type_id
        pred.save()
    except Exception as e:
        print(e)
        return {"status_code": 400, "describe": "Ошибка при сохранении"}
    return {
        "Message": "Successful",
        "pred_id": pred.id,
        "document_id": pred.document_id.id,
        "type_name": type_name
    }


@app.post("/save_doc", description="Сохраняет новый документ")
def save_doc(name: str, path: str):
    try:
        doc = document()
        doc.name = name
        doc.path = path
        doc.save()
    except Exception as e:
        return {"Error": str(e)}
    return {
        "Message": "Successful", "id": doc.id,
        "name": doc.name, "path": doc.path
    }


@app.post("/change_status", description="Изменяет статус")
def change_status(id, status):
    try:
        doc = document()
        doc.id = id
        doc.status = status
        doc.save()
    except Exception as e:
        return {"Error": str(e)}
    return {"Message": "Successful", "id": doc.id}


@app.get("/get_all_docs", description=("Возвращает список всех документов,"
                                       "их параметров и предсказаний модели"))
def get_all_docs():
    docs = document.select()
    data = []
    for doc in docs:
        query = predict.select() \
            .join(document_type, on=(document_type.id == predict.type_id)) \
            .where(predict.document_id == doc.id)

        type_name = None
        if query:
            type_name = query.get().type_id.name

        data.append({
            "id": doc.id,
            "name": doc.name,
            "path": doc.path,
            "status": doc.status,
            "type": type_name
        })
    return {"Message": "Successful", "documents": data}



@app.get("/get_docs", description=("Возвращает документ по id"))
def get_all_docs(id):
    docs = document.select().where(document.id == id)

    if len(docs) == 0:
         return {"Message": "Not found", "document": null}
    else:
        doc = docs[0]
        query = predict.select() \
            .join(document_type, on=(document_type.id == predict.type_id)) \
            .where(predict.document_id == doc.id)

        type_name = None
        if query:
            type_name = query.get().type_id.name

        data = {
            "id": doc.id,
            "name": doc.name,
            "path": doc.path,
            "status": doc.status,
            "type": type_name
        }
    return {"Message": "Successful", "document": data}
    
@app.get("/get_all_types", description=("Возвращает список всех типов документов"))
def get_all_types():
    types = document_type.select()
    data = []
    for type in types:
        data.append({
            "id": type.id,
            "name": type.name,
        })
    return {"Message": "Successful", "types": data}


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)