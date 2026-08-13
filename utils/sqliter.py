import sqlite3
from loguru import logger
import datetime


class Sqlite:

    def __init__(self, db_file: str) -> None:
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def user_in_bd(self, user_id: str) -> None:
        txt = ''
        check = self.cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
        if check.fetchone() is None:
            self.cursor.execute('INSERT INTO users VALUES(?, ?, ?)', (user_id, txt, txt))
            self.cursor.execute('INSERT INTO personal_account VALUES(?, ?, ?, ?, ?, ?, ?)', (user_id, 0, 0, 0, txt, txt, txt))
            self.conn.commit()
            logger.info(f'Новый пользователь--{user_id}')
        else:
            logger.info(f'Пользователь есть--{user_id}')

    def add_second_id(self, user_id: str, second_id: str) -> None:
        self.cursor.execute("UPDATE users SET second_id=? WHERE user_id=?", (user_id, second_id))
        self.cursor.execute("UPDATE users SET second_id=? WHERE user_id=?", (second_id, user_id))
        self.conn.commit()

    def add_feed_back(self, feedback: str, user_id: str) -> None:
        self.cursor.execute("UPDATE personal_account SET feedback=? WHERE user_id=?", (feedback, user_id))
        self.conn.commit()

    def add_question(self, user_id: str, question: str) -> None:
        self.cursor.execute("UPDATE personal_account SET qestion=? WHERE user_id=?", (question, user_id))
        self.conn.commit()

    def take_second_id(self, user_id: str) -> None:
        sec_id = self.cursor.execute("SELECT second_id FROM users WHERE user_id=?", (user_id,)).fetchone()[0]
        return sec_id

    def add_money(self, first_id: str,  second_id: str, money: str) -> None:
        self.cursor.execute("UPDATE users SET price=? WHERE user_id=?", (money, first_id))
        self.cursor.execute("UPDATE users SET price=? WHERE user_id=?", (money, second_id))
        self.conn.commit()

    def get_money_for_pay(self, user_id: str) -> int:
        money = self.cursor.execute("SELECT price FROM users WHERE user_id=?", (user_id, )).fetchone()[0]
        return money

    def get_feed_back(self) -> sqlite3.Cursor:
        feedback = self.cursor.execute("SELECT feedback FROM personal_account")
        return feedback

    def get_question(self) -> sqlite3.Cursor:
        question = self.cursor.execute("SELECT * FROM users")
        return question

    def get_all_id(self) -> sqlite3.Cursor:
        users_id = self.cursor.execute("SELECT user_id FROM users")
        return users_id

    def add_count(self, counter: str, user_id: str) -> None:
        self.cursor.execute("UPDATE personal_account SET count=? WHERE user_id=?", (counter, user_id))
        self.conn.commit()

    def add_pay(self, pay: str, user_id: str) -> None:
        self.cursor.execute("UPDATE personal_account SET pay=? WHERE user_id=?", (pay, user_id))
        self.conn.commit()

    def add_sold(self, sold: str, user_id: str) -> None:
        self.cursor.execute("UPDATE personal_account SET sold=? WHERE user_id=?", (sold, user_id))
        self.conn.commit()

    def get_all_information(self, user_id: str) -> tuple:
        count = self.cursor.execute("SELECT count FROM personal_account WHERE user_id=?",  (user_id, )).fetchone()[0]
        pay = self.cursor.execute("SELECT pay FROM personal_account WHERE user_id=?", (user_id, )).fetchone()[0]
        sold = self.cursor.execute("SELECT sold FROM personal_account WHERE user_id=?", (user_id, )).fetchone()[0]
        return pay, count, sold

    def add_history(self, history: str, user_id: str) -> None:
        history_list = []
        hist = self.cursor.execute("SELECT history FROM personal_account WHERE user_id=?", (user_id, )).fetchone()[0]
        history_list.append(hist)
        history_list.append(history)
        all_history = ''
        for i_history in history_list:
            all_history += '\n\n' + i_history + f"Время проведения сделки: {datetime.datetime.now()}\n"
        self.cursor.execute("UPDATE personal_account SET history=? WHERE user_id=?", (all_history, user_id))
        self.conn.commit()

    def get_users_history(self, user_id: str) -> str:
        hist = self.cursor.execute("SELECT history FROM personal_account WHERE user_id=?", (user_id,)).fetchone()[0]
        return hist
