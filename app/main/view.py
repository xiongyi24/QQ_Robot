from . import main
from flask import request
from json import loads
from .func import main_func 
from loding import loding_config 

@main.route('/api',methods=['POST'])
def function():
    msg = request.get_data().decode('utf-8')
    msg = loads(msg)

    reply_msg = {}

    if msg['post_type'] == 'message':
        if msg['message_type'] == 'group' and msg['group_id'] == loding_config.group_id :  
            if msg['message'][0] == {'data': {'qq': str(loding_config.my_id)}, 'type': 'at'} :
                message = main_func(msg)
                reply_msg = {
                    'reply' : message,
                    'at_sender': True
                }
        
    return reply_msg