from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from flask_restx import Api, Resource, fields

client = MongoClient('mongodb://test:test@3.38.94.94', 27017)

client = MongoClient('mongodb://localhost:5000, 27017')

db = client.project

app = Flask(__name__)

api = Api(app,
          version="1.0",
          title="Server Storage Service",
          description="Manage metadata")

ns = api.namespace('metadata', description='Project APIs')
model = api.model('Metadata Model',
                  {
                      'id': fields.String(required=True,
                                          description="ID of the metadata",
                                          help="ID cannot be blank."),
                      'created_datetime': fields.String(required=True,
                                            description="created_datetime of the metadata",
                                            help="cannot be blank."),
                      'inference_result': fields.String(required=False,
                                           description="inference_result of the metadata",
                                           help="can be blank."),
                       'file_path': fields.String(required=False,
                                           description="file_path of the metadata",
                                           help="can be blank."),
                       'type': fields.String(required=False,
                                           description="type of the metadata",
                                           help="can be blank."),
                  })

members = dict()


@ns.route("/")
class MemberList(Resource):
    def get(self):
        """
        returns list of metadata
        """
        data_list = list(db.metadata.find({}, {'_id': False}))
        return data_list

    @ns.expect(model)
    def post(self):
        """
        Adds a new metadata to the list
        """
        body = request.json
        db.metadata.insert_one(body)


@ns.route("/<id>")
class Member(Resource):
    @ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'},
             params={'id': 'Specify the Id associated with the metadata'})
    def get(self, id):
        """
        get a metadata
        """
        data_list = list(db.metadata.find({"id":id}, {'_id': False}))
        return data_list


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)