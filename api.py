from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
import uuid
import boto3
import time
import threading
from multiprocessing import Process

from run_sim import runSim
from run_sim import makeTables


app = Flask(__name__)
api = Api(app)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('apitest')

threads = {}


class Setup(Resource):
    def get(self):

        # Create unique UUDI
        id = uuid.uuid4()

        makeTables(id)

        # TODO add new line to tabe with uuid
        # table.put_item(
        #     Item={
        #         'uuid': id
        #     }
        # )
        id_str = str(id)
        return {'uuid': id_str}, 200  # return data and 200 OK code
    pass


class Status(Resource):
    def post(self):
        parser = reqparse.RequestParser()  # initialize

        parser.add_argument('uuid', required=True, location='args')

        args = parser.parse_args()  # parse arguments to dictionary

        if args['uuid'] in threads:
            if (threads[args['uuid']].is_alive()):
                return {'status': 'Running'}, 200
            else:
                return {'status': 'Finished or not Started'}, 200
        else:
            return {'status': 'Finished or not Started'}, 200
        # try:
        #     response['Item']['uuid']
        #     return 200
        # except:
        #     return 401
    pass


def print_time():
    for x in range(0, 10):
        print(x)
        time.sleep(1)


class Start(Resource):
    def post(self):
        parser = reqparse.RequestParser()  # initialize

        parser.add_argument('uuid', required=True, location='args')

        args = parser.parse_args()  # parse arguments to dictionary
        arg_str = str(args['uuid'])
        threads.update({
            args['uuid']: Process(target=runSim, args = [arg_str])
        })
        threads[args['uuid']].start()
        return 200  # return data with 200 OK
    pass


class Kill(Resource):
    def post(self):
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('uuid', required=True, location='args')
        args = parser.parse_args()  # parse arguments to dictionary

        if args['uuid'] in threads:
            threads[args['uuid']].terminate()
            return 200
        else:
            return {'error': 'Bad uuid or not currently running'}, 400


api.add_resource(Status, '/status')
api.add_resource(Setup, '/setup')
api.add_resource(Start, '/start')
api.add_resource(Kill, '/kill')

if __name__ == '__main__':
    app.run(debug=True)  # run our Flask app
