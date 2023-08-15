'''
Netease Minecraft Nickname Random by wangyupu
使用来自网易的词典
全部使用built-in库
可自定义
'''
import random
import os
import hashlib
import time
import tkinter as tk
from tkinter import messagebox as tkmb
import json

# 名称的结构 可配置
# 前缀、人名、人物、动词、形容、物品 填入为随机
# 以+分割
# 比如 "前缀+人名+动词" 就是随机从前缀、人名、动词中选词再拼接
# 如果要强制制定词，可使用 "#字词"，比如："前缀+#的"就是随机的前缀拼接一个"的"字
# 格式是python字典，不可缺逗号
# 如果在末尾留下了+号会报错，注意格式
# 没有使用eval、exec之类的不安全实现
#
# default:
# name_stru = {1:"前缀+人名+动词",2:"前缀+人物+动词",
#           3:"前缀+人物+动词",4:"前缀+形容+人名",
#           5:"前缀+动词+人物",6:"前缀+动词+人名",
#           7:"人名+#的+前缀+物品",}

# 不要改啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊
_version = 0.1
application_title = "Netease Minecraft Nickname Random"
application_author = "wangyupu"
application_start_time = time.time()
print(f"{application_title} {_version}\nAuthor:{application_author}")
# 获取目录
path = __file__
path = path[:len(path)-7]
os.chdir(path)
#print(f"当前目录:{path}")

# 处理db
dbfs = os.listdir("./db/")
dbs = {}
f2s = {}
try:
    dbfs.remove(".DS_Store")
    dbfs.remove("字到音")
except: 
    pass
##print(f"获取到的名称片段:{dbfs}")
# 写入变量
for filename in dbfs:
    with open(f"{path}db/{filename}",mode='r') as file:
        dbs[filename] = file.read().split("\n")

with open(f"{path}db/字到音",mode='r') as file:
    lines = file.read().split('\n')
    for item in lines:
        lineitems = item.split(',')
        f2s[lineitems[0]] = lineitems[1]

name_stru = {}
name_stru_keys = []
with open(f"{path}name_strus.json",mode='r') as file:
    name_stru = json.load(file) # type: ignore

for k,v in name_stru.items():
    name_stru_keys.append(k)

##print("加载db成功")

# 主
def init_random():
    seed = (hashlib.sha512(str(time.time()).encode()).hexdigest())[:8]
    seed = int(seed,16)
    ##print(f"初始化到种子{seed}")
    random.seed(seed)

def random_nickname():
    nickname_type = random.choice(name_stru_keys)
    nick = ""
    parts = []

    thisnickname_stru = (name_stru[nickname_type]).split("+")
    for item in thisnickname_stru:
        if str(item)[0] == "#":
            thispart = item[1:]
        else:
            thispart = random.choice(dbs[item])
        parts.append(thispart)
        nick = nick+thispart

    return nick,nickname_type,parts

w = tk.Tk()
w.title(f"网易MC名称生成器 {_version}")
w.resizable(False,False)
history = []
#w.overrideredirect(True)

# 计算居中位置
def first_center_window(winx=375,winy=150):
    outx = int((w.winfo_screenwidth()-winx)/2)
    outy = int((w.winfo_screenheight()-winy)/2)
    w.geometry(f"{winx}x{winy}+{outx}+{outy}")

def center_window(winx=375,winy=150):
    w.geometry(f"{winx}x{winy}")

first_center_window()
# 全局变量
nickname_attrs = ()
attrshow = False

# 素材加载
asset_dice_0 = tk.PhotoImage(file="./assets/ui/dice_0.png")
asset_checked = tk.PhotoImage(file="./assets/ui/green_check.png")
asset_redcross = tk.PhotoImage(file="./assets/ui/red_cross.png")
asset_seedinit = tk.PhotoImage(file="./assets/ui/refresh_seed.png")

# 回调定义
def exit_program():
    writein_history()

def rnname(event=0):
    global nickname_attrs
    rnnametotal = len(history)
    if rnnametotal < 1000:
        nick = random_nickname()
        nameentrytext.set(nick[0])
        nickname_attrs = nick
        appendnick = list(nick)
        appendnick.append(time.time())
        history.append(appendnick)
        refresh_attrshow()
    else:
        tkmb.showinfo("网易MC名称生成器","随机的次数过多，历史爆炸")

def readled_time(timestamp):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))


