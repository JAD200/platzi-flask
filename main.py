import unittest

from flask import make_response, redirect, render_template, request, session

from app import create_app
from app.firestore_service import get_users, get_todos

app = create_app()

# todos = ['Comprar cafe', 'Comprar guantes', 'Hacer el pull request']


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
@app.route('/hello', methods=['GET'])
def hello():
    """hello Defines the data for this path

    Returns:
        html: Template on Jira 2 with the route information
    """
    user_ip = session.get('user_ip')
    username = session.get('username')

    context = {
        'user_ip': user_ip,
        'todos': get_todos(user_id=username),
        'username': username,
    }
    
    users = get_users()
    
    for user in users:
        print(user.id)
        print(user.to_dict()['password'])

    return render_template('hello.html', **context)
