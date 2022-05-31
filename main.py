import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)
DataBase = 'DataBase.db'


def cursor_fetchall(arg1, arg2=()):
    with sqlite3.connect(DataBase) as DB:
        cursor = DB.cursor()
        cursor.execute(arg1, arg2)
        data = cursor.fetchall()
    return data


def db_commit(arg1, arg2):
    with sqlite3.connect(DataBase) as DB:
        cursor = DB.cursor()
        cursor.execute(arg1, arg2)
        DB.commit()


@app.route('/', methods=['GET', 'POST'])
def music_lib():

    data_list = ['name', 'band', 'album', 'genre', 'year']
    search = request.values.get('search')
    insert = request.values.get('add_new')
    update = request.values.get('update')
    delete = request.values.get('delete')

    if insert:
        insert_new = []
        for i in data_list:
            insert_new.append(request.values.get(i))
        if insert_new[0] and insert_new[1] and insert_new[3] and insert_new[4]:
            db_commit('insert into song (name, band, album, genre, year) values (?,?,?,?,?);', insert_new)

    if search:
        if search == 'name':
            search_song = request.values.get(search)
            if len(search_song) > 0:
                data = cursor_fetchall('select * from song where name like ?;', ('%' + search_song + '%',))
                return render_template('index.html', context=data)

        if search == 'band':
            search_song = request.values.get(search)
            if len(search_song) > 0:
                data = cursor_fetchall('select * from song where band like ?;', ('%' + search_song + '%',))
                return render_template('index.html', context=data)

        if search == 'alltracks':
            data = cursor_fetchall('select * from song;', )
            return render_template('index.html', context=data)

    if update:
        update_list = []
        for i in data_list:
            update_list.append(request.values.get(i))
        update_list.append(update)
        print(update_list)
        if update_list[0] and update_list[1] and update_list[3] and update_list[4]:
            db_commit('update song set name=?, band=?, album=?, genre=?, year=? where id=?', (update_list))

    if delete:
        db_commit('DELETE FROM Song WHERE id = ?;', (delete,))

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
