from flask import Flask, request, redirect, render_template, session, url_for, flash, jsonify, logging
import logging
import boto3

app = Flask(__name__)
app.logger.setLevel(logging.INFO)
handler = logging.FileHandler('/var/log/apache2/myapp.log')
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)
s3 = boto3.client('s3')
bucket_name = "music-bucket340822"

import utils


@app.route('/')
def root():
    # utils.create_music_table()
    # utils.load_music()
    # utils.create_login_table()
    # utils.load_login_data()
    # utils.load_image_url()
    return render_template(
        'login.html')


@app.route('/login', methods=['GET', "POST"])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    email = request.form['email']
    password = request.form['password']

    user = utils.validate_user(email, password)
    # If the query returned one user entity, redirect to the dashboard
    if user:
        session['email'] = email
        session['user_name'] = user['user_name']
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


@app.route('/forum', methods=['GET', "POST"])
def forum():
    user_name = session.get("user_name")
    return render_template("forum.html", user_name=user_name)
    return redirect(url_for("login"))


@app.route('/logout', methods=['GET', 'POST'])
def logout_():
    del session['email']
    del session['user_name']
    return redirect('/login')


@app.route('/perform-query', methods=['GET'])
def perform_query():
    title = request.args.get('title')
    year = request.args.get('year')
    artist = request.args.get('artist')
    app.logger.info("title: " +title)
    app.logger.info("year: " +year)
    app.logger.info("artist: " +artist)

    response = utils.query_music(title, year, artist)
    if response['Count'] == 0:
        return jsonify({'message': 'No result is retrieved. Please query again.'}), 200
    music_list=[]
    for item in response['Items']:
        music_info = {
            'title': item['title'],
            'year': item['year'],
            'artist': item['artist']
        }
        image_url = item['img_url']
        image_name = image_url.split('/')[-1]
        image_signed_url = s3.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': image_name})
        music_info['image_url'] = image_signed_url
        music_list.append(music_info)

    return jsonify({'music_list': music_list})

    # if no_results:
    #     return jsonify({'message': 'No result is retrieved. Please query again.'}), 200
    # else:
    #     # Construct JSON response containing retrieved music information and corresponding artist images
    #     response = {'music_info': [], 'images': []}
    #     for result in results:
    #         response['music_info'].append({'title': result.title, 'year': result.year, 'artist': result.artist})
    #         response['images'].append(result.artist_image_url)
    #     return jsonify(response), 200


if __name__ == '__main__':
    app.run()
