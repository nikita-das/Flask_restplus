from flask import Flask, request
from flask_restplus import Api, Resource, fields

app = Flask(__name__)
api = Api(app)

name_space = api.namespace('main', description='Main APIs')


model = app.model('Name Model', 
		  {'name': fields.String(required = True, 
					 description="Name of the person", 
					 help="Name cannot be blank.")})
                     
@name_space.route("/")
class MainClass(Resource):
	def get(self):
		return {
			"status": "Got new data"
		}
	def post(self):
		return {
			"status": "Posted new data"
		}


if __name__ == '__main__':
    app.run(debug=True)