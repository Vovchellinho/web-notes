from flask import Flask, render_template, session
from sql_provider import SQLProvider
from scenario_auth.routes import auth_bp
from scenario_notes.routes import notes_bp
from scenario_reg.routes import reg_bp
from config import secret_key


app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key
provider = SQLProvider('sql')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(notes_bp, url_prefix='/notes')
app.register_blueprint(reg_bp, url_prefix='/registration')

@app.route('/')
def index():
    items = []
    if 'login' in session.keys():
        items.append(session['login'])
    return render_template('menu.html', items=items)

@app.route('/exit')
def clear_session():
    session.clear()
    return render_template('menu.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)