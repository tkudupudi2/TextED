import datetime
import json
import os
import secrets

import flask
import redis
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, make_response, jsonify

from textapp import app, db, bcrypt, mail
from textapp.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm 
from textapp.models import User, Appointment
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
r=''
r=redis.StrictRedis(host='localhost',port=6379,db=1,decode_responses=True)
user_socket_dict={}
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/userhome')
def userhome():
    return render_template('userhome.html', title = 'Home')

@app.route('/about')
def about():
    return render_template('about.html', title = 'About')

@app.route('/classes')
def classes():
    return render_template('classes.html', title = 'Classes')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('userhome'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, major=form.major.data, minor=form.minor.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('userhome'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            flask.session['user']=user.username
            flask.session['email']=user.email
            login_user(user, remember=form.remember.data)
            return redirect(url_for('userhome'))
            return redirect(next_page) if next_page else redirect(url_for('userhome'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.major = form.major.data
        current_user.minor = form.minor.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect (url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.major.data = current_user.major
        form.minor.data = current_user.minor
    image_file = url_for('static', filename = 'profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file = image_file, form = form)

def send_reset_email(user):
    #token = user.get_reset_token()
    body = '''To reset your password, visit the following link:
    {url_for('reset_token', token = token, _external = True)}
    If you did not make this request and simply ignore this email and no changes will be made.
    '''
    msg = Message('Password Reset Request', sender = 'noreply@texted.com', recipients = [user.email],body=body)
    mail.send(msg)

@app.route("/reset_password", methods = ['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title = 'Reset Password', form = form)

@app.route("/reset_password/<token>", methods = ['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect (url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title = 'Reset Password', form = form)

app.secret_key='hard_key'

def event_stream():
    pubsub=r.pubsub()
    pubsub.subscribe('chat')
    for message in pubsub.listen():
        yield 'data:{}\n\n'.format(message['data'])


@app.route('/calendar',methods = ['GET', 'POST'])
def calendar():
    if 'email' not in flask.session:
        return flask.redirect('/login')
    email = flask.session['email']
    if request.method=="GET":
        time = []
        user = User.query.filter_by(email=email).first()
        infos=Appointment.query.filter_by(user=user.id).all()
        if infos:
            for i in infos:
                time.append(i.times)
        return render_template('appointment.html', title = 'Calendar',times=time)
    if request.method=="POST":
        method=request.form.get('method')
        if method:
            time=request.form.get('time')
            user = User.query.filter_by(email=email).first()
            info = Appointment.query.filter_by(user=user.id).all()
            info_text=""
            id=0
            for i in info:
                if i.times==time:
                    info_text=i.infos
                    id=i.id
            return make_response(jsonify({'info':info_text,"id":id}))
        else:
            user = User.query.filter_by(email=email).first()
            time = request.form.get('time')
            type = request.form.get('type')
            info = request.form.get('info')
            print(user,time,type,info)
            if type=='add':
                a=Appointment(user=user.id,times=time,infos=info)
                db.session.add(a)
                db.session.commit()
                return redirect('/calendar')
            if type=='edit':
                id=request.form.get('id')
                info=request.form.get("info")
                appointment = Appointment.query.filter_by(id=int(id)).first()
                appointment.infos=info
                db.session.commit()
                return redirect('/calendar')
@app.route('/send',methods=['POST'])
def sends():
    message=flask.request.form['message']
    user=flask.session.get('user','anonymous')
    now=datetime.datetime.now().replace(microsecond=0).time()
    r.publish('chat','[{}] {} : {}'.format(now.isoformat(),user,message))
    return flask.Response(status=204)


@app.route('/stream')
def stream():
    return flask.Response(event_stream(),mimetype='text/event-stream')


@app.route('/chat')
def chat():
    if 'user' not in flask.session:
        return flask.redirect('/login')
    user=flask.session['user']
    flask.session['user'] = user
    r.publish('chat', 'notice: user {} get into the room!'.format(flask.session['user']))
    return render_template('chat.html', title = 'Chat',user=user)


@app.route("/logout")
def logout():
    if 'user' not in flask.session:
        return flask.redirect('/login')
    user = flask.session['user']
    r.publish('chat', 'notice: user {} quit the room!'.format(user))
    logout_user()
    flask.session.pop('user')
    flask.session.pop('email')
    return redirect(url_for('home'))