# Form validation
import wtforms
from wtforms.validators import length, email, equal_to, input_required

from models import EmailCaptchaModel, UserModel


class RegisterForm(wtforms.Form):
    email = wtforms.StringField(validators=[email()])
    captcha = wtforms.StringField(validators=[length(min=4, max=4)])
    username = wtforms.StringField(validators=[length(min=3, max=20)])
    password = wtforms.StringField(validators=[length(min=6, max=20)])
    password_confirm = wtforms.StringField(validators=[equal_to('password')])

    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        captcha_model = EmailCaptchaModel.query.filter_by(email=email).first()
        if not captcha_model or captcha_model.captcha.lower() != captcha.lower():
            raise wtforms.ValidationError('邮箱验证码错误')

    def validate_email(self, field):
        email = field.data
        user = UserModel.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError('邮箱已注册')


class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[email()])
    password = wtforms.StringField(validators=[length(min=6, max=20)])


class QuestionForm(wtforms.Form):
    title = wtforms.StringField(validators=[length(min=1, max=200)])
    content = wtforms.StringField(validators=[length(min=1)])


class AnswerForm(wtforms.Form):
    answer = wtforms.TextAreaField(validators=[length(min=1)])
    # question_id = wtforms.IntegerField(validators=[input_required()])




