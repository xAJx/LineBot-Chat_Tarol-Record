import pyimgur
# import random

CLIENT_ID = "2beea3a7ff2e552"
PATH = "C:\\Users\\jac13\\TarolCards\\Tar_gif_update\\"       # 路徑 要 兩個 反斜線，才能進下一層

# PATH = "C:\\Users\\jac13\\OneDrive\\桌面\\Line_Bot_AJ\\AJ_refer_to_Chapter_5\\TarolCards\\Tar_gif_update\\"

#PATH = "C:\\Users\\jac13\\TarolCards\\Tar_jpg\\"   
#PATH = "圖片"
title = "塔"        # "Uploaded with PyImgur"

# name = {"0_愚者正,":"愚者正","1_愚者逆,":"愚者逆","2_魔術師正,":"魔術師正","3_魔術師逆,":"魔術師逆","4_女皇正,":"女皇正"
#        ,"5_女皇逆,":"女皇逆","6_月亮正,":"月亮正","7_月亮逆,":"月亮逆","8_世界正,":"世界正","9_世界逆,":"世界逆"}

'''name = {"https://i.imgur.com/NR3Fgr7.gif":"愚者正","https://i.imgur.com/aTexDy4.gif":"愚者逆","https://i.imgur.com/ENOLwYy.gif":"魔術師正"
        ,"https://i.imgur.com/A11kZQA.gif":"魔術師逆","https://i.imgur.com/if2JtP0.gif":"女皇正","https://i.imgur.com/But8yCJ.gif":"女皇逆"
        ,"https://i.imgur.com/OQGYo6j.gif":"月亮正","https://i.imgur.com/Oev9VPV.gif":"月亮逆"
        ,"https://i.imgur.com/8oA4M7w.gif":"世界正","https://i.imgur.com/eQswllg.gif":"世界逆"}'''

# name = {"愚者正":"0","愚者逆":"1","魔術師正":"2","魔術師逆":"3","女皇正":"4","女皇逆":"5","月亮正":"6","月亮逆":"7"
#        ,"世界正":"8","世界逆":"9"}   # 這是 dictionary 的 大括號、內部 冒號，"key":"Value"，[本機圖片名稱也要設定對應相同的名字]

# name = {"愚者正":"0"}
# name = {"0":"愚者正"}    # 抓 [愚者正]圖片_在 imgur 的 專屬 url

name = {"0":"節制逆"}

# name = {"https://i.imgur.com/dqKYF4T.gif":"正義逆"}

'''name = {"0":"愚者正","1":"愚者逆","2":"魔術師正","3":"魔術師逆",
        "4":"女皇正","5":"女皇逆","6":"月亮正","7":"月亮逆",
        "8":"世界正","9":"世界逆","10":"倒吊正","11":"倒吊逆",
        "12":"力量正","13":"力量逆","14":"命輪正","15":"命輪逆",
        "16":"塔塔正","17":"塔塔逆","18":"太陽正","19":"太陽逆",
        "20":"女祭正","21":"女祭逆","22":"審判正","23":"審判逆",
        "24":"惡魔正","25":"惡魔逆","26":"戀人正","27":"戀人逆",
        "28":"戰車正","29":"戰車逆","30":"教皇正","31":"教皇逆",
        "32":"星星正","33":"星星逆","34":"正義正","35":"正義逆",
        "36":"死神正","37":"死神逆","38":"隱者正","39":"隱者逆",
        "40":"皇帝正","41":"皇帝逆","43":"節制正","44":"節制逆",
        }'''

turkey = list(name.keys())
turvalue = list(name.values())

a=list(name.items() )
#print(a[1][0])
# print(a[0][0])
im = pyimgur.Imgur(CLIENT_ID)
for n in name:  # for 迴圈 預設 都是 抓 前面的 key 值，例如 上面 第x行  name 裡面的 0、1、2
    #uploaded_image = im.upload_image(PATH+name[n] +".jpg", title=title)      # (檔案路徑PATH + 迴圈回傳的 每個圖片 名稱name[n] + 檔名.jpg)
    uploaded_image = im.upload_image(PATH+name[n] +".gif") 
    
    print()
    print(turvalue, uploaded_image.link, sep='   ~  ')   # seq 增加 空格
    #print(turvalue,uploaded_image.link)
    #print(name['2'],     uploaded_image.link)
    # print(turkey[1])
    #print(name['0'])
    #print(uploaded_image.link)
    
    # print(a[0][0], name.items() )
    
    # print(uploaded_image.link)   # 這只能知道 現在上傳的 這張圖片的 (雲端暫存網址、並非直接 存在 imgur 的 資料庫裡)
    # print(uploaded_image.type)   # 這三行 [title、link、type]  如果 在最外圍 迴圈外，則只會 秀出 迴圈 最後一張圖 結果
print()  # 秀全部圖片的網址


