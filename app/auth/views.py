from app.firestore_service import get_user
from app.forms import LoginForm
from app.models import UserData, UserModel

from flask import flash, redirect, render_template, url_for
from flask_login import current_user,login_user, login_required, logout_user

from . import auth


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    else:
        login_form = LoginForm()
        context = {
            'login_form': login_form
        }

        if login_form.validate_on_submit():
            username = login_form.username.data
            password = login_form.password.data

            user_doc = get_user(username)

            if user_doc.to_dict() is not None:
                password_from_db = user_doc.to_dict()['password']

                if password == password_from_db:
                    user_data = UserData(username, password)
                    user = UserModel(user_data)
                    # log to the user 
                    login_user(user)

                    flash('Bienvenido de nuevo')

                    redirect(url_for('hello'))
                else:
                    flash('La contraseña o el usuario no coinciden')

            else:
                flash('El usuario no existe')

            return redirect(url_for('index'))

    return render_template('login.html', **context)


@auth.route('logout')
@login_required
def logout():
    logout_user()
    flash('Regresa pronto!')
    
    return redirect(url_for('auth.login'))