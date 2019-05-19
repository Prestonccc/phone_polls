from flask import render_template, flash, redirect, url_for, request, jsonify
from app import app, db, admin
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Admins
from werkzeug.urls import url_parse
from datetime import datetime
from app.forms import EditProfileForm
from flask_admin.contrib.sqla import ModelView
from app.models import Post, Phone, Vote


@app.route('/home')
@app.route('/')
def home():
    all_phone = [i.to_dict() for i in Phone.query.all()]

    all_phone = sorted(all_phone, key=lambda i: i['vote_number'], reverse=True)

    all_phone_name = [i['p_name'] for i in all_phone]
    all_phone_data = [i['vote_number'] for i in all_phone]

    all_posts = [i.to_dict() for i in Post.query.all()]

    if current_user.get_id() == None:
        user_name = 'Please Login'
    else:
        user_name = current_user.username
    data = {
        'all_phone_name': all_phone_name,
        'all_phone_data': all_phone_data,
        'all_posts': all_posts,
        'username': user_name
    }
    if not current_user.get_id():
        return render_template('home.html', data=data)
    last_seen = User.query.filter_by(id=current_user.get_id()).first().last_seen
    last_seen = '{}-{}-{} {}:{}:{}'.format(last_seen.year, last_seen.month, last_seen.day, last_seen.hour,
                                           last_seen.minute, last_seen.second)
    return render_template('home.html', last_seen=last_seen, all_phone_name=all_phone_name, data=data)


@app.route('/index')
@login_required
def index():
    vote = Vote.query.filter_by(user_id=current_user.id).all()
    if vote != []:
        flash('You have already voted', 'yes')
        return redirect('/home')
    phones = Phone.query.all()
    phones = [i.to_dict() for i in phones]
    last_seen = User.query.filter_by(id=current_user.get_id()).first().last_seen
    last_seen = '{}-{}-{} {}:{}:{}'.format(last_seen.year, last_seen.month, last_seen.day, last_seen.hour,
                                           last_seen.minute, last_seen.second)
    data = {
        'username': current_user.username,
    }
    return render_template('index.html', title='Home', phones=phones, last_seen=last_seen, user_id=current_user.id,
                           data=data)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'no')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    data = {
        'username': 'Please Login'
    }
    return render_template('login.html', title='Sign In', form=form, data=data)


@app.route('/login_admin', methods=['GET', 'POST'])
def login_admin():
    if request.method == 'GET':
        data = {
            'username': 'Please Login'
        }
        return render_template('admin_login.html', data=data)
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        admin = Admins.query.filter_by(admin_name=username).first()
        if admin is None or not admin.check_password(password):
            flash('Invalid username or password', 'no')
            return redirect(url_for('login_admin'))
        return redirect('/admin')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!', 'yes')
        return redirect(url_for('login'))
    data = {
        'username': 'Please Login'
    }
    return render_template('register.html', title='Register', form=form, data=data)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(user_id=user.id).all()
    res_posts = [i.to_dict() for i in posts]
    data = {
        'username': current_user.username
    }
    return render_template('user.html', user=user, posts=res_posts, data=data)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        username = form.username.data
        about_me = form.about_me.data
        u = User.query.filter(User.username == username).first()
        u.about_me = about_me
        db.session.commit()
        flash('Your changes have been saved.', 'yes')
        return redirect('/user/' + username)
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    data = {
        'username': current_user.username
    }
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form, data=data)


@app.route('/vote', methods=['POST'])
def vote():
    form = request.form
    user_id = form['user_id']
    phone_id = form['phone_id']
    new_vote = Vote(user_id=user_id, phone_id=phone_id)
    db.session.add(new_vote)
    db.session.commit()
    flash('Congratulations on voting success', 'yes')
    return jsonify({'code': '200'})


@app.route('/post', methods=['POST', 'GET'])
def post():
    if request.method == 'GET':
        posts = [i.to_dict() for i in Post.query.all()]
        for i in posts:
            i['author'] = i['author'].username
        return jsonify(posts)

    elif request.method == 'POST':
        form = request.form
        body = form['body']
        anonymous = form['anonymous']
        if anonymous == 'false':
            post = Post(body=body, user_id=current_user.id, timestamp=datetime.now())
        else:
            post = Post(body=body, user_id=0, timestamp=datetime.now())
        try:
            db.session.add(post)
            db.session.commit()
        except BaseException as err:
            return jsonify({'code': '500', 'message': err})
        return jsonify({'code': '200', 'message': 'Post Success!!'})


admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Admins, db.session))
admin.add_view(ModelView(Phone, db.session))
admin.add_view(ModelView(Vote, db.session))
admin.add_view(ModelView(Post, db.session))
