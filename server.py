import random
import pymorphy3
import datetime
from flask import Flask, render_template, redirect, abort, make_response, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from data import db_session
from data.users import User
from data.groups import Group
from data.news import News
from data.random_variants import Random_variant
from data.tasks import Task
from data.variants import Variant
from data.answers_variants import Answers_variant
from data.answers_works import Answers_work
from data.group_works import Group_work
from forms.user import RegisterForm, LoginForm
from forms.group import editGroupForm, createGroupForm

import services.group_service
import services.task_service
import services.user_service
import services.variant_service
import api.groups_api
import api.users_api
import api.news_api

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
db_session.global_init("db/usersData.db")
db_sess = db_session.create_session()

login_manager = LoginManager()
login_manager.init_app(app)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def main():
    params = {
        'news': db_sess.get(News, 1),
        'title': 'Главная страница',
        'active': '1'
    }
    return render_template('MainPage.html', **params)


@app.route('/catalog')
def catalog():
    data = db_sess.query(Task).filter(Task.number == 1)
    if current_user.is_authenticated:
        solved = current_user.solved_tasks_ids.split(';')
    else:
        solved = ''
    params = {
        'tasks': data,
        'solved': solved,
        'title': 'Каталог заданий',
        'active': '2'
    }
    return render_template('CatalogOfTasks.html', **params)


@app.route('/variants/choose')
@login_required
def variants_choose():
    params = {
        'vars_list': db_sess.query(Variant).all(),
        'title': 'Выбор варианта',
        'active': '3'
    }
    return render_template('VariantsChoose.html', **params)


@app.route('/variants/generate')
@login_required
def variants_generate():
    params = {
        'title': 'Генерация варианта',
        'active': '3'
    }
    return render_template('VariantsGenerate.html', **params)


@app.route('/variants/solving/<var>')
@login_required
def variants_solving(var):
    if var == 'random':
        variant = Random_variant(
            user_id=current_user.id
        )
        for i in range(1, 13):
            tasks = db_sess.query(Task).filter(Task.number == i,
                                               Task.difficulty == random.choice(
                                                   ['Простой', 'Средний', 'Сложный'])).all()
            variant.tasks.append(random.choice(tasks))
        first = variant.tasks[0]
        name = 'Случайный вариант'
        length = variant.tasks[-1].number
        variant_delete = db_sess.query(Random_variant).filter(Random_variant.user_id == current_user.id).first()
        if variant_delete:
            db_sess.delete(variant_delete)
        db_sess.add(variant)
        db_sess.commit()
    else:
        try:
            variant = db_sess.get(Variant, int(var))
            first = variant.tasks[0]
            name = variant.name
            length = variant.tasks[-1].number
        except TypeError:
            abort(404)
    return render_template('VariantsSolving.html', first=first, length=length,
                           name=name, var=var + '-variant', title='Решение варианта', active='3')


@app.route('/variants/results')
@login_required
def variants_results():
    answers_variant = db_sess.query(Answers_variant).filter(Answers_variant.user_id == current_user.id).first()
    results = answers_variant.get_result()
    if results['total_points'] == 100 and current_user.is_authenticated:
        db_sess.get(User, current_user.id).add_solved_variant()
        db_sess.commit()
    params = {
        'points': results['points'],
        'totalPoints': results['total_points'],
        'corrAns': results['correct_answers'],
        'totalAns': results['total_answers'],
        'results': answers_variant.get_answers(),
        'active': '3',
        'title': 'Результаты решения варианта',
        'mode': 'variant'
    }
    return render_template('VariantsResults.html', **params)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('Register.html', title='Регистрация',
                                   form=form, active='0',
                                   message="Пароли не совпадают")
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('Register.html', title='Регистрация',
                                   form=form, active='0',
                                   message="Пользователь с указанной почтой уже зарегистрирован на данном сайте")
        if len(form.name.data) > 14 or len(form.surname.data) > 14:
            return render_template('Register.html', title='Регистрация',
                                   form=form, active='0',
                                   message="Длина имени или фамилии превышает допустимые 12 символов")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
            is_teacher=form.is_teacher.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('Register.html', title='Регистрация', form=form, active='0')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('Login.html',
                               message="Неправильная почта или пароль",
                               form=form)
    return render_template('Login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/profile', methods=['GET'])
