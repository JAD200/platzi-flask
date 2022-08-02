from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

from flask import Flask, flash,make_response, redirect, render_template, request, session, url_for

app = Flask(__name__, template_folder='./templates', static_folder='./static')
bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = '69E9FBBE-27B3-4E68-8BC3-2D9EE573FFEF'

todos = ['Comprar cafe', 'Comprar guantes', 'Hacer el pull request']


class LoginForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Enviar')


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
def hello():
    """hello Defines the data for this path

    Returns:
        html: Template on Jira 2 with the route information
    """
    user_ip = session.get('user_ip')
    login_form = LoginForm()
    username = session.get('username')

    context = {
        'user_ip': user_ip,
        'todos': todos,
        'login_form': login_form,
        'username': username,
    }
    if login_form.validate_on_submit():
        username = login_form.username.data
        session['username'] = username
        
        flash('Nombre de usuario registrado con éxito!')
        
        return redirect(url_for('index'))

    return render_template('hello.html', **context)
