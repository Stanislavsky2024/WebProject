from flask import Blueprint, request, jsonify, make_response
from data import db_session
from data.news import News
from PIL import Image

blueprint = Blueprint('news_api', __name__, template_folder='templates')
db_session.global_init("db/usersData.db")
db_sess = db_session.create_session()


@blueprint.route('/api/news', methods=['GET'])
def get_news():
    news = db_sess.query(News).first()
    return jsonify(
        news.to_dict(only=('name', 'content', 'image'))
    )


@blueprint.route('/api/news', methods=['POST'])
def create_news():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request (Request form: [name, content, image])'}), 400)
    elif not all(key in request.json for key in
                 ['name', 'content', 'image']):
        return make_response(
            jsonify({'error': 'Bad request: One or more required fields are missing [name, content, image]'}), 400)
    elif len(request.json['name']) > 35:
        return make_response(jsonify(
            {"error": f"Bad request: News name length is too long ({len(request.json['name'])} > 35 characters)"}), 400)
    elif len(request.json['content']) > 250:
        return make_response(jsonify(
            {"error": f"Bad request: News content length is too long ({len(request.json['name'])} > 250 characters)"}),
            400)
    try:
        with Image.open('.' + request.json['image']) as f:
            f.verify()
    except FileNotFoundError:
        return make_response(jsonify({'error': 'Bad request: filepath is invalid'}))
    except (IOError, SyntaxError):
        return make_response(jsonify({'error': "Bad request: file isn't an image"}))
    news = News(
        name=request.json['name'],
        content=request.json['content'],
        image=request.json['image']
    )
    news_delete = db_sess.query(News).first()
    db_sess.delete(news_delete)
    db_sess.add(news)
    db_sess.commit()
    return jsonify({'success': f'News was created successfully'})


@blueprint.route('/api/news', methods=['PUT'])
def edit_news():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request (Request form: [name, content, image])'}), 400)
    news = db_sess.query(News).first()
    for key in request.json.keys():
        if key == 'name':
            if len(request.json['name']) > 35:
                return make_response(jsonify(
                    {
                        "error": f"Bad request: News name length is too long "
                        f"({len(request.json['name'])} > 35 characters)"}),
                    400)
            news.name = request.json['name']
            db_sess.commit()
        elif key == 'content':
            if len(request.json['content']) > 250:
                return make_response(jsonify(
                    {
                        "error": f"Bad request: News content length is too long "
                        f"({len(request.json['name'])} > 250 characters)"}),
                    400)
            news.content = request.json['content']
            db_sess.commit()
        elif key == 'image':
            try:
                with Image.open('.' + request.json['image']) as f:
                    f.verify()
            except FileNotFoundError:
                return make_response(jsonify({'error': 'Bad request: filepath is invalid'}))
            except (IOError, SyntaxError):
                return make_response(jsonify({'error': "Bad request: file isn't an image"}))
            news.image = request.json['image']
            db_sess.commit()
    return jsonify({'success': f'News was edited successfully'})
