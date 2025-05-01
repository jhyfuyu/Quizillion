import time 
import os.path
import sqlite3
from typing import List, Any
from typing import Callable

DATABASE: str = os.path.join("database", "database.db")
TABLE: str = 'users'

def registration_user_in_bd(tg_id: str, username: str) -> None:
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute(
        f"INSERT INTO {TABLE} (tg_id, username, balance, count, income_count, correct_answer, exc_flag, ref) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
        (tg_id, username, 0, 0, 0, 0, False, 0)
    )
    cursor.execute(
        f"update {TABLE} set correct_answer=0 where tg_id={tg_id}"
    )
    connection.commit()
    connection.close()


def get_data_from_database(tg_id, value='*') -> Any: # Rename function to tg
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute(f"SELECT balance FROM {TABLE} WHERE tg_id={tg_id}")
        result = cursor.fetchall()
    return result


def raise_income(tg_id, value=20) -> None:
    """ Подсчёт заработка монеток за викторины """
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute(f"SELECT income_count FROM {TABLE} WHERE tg_id={tg_id}")
        old_income = cursor.fetchall()
        cursor.execute(
            f"UPDATE {TABLE} SET income_count={old_income[0][0] + value} WHERE tg_id={tg_id}"
        )


def raise_balance(tg_id, raise_value=20) -> None:
    """ Заработок монеток за викторины """
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute(f"SELECT balance FROM {TABLE} WHERE tg_id={tg_id}")
        old_value = cursor.fetchall()
        cursor.execute(
            f"UPDATE {TABLE} SET balance={old_value[0][0] + raise_value} WHERE tg_id={tg_id}"
        )


def register_data(tg_id, request) -> None:
    """ Многофункциональный метод для отправки запросов к БД""" 
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute(request)
        value = cursor.fetchall()
    return value


def select_flag_bonus(tg_id, flag) -> None:
    """ Флаг по бонусу за подписку """
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute(
            f"SELECT ch_{flag} FROM {TABLE} WHERE tg_id={tg_id}"
        ) 
        value = cursor.fetchall()
    return value


def raise_counter(tg_id, raise_value=1, income=False) -> None:
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute(f"SELECT count FROM {TABLE} WHERE tg_id={tg_id}")
        old_value = cursor.fetchall()

        print(old_value)
        cursor.execute(
            f"UPDATE {TABLE} SET count={old_value[0][0] + raise_value} WHERE tg_id={tg_id}"
        )


def zero_income(tg_id) -> None:
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute(
            f"UPDATE {TABLE} SET income_count=0 WHERE tg_id={tg_id}"
        )


def zero_count(tg_id) -> None:
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute(
                f"UPDATE {TABLE} SET count=0 WHERE tg_id={tg_id}"
            )


def get_count(tg_id) -> Any:
    """ Вывод счётчика """
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute(
            f"SELECT count FROM users WHERE tg_id={tg_id}"
        )
        value = cursor.fetchall()
    return value[0][0]


def get_income_from_db(tg_id) -> Any:
    """ Вывод дохода на экран """
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute(
            f"SELECT income_count FROM users WHERE tg_id={tg_id}"
        )
        value = cursor.fetchall()
    return value[0][0]


def create_table_ref(tg_id) -> None:
    register_data(tg_id, f"CREATE TABLE IF NOT EXISTS {tg_id} (id INTEGER PRIMARY KEY AUTOINCREMENT, referal1 TEXT, referal2 TEXT, referal3 TEXT, reward BOOLEAN)")


def add_referal(referer_id, tg_id: str, referal_level: str) -> None:
    register_data(tg_id, f"INSERT INTO {referer_id} ({referal_level}) VALUES ({tg_id})")


def find_table_with_referer(referer):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Получение списка всех таблиц в базе данных
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    for table in tables[2:]:
        cursor.execute(f"SELECT referal1 FROM {table}")
        tables_1 = cursor.fetchall()

        if f'a{tables_1[0][0]}' == referer:
            return table
    return None


def select_referal_from_table(tg_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT referal1, referal2, referal3 FROM tg_id")
    return cursor.fetchall()


def get_count_exc(table_name="exc") -> Any:
    with sqlite3.connect(DATABASE) as connection:
        try:
            cursor = connection.cursor()
            cursor.execute(f"select count (*) from {table_name}")
            res = cursor.fetchall()
        except Exception as exc:
            res = [[(0)]]
    return res[0][0]


def raise_ref(num: int, id: str) -> Any:
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute(f"update users set ref={num} where tg_id={id}")


def select_quiz_data(num: int, uid: str) -> None:
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute(f"update users set quiz={num} where tg_id={uid}")


def check_quiz_number(uid: str) -> int:
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute(f"select quiz from users where tg_id={uid}")
        result = cursor.fetchall()
    return result[0][0]


def get_quiz_key(quiz: str, uid: str) -> str:
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute(f"select quiz_key{quiz} from users where tg_id={uid}")
        result = cursor.fetchall()
    return result[0][0]


def reject_this_quiz(qid: int, uid: str, unique_key: str) -> None:
    quiz_string: str = ''
    qid = int(qid)

    if qid == 1: 
        quiz_string = 'quiz_key1' 
    if qid == 2: 
        quiz_string = 'quiz_key2' 
    if qid == 3: 
        quiz_string = 'quiz_key3' 

    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute(f'update users set {quiz_string}="{unique_key}" where tg_id="{uid}"')


def get_quiz_end(uid: str) -> Any:
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        res = cursor.execute(f'select v_end from users where tg_id={uid}').fetchall()
        return res[0][0]
