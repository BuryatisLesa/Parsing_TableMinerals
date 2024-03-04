import sqlite3

connection = sqlite3.connect('db_minerals.db')
sql = "CREATE TABLE MINERALS (Название TEXT, Формула TEXT, Сингония TEXT, Агрегаты TEXT, Цвет TEXT, Цвет_черты TEXT, Блеск TEXT, Спайность TEXT, Твердость TEXT, Уд_вес TEXT, Диагностика TEXT, Ассоциация TEXT)"
del_table = "DELETE FROM MINERALS"
cursor = connection.cursor()
cursor.execute(sql)
connection.close()
