import datetime
from functools import wraps
from flask import Blueprint, request
from flask_login import current_user
from data import db_session
from data.users import User
from data.groups import Group
from io import BytesIO
from PIL import Image

blueprint = Blueprint('user_service', __name__, template_folder='templates')
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


@blueprint.route('/user_service/avatar_loader', methods=['POST'])
@error_handler
def avatar_loader():
    path = f'static/profile_pics/'
    raw_image = BytesIO(request.get_data())
    image = Image.open(raw_image)
    image.save(path + f'{str(current_user.id)}.png')
    user = db_sess.get(User, current_user.id)
    user.profile_pics = '/' + path + f'{str(current_user.id)}.png'
    db_sess.commit()
    return path + f'{str(current_user.id)}.png'


@blueprint.route('/user_service/leave_group', methods=['POST'])
@error_handler
def leave_group():
    group_id = request.get_data(as_text=True)
    user = db_sess.get(User, current_user.id)
    group = db_sess.get(Group, group_id)
    user.remove_group_participant(group_id)
    group_works = group.group_works.copy()
    for work in group_works:
        work.remove_user_result(user.id)
    group.remove_member(current_user.id)
    db_sess.commit()
    return 'ok'
