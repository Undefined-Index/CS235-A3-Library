import hashlib
import re

from library.adapters.repository import AbstractRepository
from library.domain.model import User


def login_serv(username: str, password: str, repo: AbstractRepository):
    username = username.strip().lower()
    # Encryption the password
    hl = hashlib.md5()
    hl.update(password.encode("utf-8"))
    pw_md5 = hl.hexdigest()
    for i in repo.get_repo_user():
        if username == i.user_name and pw_md5 == i.password:
            return True
    return False


def register_serv(username: str, password: str, repo: AbstractRepository):
    if len(username) < 1 or re.search(r"\W", password) != None:
        return 3
    if len(password) < 8 or len(password) > 20 or re.search(r"\W", password) != None:
        return 1
    # Encryption the password
    hl = hashlib.md5()
    hl.update(password.encode("utf-8"))
    pw_md5 = hl.hexdigest()
    U = User(username, pw_md5)
    if U not in repo.get_repo_user():
        repo.add_repo_user(U)
        return True
    else:
        return 2


# test purpose
def get_user_dict(username: str, repo: AbstractRepository):
    users = repo.get_repo_user()
    for user in users:
        if user.user_name == username:
            return {
                'user_name': user.user_name,
                'password': user.password
            }
    return None
