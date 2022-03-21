from flask_restful import Resource, Api
from picamera import PiCamera
from dataclasses import dataclass
from time import sleep
from uuid import uuid4
import json
from flask import Flask, request, jsonify, redirect
from sqlalchemy import Column, Text, DateTime, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import func





Base = declarative_base()
metadata = Base.metadata
engine = create_engine('sqlite:///pictureDB.db', echo=True)
db_session = scoped_session(sessionmaker(autocommit=True, autoflush=True, bind=engine))
Base.query = db_session.query_property()
app = Flask(__name__)
api = Api(app)

@dataclass
class pictureDB(Base):
    __tablename__ = 'binary_with_metadata'
    id: str
    name: str
    description: str
    who: str
    date: str
    data: str

    id = Column(Text, primary_key=True)
    name = Column(Text)
    description = Column(Text)
    who = Column(Text)
    date = Column(DateTime, default=func.now())
    data = Column(Text)


class pictureDBREST(Resource):
    def get(self, id):
        info = pictureDB.query.get(id)
        return jsonify(info)

    def put(self):
        data = request.get_json(force=True)
        print(data)
        info = pictureDB(name=data['name'], description=data['description'],who=data['who'], data=data['data'])
        db_session.add(info)
        db_session.flush()
        return jsonify(info)

    def delete(self, id):
        info = pictureDB.query.get(id)
        db_session.delete(info)
        db_session.flush()
        return jsonify("message " + id + " deleted")

    def patch(self, id):
        info = pictureDB.query.get(id)
        data = json.loads(request.json['info'])
        if 'name' in data:
            info.question = data['name']

        if 'description' in data:
            info.question = data['description']

        if 'who' in data:
            info.question = data['who']

        if 'data' in data:
            info.question = data['data']

        db_session.add(info)
        db_session.flush()
        return (id + " modified")


api.add_resource(pictureDBREST, '/picture_meta/<int:id>')
@app.teardown_appcontext
def shutdown_session(exception=None):
    print("Shutdown Session")
    db_session.remove()


# sqlite stuff:
def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', debug=True)  # host ip #raspberry ip zuhause: 10.0.0.69
