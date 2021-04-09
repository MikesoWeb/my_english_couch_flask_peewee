from peewee import Model, CharField, PrimaryKeyField, SqliteDatabase

dt = SqliteDatabase('db_1.db')
# dt = SqliteDatabase('db_test.db')


class English(Model):
    id = PrimaryKeyField(primary_key=True)
    word = CharField(max_length=50, unique=True)
    translate = CharField(max_length=50, unique=True)

    class Meta:
        database = dt
        db_table = 'english'
        order_by = '-word'


English.create_table()
