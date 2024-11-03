import json
import sqlite3 as sql

class MetaSingleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Drive_DB(metaclass=MetaSingleton):
    
    def __init__(self,db_name):
        self.db_name = db_name;
        try:
            self.connection = sql.connect(self.db_name)
            self.cursor = self.connection.cursor()
        except ValueError:
            print('Error Connect')

    def __del__(self):
        self.connection.close()

    def fetch(self, sql_command, data):
        self.cursor.execute(sql_command, data)
        return self.cursor.fetchone()

    def commit(self, sql_command, data):
        self.cursor.execute(sql_command, data)
        self.connection.commit()


class Driver_FSM(Drive_DB):

    def find_fsm(self, u_id):
        sql_find = "SELECT id FROM User_step WHERE u_id = ?;"
        if self.fetch(sql_find, (u_id,)) == None:
            return False
        else: 
            return True

    def read_fsm(self, u_id):
        sql_status = "SELECT u_info FROM User_step WHERE u_id = ?;"
        return json.loads(self.fetch(sql_status, (u_id,))[0])

    def commit_fsm(self, u_id, u_fsm):
        if self.find_fsm(u_id): 
            sql = 'UPDATE User_step SET u_info = ? WHERE u_id = ?;'
            self.commit(sql, (json.dumps(u_fsm), u_id,))
        else:
            sql = 'INSERT INTO User_step (u_id, u_info) VALUES (?,?);'
            self.commit(sql, (u_id, json.dumps(u_fsm),))

class Driver_MSG(Drive_DB):

    def find_msg(self, msg_id):
        sql_find = "SELECT u_id FROM User_Msg WHERE id = ?;"
        if self.fetch(sql_find, (msg_id,)) == None:
            return False
        else: 
            return True

    def read_msg(self, msg_id):
        sql_status = "SELECT msg_data FROM User_Msg WHERE id = ?;"
        return json.loads(self.fetch(sql_status, (msg_id,))[0])

    def commit_msg(self, msg_id, msg_data):
        if self.find_msg(msg_id):
            sql = 'UPDATE User_Msg SET msg_data = ? WHERE id = ?;'
            self.commit(sql, (json.dumps(msg_data), msg_id,))
            
    def new_msg(self, u_id):
            sql = 'INSERT INTO User_Msg (u_id, msg_data) VALUES (?,?);'
            self.commit(sql, (u_id, '',))
            return self.cursor.lastrowid
            
