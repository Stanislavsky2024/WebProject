import datetime
from functools import wraps
from flask_login import current_user
from flask import Blueprint, request, jsonify
from data import db_session
from data.random_variants import Random_variant
from data.variants import Variant
from data.answers_variants import Answers_variant
from data.group_works import Group_work
from data.answers_works import Answers_work

blueprint = Blueprint('variant_service', __name__, template_folder='templates')
db_session.global_init("db/usersData.db")
db_sess = db_session.create_session()


def error_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as error:
            error_time = datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
            error_service = f'Сервис, вызвавший ошибку: {blueprint.name} ({func.__name__})'
            error_message = f'Тип ошибки: {type(error).__name__}, сообщение: {str(error)}'
            with open('logs.txt', 'w', encoding='utf8') as log:
                log.writelines(
                    ['-' * 25 + '\n', error_time + '\n', error_service + '\n', error_message + '\n', '-' * 25])
            print('-' * 25, error_time, error_service, error_message, '-' * 25, sep='\n')

    return wrapper


@blueprint.route('/variant_service/get_tasks', methods=['POST'])
@error_handler
def get_tasks():
    response = request.get_data(as_text=True)
    data = response.split('-')[0]
    data_type = response.split('-')[1]
    tasks = []
    if data_type == 'variant':
        if data == 'random':
            variant = db_sess.query(Random_variant).filter(Random_variant.user_id == current_user.id).first()
        else:
            variant = db_sess.get(Variant, int(data))
        for task in variant.tasks:
            task_dict = task.get_dict()
            task_dict['id'] = task.id
            tasks.append(task_dict)
    else:
        work = db_sess.get(Group_work, int(data))
        for task in work.tasks:
            task_dict = task.get_dict()
            task_dict['id'] = task.id
            tasks.append(task_dict)
    return jsonify(tasks)


@blueprint.route('/variant_service/get_answers', methods=['POST'])
@error_handler
def get_answers():
    response = request.get_json(force=True)
    data = response['var'].split('-')[0]
    data_type = response['var'].split('-')[1]
    if data_type == 'variant':
        answers_variant = Answers_variant(
            user_id=current_user.id
        )
        if data == 'random':
            variant = db_sess.query(Random_variant).filter(Random_variant.user_id == current_user.id).first()
        else:
            variant = db_sess.get(Variant, int(data))
        for i in range(len(variant.tasks)):
            if str(i + 1) in response['answers'].keys():
                user_answer = response['answers'][str(i + 1)]
            else:
                user_answer = '-'
            answers_variant.add_answers(user_answer, variant.tasks[i].answer)
        answers_variant_delete = db_sess.query(Answers_variant).filter(
            Answers_variant.user_id == current_user.id).first()
        if answers_variant_delete:
            db_sess.delete(answers_variant_delete)
        db_sess.add(answers_variant)
        db_sess.commit()
    else:
        work = db_sess.get(Group_work, int(data))
        answers_work = Answers_work(
            user_id=current_user.id,
            max_points=len(work.tasks)
        )
        for i in range(len(work.tasks)):
            if str(i + 1) in response['answers'].keys():
                user_answer = response['answers'][str(i + 1)]
            else:
                user_answer = '-'
            answers_work.add_answers(user_answer, work.tasks[i].answer)
        answers_work_delete = db_sess.query(Answers_work).filter(Answers_work.user_id == current_user.id).first()
        if answers_work_delete:
            db_sess.delete(answers_work_delete)
        db_sess.add(answers_work)
        result = answers_work.get_result()
        work.add_result(str(current_user.id), str(result['correct_answers']))
        db_sess.commit()
    return 'ok'
