import random
import string

from flask import Blueprint, render_template, request, url_for, redirect, jsonify, session, flash
from flask_mail import Message
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from extensions import mail
from models import *
from .forms import RegisterForm, LoginForm

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if not user or not check_password_hash(user.password, password):
                flash('邮箱和密码不匹配！')
                return redirect(url_for('user.login'))

            session['user_id'] = user.id

            return redirect('/')

        else:
            flash('邮箱或者密码格式错误！')
            return redirect(url_for('user.login'))


@bp.route('/logout')
def logout():
    # Clear all session data
    session.clear()
    return redirect(url_for('user.login'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = generate_password_hash(form.password.data)

            user = UserModel(email=email, username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('user.login'))
        else:
            return redirect(url_for('user.register'))


    else:
        return render_template('register.html')


@bp.route('/captcha', methods=['POST'])
def get_captcha():
    email = request.form.get('email')
    print(email)

    if email:
        # Make captcha
        letters = string.ascii_letters + string.digits
        captcha = ''.join(random.sample(letters, 4))

        # Send Mail
        message = Message(
            subject='验证码',
            recipients=[email],
            body=f'【问答系统】您的验证码为: {captcha}, 请不要告诉任何人'
        )
        mail.send(message)

        # Save captcha into db
        captcha_model = EmailCaptchaModel.query.filter_by(email=email).first()
        if captcha_model:
            captcha_model.captcha = captcha
            captcha_model.create_time = datetime.now()
            db.session.commit()
        else:
            captcha_model = EmailCaptchaModel(email=email, captcha=captcha)
            db.session.add(captcha_model)
            db.session.commit()

        print('captcha', captcha)
        return jsonify({'code': 200, })
    else:
        # 400 客户端错误
        return jsonify({'code': 400, 'message': '请先传递邮箱'})
