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

    def rename_my_rune(self):
        if len(self.my_rune_listbox.curselection()) <= 0:
            utils.error("请选择要重命名的天赋!")
            return

        index = self.my_rune_listbox.index(self.my_rune_listbox.curselection())

        input_box = Tk()
        input_box.title("重命名")
        center_window(input_box, 230, 100)
        label = Label(input_box, text="请输入天赋名称：")
        label.pack()

        rune_text = StringVar()
        rune_entry = Entry(input_box, textvariable=rune_text)
        rune_entry.pack()

        def rename_rune():
            rune_name = rune_entry.get()
            if rune_name is None or rune_name.strip() == "":
                utils.error("天赋名称不能为空")
                # 防止弹出提示框后，input_box变到最底层
                input_box.lift()
                return

            old_filepath = './runes/' + self.my_runes[index]
            new_filepath = './runes/' + rune_name + ".rune"
            os.rename(old_filepath, new_filepath)
            self.refresh_my_runes()
            input_box.destroy()

        Button(input_box, text="确认", command=rename_rune).pack()
        input_box.mainloop()

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


def center_window(root, w, h):
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    # 计算 x, y 位置
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))


def launch():
    rune_state = RuneState()

    root = Tk()  # 根节点
    root.title('LOL一键自定义符文')
    center_window(root, 550, 450)
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
    my_rune_label.place(x=280, y=50, width=60, height=20)

    my_rune_listbox_var = StringVar(value=rune_state.get_my_runes())
    my_rune_listbox = Listbox(master=root, listvariable=my_rune_listbox_var)
    my_rune_listbox.place(x=290, y=70, width=180, height=360)

    rune_state.my_rune_listbox = my_rune_listbox
    rune_state.my_rune_listbox_var = my_rune_listbox_var

    load_button = Button(root, text='一键载入', command=rune_state.load_rune)
    load_button.place(x=480, y=70, width=60, height=30)

    delete_button = Button(root, text='删除', command=rune_state.delete_my_rune)
    delete_button.place(x=480, y=110, width=60, height=30)

    rename_button = Button(root, text='重命名', command=rune_state.rename_my_rune)
    rename_button.place(x=480, y=150, width=60, height=30)

    root.mainloop()


if __name__ == '__main__':
    launch()
