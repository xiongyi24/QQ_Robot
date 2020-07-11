import configparser

conf = configparser.ConfigParser()

conf.read('loding/config.ini')

my_id = int(conf.get('CONFIG','my_id'))
group_id = int(conf.get('CONFIG','group_id'))
total_day = int(conf.get('CONFIG','total_day'))
send_id = int(conf.get('CONFIG','send_id'))
