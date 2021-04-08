from flask import Flask, render_template, request, redirect, url_for
from peewee import IntegrityError, fn
from models import English

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add_page')
def add():
    return render_template('add.html')


@app.route('/add', methods=['POST'])
def input_data():
    if request.method == 'POST':
        word = request.form['word']
        translate = request.form['translate']
        try:
            if English.create(word=word, translate=translate):
                return render_template('add.html', word=word, translate=translate)

        except IntegrityError:
            return render_template('add.html', word=word, integrity_error=IntegrityError)

    else:
        return redirect(url_for('index'))


@app.route('/update_page')
def update():
    return render_template('update.html')


@app.route('/update', methods=['post'])
def update_data():
    if request.method == 'POST':
        words = request.form['word']
        if English.select().where(English.word == words):
            word_upd = request.form['translate']
            q = English.update(translate=word_upd).where(English.word == words)
            q.execute()
            return render_template('update.html', words=words, word_upd=word_upd)
        else:
            return render_template('update.html', words=words)


@app.route('/delete_page')
def delete():
    return render_template('delete.html')


@app.route('/delete', methods=['post'])
def delete_data():
    if request.method == 'POST':
        word = request.form['word']
        del_word = English.select().where(English.word == word)
        if not del_word:
            return render_template('delete.html', word=word, del_word=del_word)
        else:
            English.delete_by_id(del_word)
            return render_template('delete.html', word=word, del_word=del_word)


@app.route('/show')
def all_notes_page():
    random_query = English.select().order_by(fn.Random())
    one_obj = random_query.get()
    return render_template('show.html', random_query=one_obj)


@app.route('/random_note')
def random_note():
    random_query = English.select().order_by(fn.Random())
    one_obj = random_query.get()
    return render_template('random_note.html', random_query=one_obj)


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
    app.run(debug=True, port=80)
