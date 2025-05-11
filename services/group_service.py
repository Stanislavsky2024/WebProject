import datetime
from functools import wraps
from flask import Blueprint, request, abort
from flask_login import current_user
from data import db_session
from data.users import User
from data.groups import Group
from data.group_works import Group_work
from data.announcements import Announcement
from data.work_tasks import Work_task

blueprint = Blueprint('group_service', __name__, template_folder='templates')
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


@blueprint.route('/group_service/check_group_name_validation', methods=['POST'])
@error_handler
def check_group_name_validation():
    data = request.get_data(as_text=True)
    if db_sess.query(Group).filter(Group.name == data, Group.user_id == current_user.id).first():
        return 'failed'
    return 'success'


@blueprint.route('/group_service/group_creator', methods=['POST'])
@error_handler
def group_creator():
    data = request.get_json(force=True)
    group = Group(
        name=data['name'],
        description=data['description'],
        user_id=current_user.id,
    )
    user = db_sess.get(User, current_user.id)
    db_sess.add(group)
    user.groups.append(group)
    db_sess.commit()
    group.create_token()
    db_sess.commit()
    return 'ok'


@blueprint.route('/group_service/group_editor', methods=['POST'])
@error_handler
def group_editor():
    data = request.get_json(force=True)
    group = db_sess.query(Group).filter(current_user.id == Group.user_id, Group.id == data['group_id']).first()
    group.name = data['name']
    group.description = data['description']
    db_sess.commit()
    return 'ok'


@blueprint.route('/group_service/group_remover', methods=['POST'])
@error_handler
def group_remover():
    group_id = request.get_data(as_text=True)
    group = db_sess.get(Group, group_id)
    if group:
        user = db_sess.get(User, current_user.id)
        user.groups.remove(group)
        for id in group.members:
            user = db_sess.get(User, id)
            user.remove_group_participant(group_id)
        for work in group.group_works:
            group.group_works.remove(work)
            db_sess.delete(work)
        announcement = group.announcement
        if announcement:
            db_sess.delete(announcement)
        db_sess.delete(group)
        db_sess.commit()
    else:
        abort(404)
    return 'ok'


@blueprint.route('/group_service/add_group_work', methods=['POST'])
@error_handler
def add_group_work():
    response = request.get_json(True)
    group = db_sess.get(Group, int(response['group_id']))
    group_work = Group_work(
        name=response['name']
    )
    for raw_task in response['tasks']:
        if len(raw_task.keys()) > 2:
            task = Work_task(
                text1=raw_task['text1'],
                image=raw_task['image'],
                text2=raw_task['text2'],
                answer=raw_task['answer']
            )
        else:
            task = Work_task(
                text1=raw_task['text1'],
                image='',
                text2='',
                answer=raw_task['answer']
            )
        group_work.tasks.append(task)
    group_work.max_result = len(group_work.tasks)
    group.group_works.append(group_work)
    db_sess.commit()
    return 'ok'


@blueprint.route('/group_service/remove_group_work', methods=['POST'])
@error_handler
def remove_group_work():
    response = request.get_json(True)
    group = db_sess.get(Group, int(response['group_id']))
    work = db_sess.get(Group_work, int(response['work_id']))
    for task in work.tasks:
        db_sess.delete(task)
    group.group_works.remove(work)
    db_sess.delete(work)
    db_sess.commit()
    return 'ok'


@blueprint.route('/group_service/add_announcement', methods=['POST'])
@error_handler
def add_announcement():
    response = request.get_json(True)
    group = db_sess.get(Group, int(response['group_id']))
    announcement = Announcement(
        title=response['title'],
        text=response['text']
    )
    if group.announcement:
        db_sess.delete(group.announcement)
    group.announcement = announcement
    db_sess.commit()
    return 'ok'
