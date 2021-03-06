import subprocess
import os
import re
import sqlite3
from scripts.sqlitescripts.db_processing import *
con = sqlite3.connect("C:/Users/Лада/PycharmProjects/nir_winter_2018/scripts/sqlitescripts/smart-contracts_database_new.db")
#c = con.cursor()

from main_script import *

def create_dir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def delete_dir(dir_path="tmp_repo"):
    os.system("rmdir /Q /S " + dir_path)


# Клонируем репозиторий
def clone_repo(repo_url, folder_name="tmp_repo"):
    # Создаем папку (для каждого нового репо заново клонируем туда), т.е переинициализируем
    create_dir(folder_name)
    subprocess.call(["git", "clone", repo_url, folder_name])

def change_working_folder(path):
    os.chdir(path)

def get_file_lines(path):
    with open(path) as file_handler:
        return file_handler.readlines()

#этот метод должен вызываться после перехода в папку с репозиторием
def get_sol_files_names_from_diff(before_audit_hash, after_audit_hash):
    # создаем файлик со всеми именами файлов из diff'а
    tmp_names_file = "tmp_names.txt"
    os.system("git diff --name-only " + before_audit_hash + "^.." + after_audit_hash + " > " + tmp_names_file)

    # получаем список строк с именами .sol файлов
    res = [ line.strip() for line in get_file_lines(tmp_names_file) if line.strip().endswith(".sol")]
    # удаляем файлик (мы его много где используем и создаем)
    os.system("rm -f " + tmp_names_file)
    return res


def get_diff_as_string(before_audit_hash, after_audit_hash, file_name):
    # функция возвращает разницу из файла(before_audit_hash, after_audit_hash) file_name в строковом виде
    tmp_names_file = "tmp_diff_file.txt"
    # file name should be declared  (file_name)
    os.system("git diff " + before_audit_hash + "^.." + after_audit_hash + " "  + file_name + " > " + tmp_names_file)
    res =  ''.join(get_file_lines(tmp_names_file))
    # the file tmp_diff_file.txt must be deleted afterwards !!!
    #I mean right here!!!
    return res

#git diff test.yml | grep '^+'


#этот метод должен вызываться после перехода в папку с репозиторием
def get_sol_file_diff(before_audit_hash, after_audit_hash, file_name):
    # создаем файлик со всеми именами файлов из diff'а
    tmp_names_file = "tmp_names.txt"
    os.system("git diff " + before_audit_hash + "^.." + after_audit_hash + " " + file_name + " > " + tmp_names_file)
    return ''.join(get_file_lines(tmp_names_file))

#def add_data(url,h_before,h_after,code_b_a,diff):
#    c.execute("INSERT INTO smart_contract_database_new (repo_url,hash_commit_before_audit, hash_commit_after_audit,code_before_after_audit, diff) VALUES (%s,%s,%s,%s,%s)" % (url,h_before,h_after,code_b_a,diff))
#    con.commit()

#run only if this
if __name__ == "__main__":
    #clone_repo("https://github.com/AugurProject/augur-core.git")
    #переходим в скачанную папку
    change_working_folder("tmp_repo")
    db_url = "github.com/AugurProject/augur-core.git"
    before_audit_hash = "45e1afb7eb1a895d923c97fe01e068c772c583ef"
    after_audit_hash = "3b5a63d372d205a0214e3061293d5bca0fd5636a"
    diff = 'diff'

    for file_name in get_sol_files_names_from_diff(before_audit_hash, after_audit_hash):
        # выводим на экран diff для одного файла (поэтому break и стоит)
        #print(get_sol_file_diff(before_audit_hash, after_audit_hash, file_name))
        #res = subprocess.call(["git", "diff", before_audit_hash + "^.." + after_audit_hash, file_name])
        plus_minus_diff_for_a_line = get_diff_as_string(before_audit_hash, after_audit_hash, file_name)
# строка с диффом хранится в одной переменной
        print(plus_minus_diff_for_a_line)
        break
    '''
    get_diff_as_string дает дифф для для файла
     mb нужно разделить его (то есть полученну строку) на 2 файла с плюсиками и минусики
     может быть, есть способ это сделать прямо из гита
     если это можно сделать, то нужно разделить метод get_diff_as_string на 2 метода для получения двух различных строк
      Это bудет удобно для дампа в базу.
    '''

        #Добавляем данные в таблицу
        # cursor.execute(' INSERT INTO smart_contract_database VALUES("URL", "hash_before", "hash_after", "code_before", "code_after", "Difference")')
    # 1-поле наименование файла .sol до, 2, 3 - содержимое файла до\после коммита, 4 - содержимое диффа + рисунок архитектуры
    conn = sqlite3.connect(
            "C:/Users/Лада/PycharmProjects/nir_winter_2018/scripts/sqlitescripts/smart-contracts_database.db")  # или :memory: чтобы сохранить в RAM
    cursor = conn.cursor()
    data1 = "github.com/AugurProject/augur-core.git"
    data2 = "45e1afb7eb1a895d923c97fe01e068c772c583ef"
    data3 = "3b5a63d372d205a0214e3061293d5bca0fd5636a"
    data4 = plus_minus_diff_for_a_line
    print(type(data4))
    cursor.execute("INSERT INTO smart_contract_database VALUES (?, ?, ?, ?)", (data1, data2, data3, data4))
        # Записываем изменения
        # Разрываем соединение с базой
    conn.commit()
    cursor.close()
    conn.close()


     #c.close()
    #con.close()
    #res = subprocess.call(["git", "diff",  "--name-only", before_audit_hash + "^.." + after_audit_hash])





    #change_working_folder("..")
    #удаляем репозиторий
    #delete_dir()