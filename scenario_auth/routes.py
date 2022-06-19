from flask import Blueprint, redirect, request, render_template, session
from sql_provider import SQLProvider
from database import work_with_db
from config import db_config
import os

auth_bp = Blueprint('auth_app', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__),'sql'))

@auth_bp.route('/', methods=['GET', 'POST'])
def login_page():
    if request.method == 'GET':
        return render_template('login_page.html')
    login = request.form.get('login', '')
    password = request.form.get('password', '')
    sql = provider.get('auth.sql', log = login, pas = password)
    login_user = work_with_db(db_config, sql)
    if not login_user:
        return render_template('invalid.html')
    session['login'] = login
    return redirect('/')