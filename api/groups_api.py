from flask import Blueprint, request, jsonify, make_response
from data import db_session
from data.users import User
from data.groups import Group

blueprint = Blueprint('group_api', __name__, template_folder='templates')
db_session.global_init("db/usersData.db")
db_sess = db_session.create_session()


@blueprint.route('/api/groups', methods=['GET'])
def get_groups():
    groups = db_sess.query(Group).all()
    return jsonify({
        'groups': [item.to_dict(only=('name', 'description', 'user_id', 'members', 'link'))
                   for item in groups]
    })


@blueprint.route('/api/groups/<int:group_id>', methods=['GET'])
def get_group(group_id):
    group = db_sess.get(Group, group_id)
    if not group:
        return make_response(jsonify({'error': 'Not found: Group ID is invalid'}), 404)
    return jsonify(
        group.to_dict(only=('name', 'description', 'user_id', 'members', 'link'))
    )


@blueprint.route('/api/groups', methods=['POST'])
def create_group():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request (Request form: [name, description, user_id])'}), 400)
    elif not all(key in request.json for key in
                 ['name', 'description', 'user_id']):
        return make_response(
            jsonify({'error': 'Bad request: One or more required fields are missing [name, description, user_id]'}),
            400)
    elif len(request.json['name']) > 20:
        return make_response(jsonify(
            {"error": f"Bad request: Group name length is too long ({len(request.json['name'])} > 20 characters)"}),
                             400)
    elif len(request.json['description']) > 30:
        return make_response(jsonify(
            {
                "error": f"Bad request: Group description length is too long ({(len(request.json['description']))} > 30 characters)"}),
            400)
    user = db_sess.get(User, int(request.json['user_id']))
    if not user:
        return make_response(jsonify({'error': 'Not found: User ID is invalid'}), 404)
    elif not user.is_teacher:
        return make_response(jsonify({'error': "Bad request: User doesn't have access to create groups"}), 400)
    group = Group(
        name=request.json['name'],
        description=request.json['description'],
        user_id=request.json['user_id']
    )
    db_sess.add(group)
    user.groups.append(group)
    db_sess.commit()
    group.create_token()
    db_sess.commit()
    return jsonify({'success': f'Group (id: {group.id}) was created successfully'})


@blueprint.route('/api/groups/<int:group_id>', methods=['PUT'])
def edit_group(group_id):
    if not request.json:
        return make_response(jsonify({'error': 'Empty request (Request form: [name, description])'}), 400)
    group = db_sess.get(Group, group_id)
    if not group:
        return make_response(jsonify({'error': 'Not found: Group ID is invalid'}), 404)
    for key in request.json.keys():
        if key == 'name':
            if len(request.json['name']) > 20:
                return make_response(jsonify({
                                                 "error": f"Bad request: Group name length is too long ({len(request.json['name'])} > 20 characters)"}),
                                     400)
            group.name = request.json[key]
            db_sess.commit()
        elif key == 'description':
            if len(request.json['description']) > 30:
                return make_response(jsonify(
                    {
                        "error": f"Bad request: Group description length is too long ({(len(request.json['description']))} > 30 characters)"}
                ), 400)
            group.description = request.json[key]
            db_sess.commit()
    return jsonify({'success': f'Group (id: {group_id}) was edited successfully'})


@blueprint.route('/api/groups/<int:group_id>', methods=['DELETE'])
def delete_group(group_id):
    group = db_sess.get(Group, group_id)
    if not group:
        return make_response(jsonify({'error': 'Not found: Group ID is invalid'}), 404)
    user = db_sess.get(User, group.user_id)
    user.groups.remove(group)
    group_members = group.members.split(';')
    for id in group_members:
        if id == '':
            break
        user = db_sess.get(User, int(id))
        user.remove_group_participant(group_id)
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
    return jsonify({'success': f'Group (id: {group_id}) was deleted successfully'})
