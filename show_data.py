from app import English

for i in English.select():
    print(i.id, i.word, i.translate)
