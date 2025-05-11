from flask import Blueprint, request, jsonify, make_response
from data import db_session
from data.users import User
from data.groups import Group

blueprint = Blueprint('user_api', __name__, template_folder='templates')
db_session.global_init("db/usersData.db")
db_sess = db_session.create_session()


@blueprint.route('/api/users', methods=['GET'])
def get_users():
    users = db_sess.query(User).all()
    return jsonify({
        'users': [item.to_dict(only=('name', 'surname', 'email', 'created_date', 'is_teacher'))
                  for item in users]
    })


@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = db_sess.get(User, user_id)
    if not user:
        return make_response(jsonify({'error': 'Not found: User ID is invalid'}), 404)
    return jsonify(
        user.to_dict(only=('name', 'surname', 'email', 'created_date', 'is_teacher'))
    )


@blueprint.route('/api/users', methods=['POST'])
def create_user():
    if not request.json:
        return make_response(
            jsonify({'error': 'Empty request (Request form: [name, surname, email, password, is_teacher])'}), 400)
    elif not all(key in request.json for key in
                 ['name', 'surname', 'email', 'password', 'is_teacher']):
        return make_response(jsonify({
                                         'error': 'Bad request: One or more required fields are missing '
                                                  '[name, surname, email, password, is_teacher]'}),
                             400)
    elif len(request.json['name']) > 14:
        return make_response(
            jsonify({'error': f'Bad request: Name length is too long ({len(request.json["name"])} > 14 characters)'}),
            400)
    elif len(request.json['surname']) > 14:
        return make_response(jsonify(
            {'error': f'Bad request: Surname length is too long ({len(request.json["surname"])} > 14 characters)'}),
                             400)
    elif type(request.json['is_teacher']) != bool:
        return make_response(jsonify({'error': f'Bad request: type of field "is_teacher" must be Bool'}), 400)
    user = User(
        name=request.json['name'],
        surname=request.json['surname'],
        email=request.json['email'],
        is_teacher=request.json['is_teacher']
    )
    user.set_password(request.json['password'])
    db_sess.add(user)
    db_sess.commit()
    return jsonify({'success': f'User (id: {user.id}) was created successfully'})


@blueprint.route('/api/users/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    if not request.json:
        return make_response(jsonify({'error': 'Empty request (Request form: [name, surname, email, password])'}), 400)
    user = db_sess.get(User, user_id)
    if not user:
        return make_response(jsonify({'error': 'Not found: User ID is invalid'}), 404)
    for key in request.json.keys():
        if key == 'name':
            if len(request.json['name']) > 14:
                return make_response(jsonify(
                    {'error': f'Bad request: Name length is too long ({len(request.json["name"])} > 14 characters)'}),
                                     400)
            user.name = request.json['name']
            db_sess.commit()
        elif key == 'surname':
            if len(request.json['surname']) > 14:
                return make_response(jsonify({
                                                 'error': f'Bad request: Name length is too long '
                                                 f'({len(request.json["surname"])} > 14 characters)'}),
                                     400)
            user.surname = request.json['surname']
            db_sess.commit()
        elif key == 'email':
            user.email = request.json['email']
            db_sess.commit()
        elif key == 'password':
            user.set_password(request.json['password'])
            db_sess.commit()
    return jsonify({'success': f'User (id: {user_id}) was edited successfully'})


@blueprint.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = db_sess.get(User, user_id)
    if not user:
        return make_response(jsonify({'error': 'Not found: User ID is invalid'}), 404)
    groups_participant = user.get_group_participant()
    groups = db_sess.query(Group).all()
    for group in groups:
        if group.user_id == user.id:
            group_members = group.members.split(';')
            for id in group_members:
                if id == '':
                    break
                member = db_sess.get(User, id)
                member.remove_group_participant(group.id)
                db_sess.commit()
            group_works = group.group_works.copy()
            for work in group_works:
                work_tasks = work.tasks.copy()
                for task in work_tasks:
                    work.tasks.remove(task)
                    db_sess.delete(task)
                    db_sess.commit()
                group.group_works.remove(work)
                db_sess.delete(work)
                db_sess.commit()
            announcement = group.announcement
            if announcement:
                db_sess.delete(announcement)
                db_sess.commit()
            db_sess.delete(group)
            db_sess.commit()
        elif groups_participant:
            if str(group.id) in groups_participant:
                group.remove_member(user_id)
                db_sess.commit()
                group_works = group.group_works.copy()
                for work in group_works:
                    work.remove_user_result(user_id)
                    db_sess.commit()

    db_sess.delete(user)
    db_sess.commit()
    return jsonify({'success': f'User (id: {user_id}) was deleted successfully'})
