from flask import Flask, make_response, redirect, render_template, request

app = Flask(__name__)

todos = ['Comprar cafe', 'Comprar guantes', 'Hacer el pull request']


#   Main route for the app
@app.route('/')
def index():
    """index Shows a redirection link if there is no user's IP cookie

    Returns:
        cookie: cookie with the user's IP
    """
    user_ip = request.remote_addr

    response = make_response(redirect('/hello'))
    response.set_cookie('user_ip', user_ip)

    return response


#   Route shown if there is a cookie with the user's IP available
@app.route('/hello')
def hello():
    """hello Defines the data for this path

    Returns:
        html: Template on Jira 2 with the route information
    """
    user_ip = request.cookies.get('user_ip')
    context = {
        'user_ip': user_ip,
        'todos': todos,
    }

    return render_template('hello.html', **context)
