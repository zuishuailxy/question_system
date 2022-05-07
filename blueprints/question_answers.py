from flask import Blueprint, render_template, request, g, redirect, url_for, flash
from helper import login_required
from .forms import QuestionForm, AnswerForm
from models import QuestionModel, AnswerModel
from extensions import db
from sqlalchemy import or_

bp = Blueprint('qa', __name__, url_prefix='/')


@bp.route('/')
def index():
    questions = QuestionModel.query.order_by(db.text('-create_time')).all()
    return render_template('index.html', questions=questions)


@bp.route('/question/publish', methods=['GET', 'POST'])
@login_required
def publish_question():
    if request.method == 'GET':
        return render_template('publish.html')
    else:
        form = QuestionForm(request.form)
        print(form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            question = QuestionModel(title=title, content=content, author=g.user)

            db.session.add(question)
            db.session.commit()

            flash('问题发布成功')
            return redirect('/')
        else:
            flash('标题或内容格式错误')
            return redirect(url_for('qa.publish_question'))


@bp.route('/question/<int:question_id>')
@login_required
def question_detail(question_id):
    question = QuestionModel.query.get(question_id)
    return render_template('detail.html', question=question)


@bp.route('/answer/<int:question_id>', methods=['POST'])
@login_required
def question_answer(question_id):
    form = AnswerForm(request.form)
    print(question_id)
    if form.validate():
        content = form.answer.data
        answer_model = AnswerModel(content=content, question_id=question_id, author=g.user)
        db.session.add(answer_model)
        db.session.commit()

        question = QuestionModel.query.get(question_id)

        return redirect(url_for('qa.question_detail', question_id=question_id))
    else:
        flash('表单验证失败')
        return redirect(url_for('qa.question_detail', question_id=question_id))


@bp.route('/search')
def question_search():
    # /search?query=xx
    query_word = request.args.get('query')
    questions = QuestionModel.query.filter(
        or_(QuestionModel.title.contains(query_word), QuestionModel.content.contains(query_word))).order_by(
        db.text('-create_time'))

    return render_template('index.html', questions=questions)
