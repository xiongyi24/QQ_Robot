from .. import db

class Data(db.Model):
    __tablename__ = 'datas'
    id = db.Column(db.Integer, primary_key=True)
    QQ_id = db.Column(db.Integer, unique=True)
    total = db.Column(db.Integer)
    last_commit = db.Column(db.Integer)
    flag = db.Column(db.Integer)    # 记录今日是否打卡 1：已打，0：未打
    auto_remind = db.Column(db.Integer) # 自动提醒打卡 1：开，0：关