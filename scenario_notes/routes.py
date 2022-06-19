from flask import Blueprint, redirect, request, render_template, session
from sql_provider import SQLProvider
from database import work_with_db, make_update
from config import db_config
import os

notes_bp = Blueprint('notes_app', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@notes_bp.route('/', methods=['GET', 'POST'])
def notes_list():
    sql_id = provider.get('id_by_login.sql', log=session['login'])
    id = work_with_db(db_config, sql_id)
    id = id[0]['id']
    if request.method == 'GET':
        notes = []
        sql_notes = provider.get('notes_list.sql', id_=id)
        notes = work_with_db(db_config, sql_notes)
        return render_template('notes.html', notes=notes, id_user=id)
    else:
        d = request.form.to_dict()
        if d['action'] == 'Редактировать':
            id_note = request.form.get('id_note')
            sql_note = provider.get('select_note.sql', id_=id, id_n=id_note)
            note = work_with_db(db_config, sql_note)
            note = note[0]['text']
            return render_template("edit_note.html", note_text=note, id_note=id_note)
        elif d['action'] == 'Удалить':
            id_note = request.form.get('id_note')
            sql = provider.get('delete_note.sql', id_=id, id_n=id_note)
            make_update(db_config, sql)
            num_of_del = int(id_note)
            sql = provider.get('num_note.sql', id_=id)
            num_of_notes = work_with_db(db_config, sql)
            num_of_notes = int(num_of_notes[0]['count(*)'])
            for i in range(num_of_del, num_of_notes+2):
                sql = provider.get('update_num_note.sql', id_=id, id_n=i)
                make_update(db_config, sql)
            return redirect('/notes')
        elif d['action'] == 'Добавить заметку':
            return render_template("add_note.html")


@notes_bp.route('/edit', methods=['GET', 'POST'])
def update_note():
    sql_id = provider.get('id_by_login.sql', log=session['login'])
    id = work_with_db(db_config, sql_id)
    id = id[0]['id']
    if request.method == 'GET':
        return render_template("edit_note.html")
    text = request.form.get('text_note')
    id_n = request.form.get('id_note')
    sql_update_text = provider.get('update_text.sql', text_note=text, id_=id, id_n=id_n)
    make_update(db_config, sql_update_text)
    return redirect('/notes')


@notes_bp.route('/add', methods=['GET', 'POST'])
def adding_note():
    sql_id = provider.get('id_by_login.sql', log=session['login'])
    id = work_with_db(db_config, sql_id)
    id = id[0]['id']
    if request.method == 'GET':
        return render_template("add_note.html")
    text = request.form.get('text_note')
    sql_num_notes = provider.get('num_note.sql', id_=id)
    num_notes = work_with_db(db_config, sql_num_notes)
    num_notes = num_notes[0]['count(*)'] + 1
    sql_add_note = provider.get('add_note.sql', id_=id, id_n=num_notes, text_note=text)
    print(sql_add_note)
    make_update(db_config, sql_add_note)
    return redirect('/notes')
