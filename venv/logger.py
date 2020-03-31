from conf import LOGS_ROOT_PATH
from datetime import date, datetime
import json

def write_log(msg, error):
    with open(LOGS_ROOT_PATH + str(date.today())+'.txt' , 'a+') as log_file:
        log_file.write(json.dumps(create_log_msg(msg, error))+'\n')
        
def create_log_msg(msg, error):
    log_msg = {'time': str(datetime.now()),
               'error' : error,
               'msg' : msg}
    return log_msg