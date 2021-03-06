from config import setting
from util import login

db = setting.db


def check(name,info):
    for key in ["name","avatar",name+"_id",name+"_access_token"]:
        # print "key",key
        if not info[key]:
            return "no "+key
    return True

def parse_data(name,info):
    data = {}

    data[name+"_id"] = str(info["id"])
    data["name"] = info["name"]
    data[name+"_access_token"] = info["access_token"]
    
    if name == "douban":
        data["avatar"] = info["avatar"]
    elif name == "weibo":
        data["avatar"] = info["profile_image_url"]
    return data

def new_oauth_user(name,info):
    data = parse_data(name,info)

    if check(name,data):
        return db.insert("user",**data)

def update_oauth_userid(name,id,oauth_id):
    data = {}
    data[name+"_id"] = oauth_id
    db.update("user",where="id=$id",vars={"id":id},**data)

def update_access_token(name,id,token):
    data = {}
    data[name+"_access_token"] = token
    db.update("user",where=name+"_id=$id",vars={"id":id},**data)

def exist_oauth_user(name,info):
    data = parse_data(name,info)
    if not check(name,data):
        return False

    rows = db.select("user",where=name+"_id=$id",vars={"id":data[name+"_id"]})
    if rows:
        return rows[0]
    else:
        return False

def login_oauth_user(name,info):
    data = parse_data(name,info)
    if not check(name,data):
        raise Exception("login arguments error")

    users = db.select("user",where=name+"_id="+data[name+"_id"])
    if not users:
        raise Exception("user not found")

    login.login(users[0]["id"])