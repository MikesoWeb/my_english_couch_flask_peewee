from flask import Flask, render_template, request, redirect, url_for, flash
from peewee import IntegrityError, fn
from models import English
from config_data import DEBUG, SECRET_KEY

app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/')
def index():
    count_words = len(English.select())
    return render_template('index.html', count_words=count_words)


# ADD
@app.route('/add_page', methods=['get'])
def add():
    count_words = len(English.select())
    return render_template('add.html', count_words=count_words)


@app.route('/add', methods=['POST', 'GET'])
def input_data():
    if request.method == 'POST':
        word = request.form['word']
        translate = request.form['translate']
        try:
            if English.create(word=word, translate=translate):
                flash(f'Слово <b>{word}</b> и его перевод <b>{translate}</b> добавлены', category='success')

        except IntegrityError:
            flash(f'Слово <b>{word}</b> в базе существует!', category='attention')

        return render_template('add.html')

    else:
        return redirect(url_for('add_page'))


# UPDATE
@app.route('/update_page')
def update():
    count_words = len(English.select())
    return render_template('update.html', count_words=count_words)


@app.route('/update', methods=['post', 'get'])
def update_data():
    if request.method == 'POST':
        words = request.form['word']
        if English.select().where(English.word == words):
            word_upd = request.form['translate']
            q = English.update(translate=word_upd).where(English.word == words)
            q.execute()
            flash(f'У слова <b>{words}</b> был обновлен перевод на <b>{word_upd}</b>!', category='attention')
        else:
            flash(f'Слово <b>{words}</b> не найдено в базе!', category='error')

        return render_template('update.html')

    # else:
    #     return redirect(url_for('update_page'))


@app.route('/delete_page')
def delete():
    count_words = len(English.select())
    return render_template('delete.html', count_words=count_words)


@app.route('/delete', methods=['post', 'get'])
def delete_data():
    if request.method == 'POST':
        word = request.form['word']
        del_word = English.select().where(English.word == word)
        if not del_word:
            flash(f'Слово <b>{word}</b> в базе не найдено!', category='error')
        else:
            English.delete_by_id(del_word)
            flash(f'Слово <b>{word}</b> удалено!', category='success')

    return render_template('delete.html')


@app.route('/show')
def all_notes_page():
    count_words = len(English.select())
    return render_template('show.html', count_words=count_words)


@app.route('/random_note')
def random_note():
    count_words = len(English.select())
    random_query = English.select().order_by(fn.Random())
    one_obj = random_query.get()
    return render_template('random_note.html', random_query=one_obj, count_words=count_words)


@app.route('/all_notes', methods=['get'])
def all_notes():
    query_all = English.select()
    count_words = len(English.select())
    return render_template('all_notes.html', query_all=query_all, count_words=count_words)


@app.route('/count_notes', methods=['post'])
def count_notes():
    if request.method == 'POST':
        count = request.form['count']
        query_count = English.select().limit(count)
        return render_template('count_notes.html', query_count=query_count)


if __name__ == '__main__':
    app.run(debug=DEBUG, port=80)
    English.create_table()
