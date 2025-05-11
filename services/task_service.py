import datetime
from functools import wraps
from flask import Blueprint, request, jsonify
from flask_login import current_user
from data import db_session
from data.users import User
from data.tasks import Task

blueprint = Blueprint('task_service', __name__, template_folder='templates')
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


@blueprint.route('/task_service/get_tasks', methods=['POST'])
@error_handler
def get_tasks():
    options = request.get_json(force=True)['options']
    if options[1] == 'Все сложности' and options[2] == 'Все типы':
        data = db_sess.query(Task).filter(Task.number == int(options[0])).all()
    elif options[1] == 'Все сложности':
        data = db_sess.query(Task).filter(Task.number == int(options[0]), Task.type == options[2]).all()
    elif options[2] == 'Все типы':
        data = db_sess.query(Task).filter(Task.number == int(options[0]), Task.difficulty == options[1]).all()
    else:
        data = db_sess.query(Task).filter(Task.number == int(options[0]), Task.difficulty == options[1],
                                          Task.type == options[2]).all()
    result = []
    for part in data:
        part_dict = part.get_dict()
        part_dict['id'] = part.id
        result.append(part_dict)
    if current_user.is_authenticated:
        solved = current_user.solved_tasks_ids
    else:
        solved = ''
    reply = {'tasks': result, 'solved': solved}
    return jsonify(reply)


@blueprint.route('/task_service/get_task_by_id', methods=['POST'])
@error_handler
def get_task_by_id():
    response_id = int(request.get_data(as_text=True))
    task = db_sess.get(Task, response_id)
    return jsonify(task.get_dict())


@blueprint.route('/task_service/get_answers', methods=['POST'])
@error_handler
def get_answers():
    response = request.get_json(force=True)
    task = db_sess.get(Task, int(response['id']))
    if task.answer.lower() == response['answer'].lower():
        return 'ok'
    return 'fail'


@blueprint.route('/task_service/get_solution', methods=['POST'])
@error_handler
def get_solution():
    response = request.get_data(as_text=True)
    task = db_sess.get(Task, int(response))
    return task.solution


@blueprint.route('/task_service/make_solved', methods=['POST'])
@error_handler
def make_solved():
    if current_user.is_authenticated:
        response = request.get_data(as_text=True)
        user = db_sess.get(User, current_user.id)
        user.add_solved_task(response)
        db_sess.commit()
        return 'ok'
    return 'fail'
