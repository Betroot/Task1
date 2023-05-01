import copy
import datetime
import json
import uuid

from flask import Flask, request, redirect, render_template, session, url_for, flash, jsonify

import boto3

# # [END gae_python3_datastore_store_and_fetch_times]
# # [END gae_python38_datastore_store_and_fetch_times]
app = Flask(__name__)
#
# app.secret_key = 'your-secret-key-here'
#
#
# def create_user_table(dynamodb=None):
#     if not dynamodb:
#         dynamodb = boto3.resource('dynamodb',
#                                   endpoint_url="http://localhost:8000")
#     table = dynamodb.create_table(
#         TableName='login',
#         KeySchema=[
#             {
#                 'AttributeName': 'email',
#                 'KeyType': 'HASH'
#             },
#             {
#                 'AttributeName': 'user_name',
#                 'KeyType': 'RANGE'
#             }
#         ],
#         AttributeDefinitions=[
#             {
#                 'AttributeName': 'email',
#                 'AttributeType': 'S'
#             },
#             {
#                 'AttributeName': 'user_name',
#                 'AttributeType': 'S'
#             },
#             {
#                 'AttributeName': 'password',
#                 'AttributeType': 'S'
#             }
#         ],
#         ProvisionedThroughput={
#             'ReadCapacityUnits': 10,
#             'WriteCapacityUnits': 10
#         }
#     )
#     return table
#
#
# [START gae_python38_datastore_render_times]
# [START gae_python3_datastore_render_times]
@app.route('/')
def root():
    #create_user_table()
    return render_template(
        'login.html')

#
# @app.route('/user', methods=['GET', "POST"])
# def user():
#     return render_template("user.html")
#
#
# # @app.route('/index')
# # def index():
# #     user_info = session.get('user_id')
# #     if not user_info:
# #         return redirect('/login')
# #     return 'hello'
#
#
# @app.route('/logout', methods=['GET', 'POST'])
# def logout_():
#     del session['user_id']
#     return redirect('/login')
#
#
# def index():
#     user_info = session.get('user_id')
#     if not user_info:
#         return redirect('/login')
#     return 'hello'


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.

    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)