@login_required
def profile():
    groups = current_user.get_group_participant()
    if groups:
        groups_amount = len(groups)
    else:
        groups_amount = 0
    groups = current_user.groups
    groups_amount += len(groups)
    variants = current_user.solved_variants
    tasks_amount = current_user.solved_tasks_ids.split(';')
    if tasks_amount == ['']:
        tasks_amount = 0
    else:
        tasks_amount = len(tasks_amount)
    morph = pymorphy3.MorphAnalyzer()
    time_word = morph.parse('день')[0]
    tasks_word = morph.parse('задание')[0]
    groups_word = morph.parse('группа')[0].inflect({'loct'})
    variants_word = morph.parse('вариант')[0]
    registered_date = datetime.datetime.strptime(current_user.created_date.split()[0], '%Y-%m-%d').date()
    current_date = datetime.datetime.now().date()
    date = (current_date - registered_date).days
    words = {
        'tasks_amount': tasks_amount,
        'groups_amount': groups_amount,
        'date_amount': date,
        'variants_amount': variants,
        'groups': groups_word.make_agree_with_number(groups_amount).word,
        'tasks': tasks_word.make_agree_with_number(tasks_amount).word,
        'variants': variants_word.make_agree_with_number(variants).word,
        'date': time_word.make_agree_with_number(date).word
    }
    return render_template('Profile.html', title='Профиль', active='4', **words)


@app.route('/groups', methods=['GET', 'POST'])
@login_required
def groups():
    formCreate = createGroupForm()
    formEdit = editGroupForm()
    groups = current_user.get_group_participant()
    if groups:
        groups_participant = [db_sess.get(Group, id) for id in groups]
    else:
        groups_participant = [None]
    params = {
        'groups': db_sess.query(Group).filter(current_user.id == Group.user_id),
        'groups_participant': groups_participant
    }
    return render_template('Groups.html', title='Группы', active='5', formCreate=formCreate,
                           formEdit=formEdit, **params)


@app.route('/groups/<int:group_id>')
@login_required
def group(group_id):
    group = db_sess.get(Group, group_id)
    if not group:
        return abort(404)
    group_works = group.group_works
    results = []
    if group_works:
        for work in group_works:
            if work.get_user_result(current_user.id):
                results.append(work.get_user_result(current_user.id) + '/' + str(work.max_result))
            else:
                results.append('-')
    else:
        group_works = []
    if group.check_member(current_user.id):
        params = {
            'creator': group.get_creator(),
            'members': group.get_members(),
            'link': group.link,
            'announcement': group.announcement,
            'works': group_works,
            'results': results,
            'active': '5',
            'title': f'Группа "{group.name}"',
            'editor': 'true',
            'group_id': group_id
        }
        return render_template('GroupPage.html', **params)
    else:
        return abort(403)


@app.route('/groups/<int:group_id>/editor')
@login_required
def group_editor(group_id):
    group = db_sess.get(Group, group_id)
    last_number = db_sess.query(Task).all()[-1].number
    if not group:
        return abort(404)
    if group.get_creator()['id'] != current_user.id:
        return abort(403)
    params = {
        'name': group.name,
        'last_number': last_number,
        'title': 'Редактор группы',
        'active': 'edit',
        'editor': 'true',
        'creator': group.get_creator()
    }
    return render_template('GroupEditor.html', **params)


@app.route('/groups/<int:group_id>/<int:work_id>/solving')
@login_required
def group_solving(group_id, work_id):
    work = db_sess.get(Group_work, work_id)
    first = work.tasks[0]
    length = len(work.tasks)
    name = work.name
    var = str(work_id) + '-work'
    return render_template('VariantsSolving.html', first=first, length=length,
                           name=name, var=var, title='Решение групповой работы', active='5')


@app.route('/groups/results')
@login_required
def group_results():
    answers_work = db_sess.query(Answers_work).filter(Answers_work.user_id == current_user.id).first()
    results = answers_work.get_result()
    params = {
        'points': answers_work.max_points,
        'totalPoints': results['total_points'],
        'corrAns': results['correct_answers'],
        'totalAns': results['total_answers'],
        'results': answers_work.get_answers(),
        'active': '5',
        'title': 'Результаты решения работы',
        'mode': 'work'
    }
    return render_template('VariantsResults.html', **params)


@app.route('/groups/join/<token>')
@login_required
def join_group(token):
    group_id = Group.verify_token(token)
    group = db_sess.get(Group, group_id)
    user = db_sess.get(User, current_user.id)
    if not group:
        abort(404)
    group.add_member(current_user.id)
    user.add_group_participant(group_id)
    db_sess.commit()
    return redirect(f'/groups/{group.id}')


if __name__ == '__main__':
    app.register_blueprint(services.user_service.blueprint)
    app.register_blueprint(services.group_service.blueprint)
    app.register_blueprint(services.variant_service.blueprint)
    app.register_blueprint(services.task_service.blueprint)
    app.register_blueprint(api.groups_api.blueprint)
    app.register_blueprint(api.users_api.blueprint)
    app.register_blueprint(api.news_api.blueprint)
    app.run(host='127.0.0.1')
