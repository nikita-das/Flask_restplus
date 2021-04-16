from flask import Flask, request
from flask_restplus import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields as FM
from sqlalchemy import (Text)  
from flask_migrate import Migrate

app = Flask(__name__)

api = Api(app, doc='/docs')

name_space = api.namespace('my_api', description='API Project')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/my_project'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:abcd@localhost/myDB'

db = SQLAlchemy(app)


# model to table Log
class Log(db.Model):
    __tablename__ = 'Log'
    id = db.Column(db.Integer, primary_key=True)
    detail = db.Column(Text)


# will be used to serialize model Log into JSON for API result
class LogSchema(Schema):
    id = FM.Int()
    detail = FM.Str()


# this will be used to add parameter in swagger for inserting/updating record
logSwagger = api.model('Log', {
    'detail': fields.String(required=True, description='Log detail content')
})

schema = LogSchema()


@name_space.route("/")
class LogList(Resource):
    # you can add additional Swagger response information here
    @api.doc(
        responses=
        {
            200: 'OK',
            400: 'Invalid Argument',
            500: 'Mapping Key Error',
        })
    def get(self):
        logs = Log.query.all()
        result = []
        schema = LogSchema()
        for log in logs:
            result.append(schema.dump(log))
        return {
            "data": result
        }

    @name_space.expect(logSwagger)
    def post(self):
        payload = request.get_json()
        log = Log()
        log.detail = payload['detail']
        db.session.add(log)
        db.session.commit()

        return {
            "data": schema.dump(log)
        }


@name_space.route("/<int:id>")
class LogDetail(Resource):
    @api.doc(
        responses=
        {
            200: 'OK',
            400: 'Invalid Argument',
            500: 'Mapping Key Error'
        },
        params=
        {
            'id': 'Id log to get the detail'
        })
    def get(self, id):
        log = Log.query.get(id)
        return {
            "data": schema.dump(log)
        }

    @api.doc(
        responses=
        {
            200: 'OK',
            400: 'Invalid Argument',
            500: 'Mapping Key Error'
        },
        params=
        {
            'id': 'Id log to be updated'
        })
    @name_space.expect(logSwagger)
    def put(self, id):
        payload = request.get_json()
        log = Log.query.get(id)
        log.detail = payload['detail']
        db.session.add(log)
        db.session.commit()
        return {
            "data": schema.dump(log)
        }

    @api.doc(
        responses=
        {
            200: 'OK',
            400: 'Invalid Argument',
            500: 'Mapping Key Error'
        },
        params=
        {
            'id': 'Id log to be removed'
        })
    def delete(self, id):
        log = Log.query.get(id)
        db.session.delete(log)
        db.session.commit()
        return {
            "status": "OK"
        }

if __name__ == '__main__':
    app.run(debug=True)