import unittest

from flask import flash, make_response, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required

from app import create_app, login_manager
from app.firestore_service import delete_todo, get_todos, put_todo, update_todo
from app.forms import TodoForm

app = create_app()
login_manager.init_app(app)


@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html', error=error)


#   Main route for the app
@app.route('/')
def index():
    """index Shows a redirection link if there is no user's IP cookie

    Returns:
        cookie: cookie with the user's IP
    """
    user_ip = request.remote_addr

    response = make_response(redirect('/hello'))
    session['user_ip'] = user_ip

    return response


#   Route shown if there is a cookie with the user's IP available
@app.route('/hello', methods=['GET', 'POST'])
@login_required
def hello():
    """hello Defines the data for this path

    Returns:
        html: Template on Jira 2 with the route information
    """
    user_ip = session.get('user_ip')
    username = current_user.id
    todo_form = TodoForm()

    context = {
        'user_ip': user_ip,
        'todos': get_todos(user_id=username),
        'username': username,
        'todo_form': todo_form,
    }

    if todo_form.validate_on_submit():
        put_todo(user_id=username, description=todo_form.description.data)

        flash('Tarea creada con éxito!')

        return redirect(url_for('hello'))

    return render_template('hello.html', **context)


@app.route('/todos/delete/<todo_id>', methods=['GET'])
def delete(todo_id):
    user_id = current_user.id
    delete_todo(user_id=user_id, todo_id=todo_id)

    return redirect(url_for('hello'))


@app.route('/todos/update/<todo_id>/<int:done>', methods=['GET', 'POST'])
def update(todo_id, done):

    user_id = current_user.id

    update_todo(user_id=user_id, todo_id=todo_id, done=done)

    return redirect(url_for('hello'))
