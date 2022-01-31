from os import listdir, path
import shutil
from flask import current_app as app
from flask import render_template, redirect, url_for, flash, send_file, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user, LoginManager
from functools import wraps
import pandas as pd
import logging
from logging import Formatter, FileHandler
from werkzeug.utils import secure_filename

from . import db, classes
from .backend.predict import predict, save_to_csv
from .models import User, Predictions
from .forms import RegistrationForm, LoginForm, CreationForm, DeleteForm, ModelForm
from .backend.preprocessing import remove_tempfile

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.login_view = 'login'
login_manager.login_message_category = "success"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def load_all_users():
    return User.query.all()


def admin_required(func):
    """
    Modified login_required decorator to restrict access to admin group.
    """

    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.admin != 1:  # one means admin
            flash("Only admin user can access this resource.", category="error")
            return redirect(url_for("login"))
        return func(*args, **kwargs)

    return decorated_view


def permission_required(func):
    """
    Modified login_required decorator to restrict access to active users group.
    """

    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.active == 0:
            flash("Your account is inactive, please contact admin.", category="error")
            return redirect(url_for("login"))
        return func(*args, **kwargs)

    return decorated_view


@app.route('/')
def index():
    return render_template('home/index.html')


@permission_required
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user.admin == 1:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))
        elif user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('return_model'))
        flash("Please check your login details and try again.", category="info")
        return redirect(url_for('login'))
    return render_template('users/login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            flash('Usename or email already exist.', category="info")
            return redirect(url_for('signup'))
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data,
                        password=hashed_password, active=1, admin=0)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('success_signup'))
    return render_template('users/signup.html', form=form)


@app.route('/dashboard')
@login_required
@admin_required
def dashboard():
    return render_template('home/dashboard.html', name=current_user.username)


@app.route('/success_signup')
def success_signup():
    return render_template('users/success_signup.html')


@app.route('/model', methods=['GET', 'POST'])
@login_required
@permission_required
def return_model():
    remove_tempfile()
    form = ModelForm()
    files_names = []
    if form.validate_on_submit():
        for file in form.files.data:
            if len(form.files.data) > 20:
                flash('Max upload (20) reached', category="info")
                return redirect(url_for('return_model'))
            file_name = secure_filename(file.filename)
            file.save(path.join(app.config['UPLOAD_PATH'], file_name))
            files_names.append(path.join(app.config['UPLOAD_PATH'], file_name))
        sentences = form.sentence.data
        sentences = sentences.splitlines()
        if len(files_names) != len(sentences):
            flash('Please provide the same length !', category="info")
            return redirect(url_for('return_model'))
        data = {'text': sentences, 'filename': files_names}
        df = pd.DataFrame(data)
        df.to_csv('app/backend/dataset.csv', encoding="utf-8", header='True')
        flash(f'Uploads image(s) and text(s) are ready !', category="success")
    files = listdir(app.config["UPLOAD_PATH"])
    shutil.copytree("uploads", "app/uploads", dirs_exist_ok=True)
    return render_template('models/model.html', form=form, files=files)


@app.route('/uploads/<filename>')
def uploads(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)


@app.route('/predict', methods=['GET', 'POST'])
@login_required
@permission_required
def prediction():
    df = pd.read_csv("app/backend/dataset.csv", index_col=[0], encoding='utf-8')
    predictions = predict(df)
    result = save_to_csv(df, predictions)
    for index, row in result.iterrows():
        prediction = Predictions(image=str(row['filename']), sentence=str(row['text']),
                                 label1=str(row['Cat_1']), label2=str(row['Cat_2']), label3=str(row['Cat_3']))
        db.session.add(prediction)
        db.session.commit()
    result[["Cat_1", "Cat_2", "Cat_3"]] = result[["Cat_1", "Cat_2", "Cat_3"]] \
        .apply(lambda x: x.map(classes))
    flash('Predictions saved !', category="success")
    return render_template('models/predictions.html',
                           tables=[result.to_html(classes='data')],
                           titles="classes")


@app.route('/create_user', methods=['GET', 'POST'])
@login_required
@admin_required
def create_user():
    form = CreationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            flash('Usename or email already exist.', category="info")
            return redirect(url_for('create_user'))
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password,
                        active=form.active.data, admin=form.admin.data)
        db.session.add(new_user)
        db.session.commit()
        flash("User successfully created", "success")
        return redirect(url_for('create_user'))
    return render_template('users/user_management.html', form=form)


@app.route('/delete_user', methods=['GET', 'POST'])
@login_required
@admin_required
def delete_user():
    form = DeleteForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or user.username == "superadmin":
            flash("Username or email doesn't exist. / Either, you can't remove superadmin user", category="info")
            return redirect(url_for('delete_user'))
        db.session.delete(user)
        db.session.commit()
        flash("User successfully deleted", "success")
        return redirect(url_for('delete_user'))
    return render_template('users/user_delete.html', form=form)


@app.route("/list_user")
@login_required
@admin_required
def list_user():
    users = load_all_users()
    return render_template("users/users_list.html", userlist=users)


@app.route("/download_db")
@login_required
@admin_required
def download_db():
    path = "database/database.db"
    return send_file(path, as_attachment=True)


@app.route("/download_predict")
@login_required
def download_predict():
    path = "./predictions/results.csv"
    return send_file(path, as_attachment=True)


@app.route('/logout')
def logout():
    logout_user()
    flash("You are not logged for now...", "logout")
    return redirect(url_for('index'))


@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


if not app.debug:
    file_handler = FileHandler('app/logs/error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')
