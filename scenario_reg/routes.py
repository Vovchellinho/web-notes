from flask import Blueprint, redirect, request, render_template, session
from sql_provider import SQLProvider
from database import work_with_db, make_update
from config import db_config
import os

reg_bp = Blueprint('reg_app', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__),'sql'))

@reg_bp.route('/', methods=['GET', 'POST'])
def reg_page():
    if request.method == 'GET':
        return render_template('registration.html')
    login = request.form.get('login', '')
    password = request.form.get('password', '')
    sql = provider.get('check_login.sql', log=login)
    login_user = work_with_db(db_config, sql)
    if login_user:
        return render_template('invalid2.html')
    sql = provider.get('insert_user.sql', log=login, pas=password)
    make_update(db_config, sql)
    session['login'] = login
    return redirect('/')