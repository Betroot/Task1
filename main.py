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
import utils
@app.route('/')
def root():
    utils.create_music_table()
    utils.load_music()
    return render_template(
        'login.html')

@app.route('/login', methods=['GET', "POST"])  # 路由默认接收请求方式位POST，然而登录所需要请求都有，所以要特别声明。
def login():
    if request.method == 'GET':
        return render_template('login.html')

    user_id = request.form['id']
    password = request.form['password']

    user = utils.validate_user(user_id, password)

    # If the query returned one user entity, redirect to the dashboard
    if user:
        session['user_id'] = user_id
        resp = redirect(url_for('forum'))
        return resp
    # If the query returned no or multiple user entities, show an error message
    else:
        error_msg = 'ID or password is invalid'
        return render_template('login.html', error_msg=error_msg)
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
    # app.run(host='127.0.0.1', port=8080, debug=True)
    app.run()

