from datetime import datetime

from peewee import Model, CharField, PrimaryKeyField, SqliteDatabase, DateField

dt = SqliteDatabase('db_1.db')


class English(Model):
    id = PrimaryKeyField(primary_key=True)
    word = CharField(max_length=50, unique=True)
    translate = CharField(max_length=50, unique=True)

    class Meta:
        database = dt
        db_table = 'english'
        order_by = 'word'


English.create_table()
