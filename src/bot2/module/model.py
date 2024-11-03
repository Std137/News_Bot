import module.driver_db as driver_db
import module.rec_fsm as rec_fsm
import module.rec_msg as rec_msg

class FSM():
    def __init__(self, db_name: str) -> None:
        self.fsa = {}
        self.db_fsm = driver_db.Driver_FSM(db_name)

    def __getitem__(self, item: str) -> dict:
        if not(item in self.fsa):
            self.find_in_db(item)
        return self.fsa[item].get()

    def __setitem__(self, key, value):
        self.fsa[key].set(value)
        self.db_fsm.commit_fsm(key, self.fsa[key].get())

    def find_in_db(self, u_id):
        self.fsa[u_id] = rec_fsm.Rec_FSM(u_id)
        if not(self.db_fsm.find_fsm(u_id)):
            self.db_fsm.commit_fsm(u_id, self.fsa[u_id].get())
        self.fsa[u_id].set(self.db_fsm.read_fsm(u_id))



class MSG():
    def __init__(self, db_name):
        self.msg = {}
        self.db_msg = driver_db.Driver_MSG(db_name)

    def new(self, u_id):
        new_msg_id = self.db_msg.new_msg(u_id)
        self.msg[new_msg_id] = rec_msg.Rec_MSG(u_id)
        self.db_msg.commit_msg(new_msg_id, self.msg[new_msg_id].get())
        return new_msg_id

    def __getitem__(self, item):
        if not(item in self.msg):
            self.load_in_db(item)
        return self.msg[item].get()

    def __setitem__(self, key, value):
        self.msg[key].set(value)
        self.db_msg.commit_msg(key, self.msg[key].get())

    def load_in_db(self, msg_id):
        self.msg[msg_id] = rec_msg.Rec_MSG(0)
        if self.db_msg.find_msg(msg_id):
          self.msg[msg_id].set(self.db_msg.read_msg(msg_id))


class User_Data():
    def __init__(self, db_name):
        self.msg = MSG(db_name)
        self.fsm = FSM(db_name)

    def __getitem__(self, item):
        fsm_item = self.fsm[item]
        if fsm_item['u_msg_id'] == 0:
            fsm_item['u_msg_id'] = self.msg.new(item)
            self.fsm[item] = fsm_item
        msg_item = self.msg[fsm_item['u_msg_id']]
        return {**fsm_item, **msg_item}

    def __setitem__(self, key, value):
        fsm_item = self.fsm[key]
        msg_item = self.msg[fsm_item['u_msg_id']]
        for keys in fsm_item.keys():
            fsm_item[keys]=value[keys]
        for keys in msg_item.keys():
            msg_item[keys]=value[keys]
        self.fsm[key] = fsm_item
        self.msg[fsm_item['u_msg_id']] = msg_item


    def next_state(self, item, step):
        fsm_item = self.fsm[item]
        if fsm_item['m_edit'] == 1:
            fsm_item['u_fsm'] = 7
            fsm_item['m_edit'] = 0
        else:
            if step == 0:
                fsm_item['u_msg_id'] = self.msg.new(item)
                fsm_item['u_fsm'] = step
            if fsm_item['u_fsm'] == 8:
                fsm_item['m_edit'] = 1
            fsm_item['u_fsm'] = step
        self.fsm[item] = fsm_item

    def msg_finish(self, item):
        self.msg[item]['msg_status'] = 1
