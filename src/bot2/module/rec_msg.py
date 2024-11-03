class Rec_MSG():
    def __init__(self, u_id):
        self.u_id = u_id
        self.msg_status = 0
        self.msg_date = ''
        self.msg_time = ''
        self.msg_header = ''
        self.msg_link = ''
        self.msg_about = ''
        self.msg_pic = ''
        
        
    def set(self, in_date):
        self.u_id = in_date['u_id']
        self.msg_status = in_date['msg_status']
        self.msg_date = in_date['msg_date']
        self.msg_time = in_date['msg_time']
        self.msg_header = in_date['msg_header']
        self.msg_link = in_date['msg_link']
        self.msg_about = in_date['msg_about']
        self.msg_pic = in_date['msg_pic']

    def get(self):
        return {\
         'u_id' : self.u_id,\
         'msg_status': self.msg_status,\
         'msg_date': self.msg_date,\
         'msg_time': self.msg_time,\
         'msg_header': self.msg_header,\
         'msg_link': self.msg_link,\
         'msg_about': self.msg_about,\
         'msg_pic': self.msg_pic\
         }
