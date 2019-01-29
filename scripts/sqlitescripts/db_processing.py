import sqlite3

def sqlite3_database_create():
    # Соединяемся с базой данных, если БД нет - создаем с таким именем
 con = sqlite3.connect("C:/Users/Лада/PycharmProjects/nir_winter_2018/scripts/sqlitescripts/smart-contracts_database.db")  # или :memory: чтобы сохранить в RAM
     #Создаем объект курсора
 cursor = con.cursor()

    # Создание таблицы
 cursor.execute("""CREATE TABLE IF NOT EXISTS smart_contract_database
                        (sol_file_name text, code_hash_commit_before_audit text, code_hash_commit_after_audit text, diff text)
                       """)
 # Добавляем данные в таблицу
 #cursor.execute(' INSERT INTO smart_contract_database VALUES ("URL", "hash_before", "hash_after", "code_before", "code_after", "Difference")')
#это работает. Как сделать с переменными?
  # Записываем изменения
 con.commit()
 cursor.close()
 con.close() #Разрываем соединение с базой
sqlite3_database_create()
