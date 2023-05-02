from flask import Flask, request, redirect, render_template, session, url_for, flash, jsonify, logging
import logging

app = Flask(__name__)
app.logger.setLevel(logging.INFO)
handler = logging.FileHandler('/var/log/apache2/myapp.log')
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)

#
# app.secret_key = 'your-secret-key-here'
#
#
import utils


@app.route('/')
def root():
    app.logger.info("this is a info log")
    utils.create_music_table()
    utils.load_music()
    utils.create_login_table()
    utils.load_login_data()
    return render_template(
        'login.html')


@app.route('/login', methods=['GET', "POST"])  # 路由默认接收请求方式位POST，然而登录所需要请求都有，所以要特别声明。
def login():
    if request.method == 'GET':
        return render_template('login.html')

    email = request.form['email']
    password = request.form['password']

    user = utils.validate_user(email, password)
    # If the query returned one user entity, redirect to the dashboard
    if user:
        session['email'] = email
        resp = redirect(url_for('forum'))
        return resp
    # If the query returned no or multiple user entities, show an error message
    else:
        error_msg = 'ID or password is invalid'
        return render_template('login.html', error_msg=error_msg)


@app.route('/register', methods=['GET', "POST"])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        # retrieve the entered values from the form
        email = request.form['email']
        user_name = request.form['user_name']
        password = request.form['password']

        if utils.is_email_exist(email):
            error_message = 'The email already exists'
            return render_template('register.html', error_msg=error_message)

        utils.insert_user(email, user_name, password)
        return redirect(url_for('login'))




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