def print_history(event=0):
    print(f'从 {readled_time(application_start_time)} 到 {readled_time(time.time())} 的历史:')
    for item in history:
        line = f"时间: {readled_time(item[3])} | 随机的名称: {item[0]} | 使用的生成器: {item[1]} | 分段: {item[2]}"
        print(line)
    print("+--------------")
    tkmb.showinfo("网易MC名称生成器","历史记录已输出到STDOUT")

def show_history(event=0):
    shw = tk.Toplevel(w)
    shw.title(f'从 {readled_time(application_start_time)} 到 {readled_time(time.time())} 的历史记录:')

    tx = tk.Text(shw)
    tx.pack(fill=tk.BOTH,expand=True)
    # 格式化历史记录并显示
    for item in history:
        fds = ''
        for part in item[2]: # type: ignore
            fds = fds+" "+part+";"
        line = f"时间: {readled_time(item[3])} | 随机的名称: {item[0]} | 使用的生成器: {item[1]} | 分段: {fds}\n"
        tx.insert(tk.END,line)
    # 锁定控件
    tx.config(state=tk.DISABLED)

    shw.mainloop()

def writein_history():
    # 获取历史文件编号
    historypath = path+"/history/"
    filenameextra = 'wffz'
    historys = os.listdir(historypath)
    # 移除
    try:
        historys.remove(".DS_Store")
    except:
        pass
    for item in historys:
        if item.split(".")[-1] != filenameextra:
            try:
                historys.remove(item)
            except:
                pass
    max_num = 0
    for item in historys:
        this_num = (item.split(".")[1])
        if int(max_num) < int(this_num):
            max_num = this_num
    this_num = int(max_num) + 1

    # 格式化历史列表
    wrote_hist = ""
    for item in history:
        wrote_hist += f"{item[0]}..{item[1]}..{item[2]}..{item[3]}"
        wrote_hist += "\n"

    wrote_hist += f"#0~{application_start_time}~{time.time()}"

    # 写入历史文件
    

    with open(f"{historypath}nemcrng_history.{this_num}.{filenameextra}",mode='w') as file:
        file.write(wrote_hist)

    w.destroy()
    print(f"Write history to {this_num}.{filenameextra}")
    print("Goodbye!")

w.protocol('WM_DELETE_WINDOW', writein_history)

def check_name_unicode_space(name):
    max_area = 0xa490

    for item in name:
        if ord(item) > max_area:
            return False
        
    return True

def name2pinyin(name):
    res = ''
    for item in name:
        try:
            res = res+f2s[item]
        except KeyError:
            res = res+item
    return res

def name2pinyin_rev(name):
    res = ''
    for item in name:
        try:
            res = f2s[item]+res
        except KeyError:
            res = item+res
    return res

bad_words = "sabi/sb/shabi/dafeiji/sese/chuo/http/https/www/jiba/weiguang/zhilang/250/520/nima/niba/woba/woma/woshinima/nijia\
giegie/daxiong/xiongda/zhanai/niuniu/jiji/penis/yindao/yingdao/yinhui/yinghui/dadoudou".split("/")
bad_words_raw = "胸/寄吧/傻/傻子/傻逼".split("/")
badreason = []
def check_name_words_fx(pyname,name):
    signal = True
    badstep = 0
    badstep_reason = {0:"未知",1:"含有不当字词",2:"混淆判断:含有不当字词",3:"去间隔后混淆判断:有不当字词",4:"去间隔后判断含有不当字词"}
    badword = ''
    # 判断字
    for item in bad_words_raw:
        if item in name:
            signal = False
            badstep = 1
            badword = item
    # 判断同音字
    for item in bad_words:
        if item in pyname:
            #print(f"敏感词:{item}")
            signal = False
            badstep = 2
            badword = item

    if signal: # 去间隔判断 同音字
        maybe_seps = ". , / * $ ¥ # @ ! ， 。 ！？0 1 2 3 4 5 6 7 8 9".split(' ')
        for item in maybe_seps:
            pyname = pyname.replace(item,"")
            badword = item
        
        # and 再来一次！
        for item in bad_words:
            if item in pyname:
                #print(f"敏感词:{item}")
                signal = False
                badstep = 3
                badword = item

    if signal: # 去间隔判断
        maybe_seps = ". , / * $ ¥ # @ ! ， 。 ！？0 1 2 3 4 5 6 7 8 9".split(' ')
        for item in maybe_seps:
            name = name.replace(item,"")
        
        # and 再来一次！
        for item in bad_words_raw:
            if item in name:
                #print(f"敏感词:{item}")
                signal = False
                badstep = 4

    if signal == False:
        global badreason
        badreason = []
        badreason.append(badstep)
        try:
            badreason.append(badstep_reason[badstep])
        except:
            badreason.append('未知')
        badreason.append(badword)
        attrshow_showwhybad()
    return signal

