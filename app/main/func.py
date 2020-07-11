from .form import Data
from .. import db
import re
import time
from .. import scheduler
import requests
from loding import loding_config 

# 主响应
def main_func(msg):
    message = msg['message'][1]['data']['text']
    get_time = msg['time']
    user_id = msg['user_id']

    return_msg = ''
    
    # 功能：初始化打卡
    if re.search(r'初始化.*?已打卡(\d{0,3})天',message) :
        db.create_all() # 初始化数据库
        # 首先判断是否已初始化
        if Data.query.filter(Data.QQ_id == user_id).first() != None :
            return_msg = '您已初始化，若需打卡请直接@我：打卡,若需删除打卡记录，请@我：删除打卡记录'
        else:
            init_day = int(re.search(r'已打卡(\d{0,3})天',message).group(1))
            data = Data(QQ_id=user_id,total=init_day,last_commit=get_time,flag=0,auto_remind=1)
            db.session.add(data)
            db.session.commit()
            return_msg = "初始化成功，您已成功打卡%d天，还需打卡%d天，继续坚持哟！" % (init_day, loding_config.total_day-init_day)

    # 功能：打卡
    elif message == '打卡' or message == ' 打卡':
        # 首先判断是否存在用户
        user = Data.query.filter(Data.QQ_id == user_id).first()
        if user :
            if user.flag == 0 :
                user.total = user.total + 1
                user.flag = 1
                return_msg = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + '''： 打卡成功！您已成功打卡%d天，还需打卡%d天，继续坚持哟！''' % (user.total, loding_config.total_day-user.total)
            else:
                return_msg = "您今天已经打过卡啦，请明日再来！"
        else:
            return_msg = "您尚未初始化，请先@我：初始化，已打卡x天。再继续操作"

    # 功能：查询打卡记录
    elif re.search(r'查询',message):
        # 首先判断是否存在用户
        user = Data.query.filter(Data.QQ_id == user_id).first()
        if user :
            return_msg = "截止至：" + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + "，您已成功打卡%d天，还需打卡%d天，继续坚持哟！" % (user.total, loding_config.total_day-user.total) 
        else:
            return_msg = "您尚未初始化，请先@我：初始化，已打卡x天。再继续操作"        

    # 功能：删除打卡记录
    elif re.search(r'删除打卡记录',message):
        # 首先判断是否存在用户
        user = Data.query.filter(Data.QQ_id == user_id).first()
        if user :
            db.session.delete(user)
            db.session.commit()
            return_msg = "删除打卡记录成功！"
        else:
            return_msg = "您尚未初始化，请先@我：初始化，已打卡x天。再继续操作"

    # 功能：自动打卡提醒开关
    elif re.search(r'自动打卡提醒',message):
        # 首先判断是否存在用户
        user = Data.query.filter(Data.QQ_id == user_id).first()
        if user :
            if re.search(r'取消',message):
                user.auto_remind = 0
                return_msg = "已取消自动提醒，如需打开，请@我：打开自动打卡提醒"
            elif re.search(r'打开',message):
                user.auto_remind = 1
                return_msg = "已打开自动提醒，如需取消，请@我：取消自动打卡提醒"
            else:
                return_msg = "哇！您输入的指令好像有问题耶，我有点无法理解"

    # 功能：说明
    elif re.search(r'说明',message):
        return_msg = ("\n嗨！我是打卡小助手。\n我能干下面这些事：\n" +
                    "1.初始化打卡：\n @我 初始化，已打卡X天 \n" + 
                    "2.打卡：\n @我 打卡 \n"  +
                    "3.查询打卡记录：\n @我 查询 \n" +
                    "4.删除打卡记录：\n @我 删除打卡记录 \n" +
                    "5.自动打卡提醒: \n 开：@我 打开自动打卡提醒 \n 关：@我 取消自动打卡提醒 \n"  +
                    "自动打卡提醒说明：如果你每天10点后还没打卡，我会私聊提醒你哟")

    else :
        return_msg = "哇！您输入的指令好像有问题耶，我有点无法理解"
    
    return return_msg

# 重置数据库flag
def set_flag():
    with scheduler.app.app_context():
        users = Data.query.filter(Data.flag == 1).all()
        for user in users :
            user.flag = 0
        print(str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + "：数据库flag重置成功！")

# 定时@全体
def at_all():
    data = {
        'group_id': loding_config.group_id,
        'message': '[CQ:at,qq=all] 现在是' + str(time.strftime("%H:%M", time.localtime())) + '，又是元气满满的一天，今天也要打卡鸭！',
        'auto_escape':False
    }
    api_url = 'http://127.0.0.1:5000/send_group_msg'
    requests.post(url=api_url,data=data)
    print(str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + "：发送全体消息成功")

# 自动提醒打卡
def auto_remind():
    with scheduler.app.app_context():
        users = Data.query.filter(Data.flag == 0).all()
        for user in users:
            if user.auto_remind == 1 :
                data = {
                    'user_id': user.QQ_id,
                    'message': '（QQ机器人自动打卡提醒）亲！您今天还未打卡哟！（如需取消，请在群中@我：取消自动打卡提醒）',
                    'auto_escape':False
                }
                api_url = 'http://127.0.0.1:5000/send_private_msg'
                requests.post(url=api_url,data=data)
                print("%d自动打卡提醒成功" % user.QQ_id)

# 发名单
def name_list():
    with scheduler.app.app_context():
        users = Data.query.filter(Data.flag == 0).all()
        name = []
        for user in users:
            name.append(user.QQ_id)
        data = {
            'user_id': loding_config.send_id,
            'message': '今天尚未打卡名单：' + str(name),
            'auto_escape':False
        } 
        api_url = 'http://127.0.0.1:5000/send_private_msg'
        requests.post(url=api_url,data=data)
        print("未打卡名单发送成功" )