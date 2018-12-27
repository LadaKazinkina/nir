from scripts.gitscripts.git_processing import *

folder = 'scripts\\gitscripts\\tmp_repo'
delete_dir(folder)
clone_repo("https://github.com/AugurProject/augur-core.git", folder)

