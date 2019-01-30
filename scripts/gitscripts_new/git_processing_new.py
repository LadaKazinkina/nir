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

def make_empty_diff_for_del_file(query, before_audit_hash, delete_file):
    os.system("git reset --hard " + before_audit_hash)
    xx = get_file_lines(delete_file)
    result = "файл был удален\n" + query + '\n-' + '-'.join(xx)
    return result

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

    try:
        os.remove(".git/index.lock")
    except:
        pass


    db_url = "github.com/AugurProject/augur-core.git"
    before_audit_hash = "45e1afb7eb1a895d923c97fe01e068c772c583ef"
    after_audit_hash = "3b5a63d372d205a0214e3061293d5bca0fd5636a"
    diff = 'diff'

    mass = get_sol_files_names_from_diff(before_audit_hash, after_audit_hash)

    conn = sqlite3.connect(
        "C:/Users/Лада/PycharmProjects/nir_winter_2018/scripts/sqlitescripts/smart-contracts_database.db")
    cursor = conn.cursor()
    for file_name in mass:
        plus_minus_diff_for_a_line = None

        # откат на старый коммит
        os.system("git reset --hard " + before_audit_hash)

        # считываем файл из старого коммита
        try:
            code_file_before = ''.join(get_file_lines(file_name))
        except:
            # файла может и не быть (он появился после первого коммита), тогда записываем пустую строку
            code_file_before = ""

        # перекатываемся в новый коммит
        os.system("git reset --hard " + after_audit_hash)

        # считываем файл из нового коммита
        try:
            code_file_after = ''.join(get_file_lines(file_name))
        except:
            # файла может и не быть - удалили , поэтому там пустота
            code_file_after = ""
            # а в дельту записываем старый файл с "-"
            query = "diff --git " + before_audit_hash + " " + after_audit_hash
            plus_minus_diff_for_a_line = make_empty_diff_for_del_file(query, before_audit_hash, file_name)

        # если еще не считывали дельту, то считываем дельту
        if not plus_minus_diff_for_a_line:
            plus_minus_diff_for_a_line = get_diff_as_string(before_audit_hash, after_audit_hash, file_name)

        # если файла не было, но появился, то добавим к дельте уведомление
        if code_file_before == "":
            plus_minus_diff_for_a_line = "файл был создан\n" + plus_minus_diff_for_a_line

        data = (
            file_name,
            code_file_before,
            code_file_after,
            plus_minus_diff_for_a_line
        )
        cursor.execute("INSERT INTO smart_contract_database VALUES (?, ?, ?, ?)", data)
        # Записываем изменения
        # Разрываем соединение с базой
        conn.commit()
        print(file_name)

    cursor.close()
    conn.close()
    print("end")
