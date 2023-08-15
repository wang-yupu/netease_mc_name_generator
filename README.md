# 网易MC名称生成器 · Netease MC Name Generator · NNG
## 快速体验 : 
[在线版本](https://wangyupu.com/tools/tools_netease_nickname_generator)  
## 详情
网易MC名称生成器，分为两个版本:  
1.python版本，使用Tkinter实现GUI。功能多  
2.在线版本，使用js实现。仅实现名称生成  

## 版本特色
| x | / | ? |
| ---- | ---- | ---- |
| 无功能 | 有功能 | 待实现 |

| 功能 | PY版本 | 在线版本 |
| ---------- | ----- | ----- |
| 名称生成 | / | / |
| 自定义词库/名称格式 | / | x |
| 历史记录 | / | x |
| 敏感词检测 | / | x |
| 高级提示 | / | ? |

## 功能详情
### 自定义词库/名称格式
Python版本特有，在 <程序目录>/name_strus.json 可以增加不同的格式。  
在随机生成名称时，会从这些格式中随机选择一个，并且生成。  
格式:  
词库名称 或 #强词  
强词: 强制在名称中插入“#”号后面的字/词  
词库名称: 在名称中插入对应词库中的随机一个词
用 词库名称/强词+词库名称/强词+词库名称/强词。可以无限拼接词库名称/强词。  
中间使用"+"号来拼接。"+"号不会显示在名称中。  
  
自定义词库:  
把你要的词库命名，文件名为词库名。  
文件编码为utf-8，一行一个词。程序将从词库中随机选一个词。    
在 <程序目录>/name_strus.json 中即可使用词库。  
### 高级提示  
Python版本特有，在线版本待实现  
按下F3可以在程序底部开启一个提示框，显示生成名称的详细信息:  
(当生成名称时)
格式: name_stru.json 中名称格式的键  
分词: 这个名称是由哪些词组成的  
(当检测到违规时)
显示哪些地方违规了，违规原因。  
### 历史记录
Python版本特有，在<程序目录>/historys/n.wffz可读取历史文件。  
在程序关闭时会在 <程序目录>/historys/ 下生成一个后缀为.wffz的文件，记录了本次运行生成的所有随机名称。  
在程序运行时，按下F4会在新窗口显示本次的历史，按下Ctrl+F4会在stdout输出历史记录。  
### 敏感词检测
Python版本特有，在输入框中按回车(Return)或按下"对勾"按钮会检测名称可用性。违规会弹窗。  
  
使用了从微信中提取的"fts"(字到音)文件进行混淆检测。  
  
先会将名称**正序**进行一次混淆和准确检测。  
混淆检测会把名称转为拼音然后检测以防止同音字。  
准确检测会检测原始名称中是否有一个特定的字以防止同音不同意的违规词。  
然后会将名称**倒序**进行一次混淆检测和准确检测。  
检测过程与正序的时候无差别，只是为了防止将违禁词倒过来写。  

# 版权
©️ wangyupu 
基于GPL v3.0协议进行开源。
