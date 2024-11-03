class Rec_FSM():
    def __init__(self, u_id):
        self.u_id = u_id
        self.u_block = 0
        self.u_name = ''
        self.u_fsm = 0
        self.m_edit = 0
        self.u_msg_id =0

    def set(self, in_date):
        self.u_id = in_date['u_id']
        self.u_block = in_date['u_block']
        self.u_name = in_date['u_name']
        self.u_fsm = in_date['u_fsm']
        self.m_edit = in_date['m_edit']
        self.u_msg_id = in_date['u_msg_id']

    def get(self):
        return {'u_id' : self.u_id, 'u_block' : self.u_block,\
        'u_name':self.u_name, 'u_fsm':self.u_fsm,\
        'm_edit' : self.m_edit, 'u_msg_id': self.u_msg_id}