def check_name_words(name):
    # 正着判断
    pyname_1 = name2pinyin(name)
    sig1 = check_name_words_fx(pyname_1,name)

    # 倒着判断
    pyname_2 = name2pinyin_rev(name)
    sig2 = check_name_words_fx(pyname_2,name[::-1])

    if sig1 and sig2:
        return True
    return False

def usname(event=0):
    name = nameentrytext.get()
    if name.strip() == "":
        tkmb.showwarning("网易MC名称生成器","名字不能为空")
    elif name.strip() != name or " " in name or "\\" in name:
        tkmb.showwarning("网易MC名称生成器","名字格式不合法")
    elif len(name) < 5:
        tkmb.showwarning("网易MC名称生成器","名字太短了")
    elif len(name) > 12:
        tkmb.showwarning("网易MC名称生成器","名字太长了(最多12字)")
    elif not(check_name_unicode_space(name)):
        tkmb.showwarning("网易MC名称生成器","存在不合法字符")
    elif not(check_name_words(name)):
        tkmb.showwarning("网易MC名称生成器","含有敏感词语")
    else:
        tkmb.showinfo("网易MC名称生成器",f"恭喜,你叫{name}")

def attshow_toggle(event=0):
    global attrshow
    if attrshow:
        disable_attrshow()
    elif not(attrshow):
        enable_attrshow()

def enable_attrshow(event=0):
    attrshowwid.pack(anchor=tk.NE,expand=True,side=tk.TOP,fill=tk.BOTH)
    center_window(winy=200)
    global attrshow
    attrshow = True
    refresh_attrshow()

def disable_attrshow(event=0):
    center_window()
    attrshowwid.pack_forget()
    global attrshow
    attrshow = False

def refresh_attrshow(event=0):
    attrshow_clean(event=0)
    global attrshowwid
    if attrshow:
        try:
            fds = ''
            for item in nickname_attrs[2]: # type: ignore
                fds = fds+" "+item+";"
            attrshowwid['text'] = f"F3高级提示:\n名称 : {nickname_attrs[0]}\n生成器 : {nickname_attrs[1]}({name_stru[nickname_attrs[1]]})\n分段 : {fds}" # type: ignore
        except:
            attrshow_clean(event=0)

def attrshow_showwhybad(event=0):
    global badreason
    attrshow_clean()
    if attrshow:
        try:
            showd = f"F3高级提示:\n违规详情:\n违规原因: {badreason[1]} (步骤{badreason[0]})\n违规字词/拼音: {badreason[2]}"
            attrshowwid["text"] = showd
        except:
            pass

def attrshow_clean(event=0):
    attrshowwid["text"] = 'F3高级提示:'

def entry_limit(event=0):
    if len(nameentrytext.get()) > 12:
        nameentrytext.set(nameentrytext.get()[0:12])

# 控件处理
widgets = tk.Frame(width=100,height=50)
nameentrytext = tk.StringVar()
nameentry = tk.Entry(widgets,textvariable=nameentrytext,width=40,font=("",30))
nameentry.pack(fill=tk.X)
attrshowwid = tk.Label(w)
underbtns = tk.Frame(widgets)
tk.Button(underbtns,image=asset_dice_0,command=rnname,name="随机名称").pack(side=tk.LEFT)
tk.Button(underbtns,image=asset_checked,command=usname).pack(side=tk.RIGHT)
tk.Button(underbtns,image=asset_redcross,command=exit_program).pack(side=tk.RIGHT)
tk.Button(underbtns,image=asset_seedinit,command=init_random).pack(side=tk.RIGHT)
underbtns.pack()
widgets.pack()

w.bind_all("<F3>",attshow_toggle) # type: ignore
w.bind_all("<Control-F4>",print_history) # type: ignore
w.bind_all("<F4>",show_history) # type: ignore
nameentry.bind("<Key>",entry_limit) # type: ignore
nameentry.bind("<Return>",usname) # type: ignore

w.mainloop()


