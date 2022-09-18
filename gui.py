import json
import os
import tkinter
from tkinter import *

from tkinter import *
import tkinter.messagebox as GUI
from tkinter import messagebox

import utils
from lcu import LCU


class RuneState:

    def __init__(self):
        self.lcu = LCU(*utils.getClientInfo())
        self.game_runes = self.lcu.get_runes()
        self.my_runes = self.load_my_runes()

        self.game_rune_listbox = None
        self.my_rune_listbox = None
        self.game_rune_listbox_var = None
        self.my_rune_listbox_var = None

    def load_rune(self):
        index = self.my_rune_listbox.index(self.my_rune_listbox.curselection())
        self.lcu.delete_one_runes(self.game_runes)
        self.lcu.load_rune(self.my_runes[index])
        self.refresh_game_runes()
        GUI.showinfo(title="成功", message="一键载入天赋成功")

    def delete_my_rune(self):
        r = messagebox.askquestion("提示", "你确定要删除吗？")
        if r == 'no':
            return

        index = self.my_rune_listbox.index(self.my_rune_listbox.curselection())
        filepath = './runes/' + self.my_runes[index]
        os.remove(filepath)
        self.refresh_my_runes()

    def rename_my_runes(self):
        index = self.my_rune_listbox.index(self.my_rune_listbox.curselection())
        filepath = './runes/' + self.my_runes[index]
        os.remove(filepath)
        self.refresh_my_runes()

    def get_game_runes(self):
        return [rune['name'] for rune in self.game_runes]

    def load_my_runes(self):
        files = os.listdir("./runes")
        runes = []
        for item in files:
            if item.endswith(".rune"):
                runes.append(item)

        return runes


    def get_my_runes(self):
        return [item[:-5] for item in self.my_runes]

    def store_rune(self):
        index = self.game_rune_listbox.index(self.game_rune_listbox.curselection())
        self._store_rune(self.game_runes[index])
        self.refresh_my_runes()
        GUI.showinfo(title="成功", message="收藏成功")

    def _store_rune(self, rune):
        rune_name = rune['name'] + '.rune'

        with open('./runes/' + rune_name, mode='w', encoding='utf-8') as f:
            f.write(json.dumps(rune, ensure_ascii=False))

    def refresh_my_runes(self):
        self.my_runes = self.load_my_runes()
        self.my_rune_listbox_var.set(self.get_my_runes())

    def refresh_game_runes(self):
        self.game_runes = self.lcu.get_runes()
        self.game_rune_listbox_var.set(self.get_game_runes())

    def refresh(self):
        self.refresh_my_runes()
        self.refresh_game_runes()



def addMyMsg():
    global root
    new_label = Label(root, text="Hi, Ling Liu!", background='green')
    new_label.pack(side=TOP)


def launch():
    rune_state = RuneState()

    root = Tk()  # 根节点
    root.title('LOL一键自定义符文')
    root.geometry('550x450')
    refresh_button = Button(root, text='刷新', command=rune_state.refresh)
    refresh_button.place(x=10, y=10, width=60, height=30)

    game_rune_label = Label(root, text="游戏符文")
    game_rune_label.place(x=6, y=50, width=60, height=20)

    game_rune_listbox_var = StringVar(value=rune_state.get_game_runes())
    game_rune_listbox = Listbox(master=root, listvariable=game_rune_listbox_var)
    game_rune_listbox.place(x=10, y=70, width=180, height=360)

    rune_state.game_rune_listbox = game_rune_listbox
    rune_state.game_rune_listbox_var = game_rune_listbox_var

    store_button = Button(root, text='收藏', command=rune_state.store_rune)
    store_button.place(x=200, y=70, width=60, height=30)

    my_rune_label = Label(root, text="我的收藏")
    my_rune_label.place(x=276, y=50, width=60, height=20)

    my_rune_listbox_var = StringVar(value=rune_state.get_my_runes())
    my_rune_listbox = Listbox(master=root, listvariable=my_rune_listbox_var)
    my_rune_listbox.place(x=290, y=70, width=180, height=360)

    rune_state.my_rune_listbox = my_rune_listbox
    rune_state.my_rune_listbox_var = my_rune_listbox_var

    load_button = Button(root, text='一键载入', command=rune_state.load_rune)
    load_button.place(x=480, y=70, width=60, height=30)

    load_button = Button(root, text='删除', command=rune_state.delete_my_rune)
    load_button.place(x=480, y=110, width=60, height=30)

    root.mainloop()


if __name__ == '__main__':
    launch()
