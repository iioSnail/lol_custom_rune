import os
import tkinter.messagebox as GUI

def getClientInfo():
    r = os.popen("wmic PROCESS WHERE name='LeagueClientUx.exe' GET commandline /value")
    text = r.read()
    r.close()
    if len(text) < 50:
        error("获取用户信息失败，请确保已运行游戏和使用管理员身份运行程序！")
        return

    text_items = text.split(" ")

    token = None
    port = None

    for item in text_items:
        item = item.replace('"', '')
        if "--remoting-auth-token" in item:
            index = item.index("=")
            token = item[index + 1:]

        if "--app-port" in item:
            index = item.index("=")
            port = item[index + 1:]

    if token is None:
        error("获取token失败！")
        return

    if port is None:
        error("获取port失败！")
        return

    return token, port

def error(msg):
    GUI.showerror(title="错误", message=msg)




