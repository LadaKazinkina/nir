import subprocess
import os
import re

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


#этот метод должен вызываться после перехода в папку с репозиторием
def get_sol_file_diff(before_audit_hash, after_audit_hash, file_name):
    # создаем файлик со всеми именами файлов из diff'а
    tmp_names_file = "tmp_names.txt"
    os.system("git diff " + before_audit_hash + "^.." + after_audit_hash + " " + file_name + " > " + tmp_names_file)
    return ''.join(get_file_lines(tmp_names_file))


#run only if this
if __name__ == "__main__":
    #clone_repo("https://github.com/AugurProject/augur-core.git")
    #переходим в скачанную папку
    change_working_folder("tmp_repo")
    before_audit_hash = "45e1afb7eb1a895d923c97fe01e068c772c583ef"
    after_audit_hash = "3b5a63d372d205a0214e3061293d5bca0fd5636a"

    for file_name in get_sol_files_names_from_diff(before_audit_hash, after_audit_hash):
        # выводим на экран diff для одного файла (поэтому break и стоит)
        #print(get_sol_file_diff(before_audit_hash, after_audit_hash, file_name))
        subprocess.call(["git", "diff", before_audit_hash + "^.." + after_audit_hash, file_name])
        break


    #res = subprocess.call(["git", "diff",  "--name-only", before_audit_hash + "^.." + after_audit_hash])





    #change_working_folder("..")
    #delete_dir()