from datetime import timedelta
import json
from flask import Flask, jsonify, request, session, Response, render_template

from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies
from flask_jwt_extended import get_jwt
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

from backend.todos.crud import get_user_todos, create_todo, delete_todo, get_current_todo, get_author_todo, update_todo
from backend.todos.utils import TodoCustomSerializer, InvalidAPIUsage
from backend.users.crud import add_user, get_user_hash_password, get_current_user
from backend.users.utils import generate_hash, authenticate

app = Flask(__name__)
app.secret_key = '6732c95ed3096a15d6fca0e52ebaf2d8f31b4145b6e6848f412027e688201421'
app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies", "json", "query_string"]
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)

jwt = JWTManager(app)


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(e):
    return jsonify(e.to_dict()), e.status_code


@app.route('/')
def index():
    context = {}
    if session.get('user_id'):
        user = get_current_user(session['user_id'])
        context['user_id'] = user[0]
        context['username'] = user[1]
    return render_template('index.html', context=context)


@app.route('/users/signup')
def signup_view():
    return render_template('auth/register.html')


@app.route('/users/login')
def login_view():
    return render_template('auth/login.html')


@app.route('/users/logout')
def logout_view():
    return render_template('auth/logout.html')


@app.route('/api/v1/users/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    hash_pass = generate_hash(password)
    new_user_id = add_user(username, hash_pass)
    user = get_current_user(new_user_id)
    user_data = {
        'id': user[0],
        'username': user[1]
    }
    response = json.dumps(user_data, ensure_ascii=False)
    return Response(response, content_type='application/json; charset=utf-8'), 201


@app.route('/api/v1/users/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    user = get_user_hash_password(username)
    if user is not None:
        auth = authenticate(password, user[2])
        if auth:
            additional_claims = {"user_id": user[0]}
            access_token = create_access_token(username, additional_claims=additional_claims)
            response = jsonify(access_token=access_token)
            set_access_cookies(response, access_token)
            session['user_id'] = user[0]
            return response
        else:
            raise InvalidAPIUsage("Password error", status_code=401)
    else:
        raise InvalidAPIUsage("Login error", status_code=401)


@app.route("/api/v1/users/logout", methods=["POST"])
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    if session.get('user_id'):
        session.pop('user_id')
    return response


@app.route("/api/v1/todos", methods=["GET", "POST"])
@jwt_required()
def get_todos():
    user_id = get_jwt().get('user_id')
    if request.method == 'GET':
        todos = get_user_todos(user_id)
        service = TodoCustomSerializer(todos)
        response = service.get_todos()
        response_data = json.dumps(response, ensure_ascii=False)
        return Response(response_data, content_type='application/json; charset=utf-8'), 200
    else:
        data = request.json
        title = data.get('title')
        description = data.get('description')
        if title is None:
            raise InvalidAPIUsage("Title is required fields", status_code=400)
        todo_id = create_todo(title, description, user_id)
        todo = get_current_todo(user_id, todo_id)
        service = TodoCustomSerializer(todo)
        response = service.get_todo()
        response_data = json.dumps(response, ensure_ascii=False)
        return Response(response_data, content_type='application/json; charset=utf-8'), 201


@app.route("/api/v1/todos/<todo_id>", methods=["GET"])
@jwt_required()
def get_todo(todo_id):
    user_id = get_jwt().get('user_id')
    todo = get_current_todo(user_id, todo_id)
    service = TodoCustomSerializer(todo)
    response = service.get_todo()
    response_data = json.dumps(response, ensure_ascii=False)
    return Response(response_data, content_type='application/json; charset=utf-8'), 200


@app.route("/api/v1/todos/<todo_id>", methods=["PUT"])
@jwt_required()
def change_todo(todo_id):
    user_id = get_jwt().get('user_id')
    author_todo = get_author_todo(todo_id, user_id)
    if author_todo is None:
        raise InvalidAPIUsage("You are not author this TODO", status_code=403)
    current_todo = get_current_todo(user_id, todo_id)
    created_at = current_todo[3]
    data = request.json
    title = data.get('title')
    description = data.get('description')
    if title is None:
        raise InvalidAPIUsage("Title is required fields", status_code=400)
    update_todo(todo_id, title, description, created_at)
    return Response(status=200)


@app.route("/api/v1/todos/<todo_id>", methods=["DELETE"])
@jwt_required()
def remove_todo(todo_id):
    user_id = get_jwt().get('user_id')
    author_todo = get_author_todo(todo_id, user_id)
    if author_todo is None:
        raise InvalidAPIUsage("You are not author this TODO", status_code=403)
    delete_todo(todo_id)
    return Response(status=204)
