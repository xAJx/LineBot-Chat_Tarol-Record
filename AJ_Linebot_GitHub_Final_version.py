from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://aj:123456@127.0.0.1:5432/linebotdb'   # 需設定成自己的
db = SQLAlchemy(app)

from flask import request, abort
from linebot import  LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage,TextSendMessage, ImageSendMessage, StickerSendMessage, LocationSendMessage, QuickReply, QuickReplyButton, MessageAction,AudioSendMessage, VideoSendMessage

import random, pyimgur, time

# 設定資料庫 的 資料模型
class LineBot_Tarol_Record(db.Model):
   __tablename__ = 'LineBot_Tarol_Record'               # 建立 pgAdmin 4  裡面的 [資料表名稱: LineBot_Tarol_Record]
   sid = db.Column(db.Integer, primary_key = True)      # 使用者 順序
   UserId = db.Column(db.String(50), nullable = False)  # 使用者 名字
   text = db.Column(db.String(5))                       # 第一按鈕 文字
   fortune = db.Column(db.String(20))                   # 第二按鈕 運勢
   fivecards = db.Column(db.String(100))                # 第三按鈕 五張卡
   cautious_entry = db.Column(db.String(5))             # 第四按鈕 使用者 慎入
   location = db.Column(db.String(5))                   # 第五按鈕 傳送位置
   quickmenu= db.Column(db.String(10))                  # 第六按鈕 快速選單
   localtime= db.Column(db.String(50))                  # 本地時間

   def __init__(self, UserId, text, fortune, fivecards, cautious_entry, location, quickmenu, localtime):
       self.UserId = UserId
       self.text = text
       self.fortune = fortune
       self.fivecards = fivecards
       self.cautious_entry = cautious_entry
       self.location = location
       self.quickmenu = quickmenu
       self.localtime = localtime  

CLIENT_ID = "2beea3a7ff2e552"   # 自己 pyimgur 的 ID

PATH = "C:\\Users\\jac13\\TarolCards\\Tar_gif_update\\"      # 自己存放圖片的本機網址， [請設自己本機端的路徑]，路徑 要 兩個 反斜線，才能進下一層
title = "塔"                                                 # "Uploaded with PyImgur"

# 44 張 imgur 的圖片網址 (dict)
name = {"https://i.imgur.com/NR3Fgr7.gif":"愚者正","https://i.imgur.com/aTexDy4.gif":"愚者逆","https://i.imgur.com/ENOLwYy.gif":"魔術師正"
        ,"https://i.imgur.com/A11kZQA.gif":"魔術師逆","https://i.imgur.com/if2JtP0.gif":"女皇正","https://i.imgur.com/But8yCJ.gif":"女皇逆"
        ,"https://i.imgur.com/OQGYo6j.gif":"月亮正","https://i.imgur.com/Oev9VPV.gif":"月亮逆","https://i.imgur.com/8oA4M7w.gif":"世界正"
        ,"https://i.imgur.com/eQswllg.gif":"世界逆","https://i.imgur.com/dtSderf.gif":"倒吊正","https://i.imgur.com/EDjdg99.gif":"倒吊逆"
        ,"https://i.imgur.com/DPvxv4a.gif":"力量正","https://i.imgur.com/ynoUku5.gif":"力量逆","https://i.imgur.com/lja59Dw.gif":"命輪正"
        ,"https://i.imgur.com/JX5XTGd.gif":"命輪逆","https://i.imgur.com/2S3o0MK.gif":"塔塔正","https://i.imgur.com/M7abryu.gif":"塔塔逆"
        ,"https://i.imgur.com/gDcHLKQ.gif":"太陽正","https://i.imgur.com/R5g7ge6.gif":"太陽逆","https://i.imgur.com/Da1bySM.gif":"女祭正"
        ,"https://i.imgur.com/i3vBeIh.gif":"女祭逆","https://i.imgur.com/Psfi02E.gif":"審判正","https://i.imgur.com/M3WWjsO.gif":"審判逆"
        ,"https://i.imgur.com/px7iVrr.gif":"惡魔正","https://i.imgur.com/afU85q4.gif":"惡魔逆","https://i.imgur.com/LZZg0DV.gif":"戀人正"
        ,"https://i.imgur.com/E4WSl7B.gif":"戀人逆","https://i.imgur.com/zwrmLUc.gif":"戰車正","https://i.imgur.com/tEbRrPG.gif":"戰車逆"
        ,"https://i.imgur.com/jPP2zAT.gif":"教皇正","https://i.imgur.com/VM0mbW3.gif":"教皇逆","https://i.imgur.com/RFciZgH.gif":"星星正"
        ,"https://i.imgur.com/XvrZU9f.gif":"星星逆","https://i.imgur.com/HyqoS07.gif":"正義正","https://i.imgur.com/5pFEUAR.gif":"正義逆"
        ,"https://i.imgur.com/ngNTGBn.gif":"死神正","https://i.imgur.com/C1Bk3ZO.gif":"死神逆","https://i.imgur.com/wyj1uEx.gif":"隱者正"
        ,"https://i.imgur.com/8q1KBc3.gif":"隱者逆","https://i.imgur.com/XktIMyB.gif":"皇帝正","https://i.imgur.com/5G1XrDw.gif":"皇帝逆"
        ,"https://i.imgur.com/vO7gA42.gif":"節制正","https://i.imgur.com/8JKyRuW.gif":"節制逆"
       }

im = pyimgur.Imgur(CLIENT_ID)

line_bot_api = LineBotApi('LBgKRFHh2Db+ko9NmKVSvraEd5IHMNsPwgTFqK5lJ6pk4/Y9o7Iq8XpMWwCqOrqh020jXnYEiIRS3/tPuXRNADaNd2h+D/f4IEQiwPQG2/dKjXFetb6wMkYWaNX4tATd7LZ5vCObvTRyVWfiCpzPVAdB04t89/1O/w1cDnyilFU=')
# Line-GUI_Channel access token

handler = WebhookHandler('97320de84ff995c000396baafb4984bd')   # Line-GUI_Channel secret 

audiourl = 'https://f195-1-200-253-95.ngrok.io/static/'  #每次開始伺服器，都要換 ngrok 網址, 音檔靜態檔案網址 路徑
#聲音url = '你的NGROK網址/static/'  #靜態檔案網址，[使用者 (按音檔) 出現 (保存期限已過)，就是這裡沒 更新到]

videourl = 'https://f195-1-200-253-95.ngrok.io/static/'  #每次開始伺服器，都要換 ngrok 網址, 音檔靜態檔案網址 路徑
#影音url = '你的NGROK網址/static/'  #靜態檔案網址,[使用者 (按音檔) 出現 (保存期限已過)，就是這裡沒 更新到]

@app.route("/Tarot", methods=['POST'])   # POST 比 GET 資料傳輸 來得安全
def Tarot():                         
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(444)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    db.create_all()                             # 資料庫 連線
    UserId = event.source.user_id               # 獲取使用者 id   
    profile = line_bot_api.get_profile(UserId)  # 獲取使用者 id 詳細訊息
    print(UserId)
    print(profile)
    print()
    t = time.localtime()             # 將秒數轉換為 struct_time 格式
    print(t)
    now = time.asctime(t)            # 將 struct_time 格式轉換為文字
    print(now)
    print()

    mtext = (event.message.text)
    #　UserId, text,fortune, fivecards, cautious_entry, location, quickmenu, localtime
    if mtext == '@傳送文字':
        datatext = LineBot_Tarol_Record(UserId, 1,'','','','','', now)         # 將使用者 id、第一按鈕 文字 一次，建立 ~ 資料庫
        db.session.add(datatext)
        db.session.commit()
        try:
            message = TextSendMessage(  
                text = "我是 Tarolbot，\n您好~ Serect Human !"
            )
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
            
    elif mtext == '@每日運勢':   # in event.message.text:  # 抽取 每日 (文字運勢、圖片卡牌)
        
        try:
            fortune = random.choice(['大凶', '凶', '末吉', '吉','中吉','大吉'])
            print(fortune)
            key_value_pair=list(name.items())
            random.shuffle(key_value_pair)                      # 洗牌
            print()
            print(key_value_pair)                               # 秀出 卡牌 清洗後的 (key:value)
            print()
            print(key_value_pair[0][0],  key_value_pair[0][1])  # 第一張 卡牌圖片 網址、卡牌名稱
            print()
            
            datafortune = LineBot_Tarol_Record(UserId, '','運勢: ' + fortune + '、卡牌: ' + key_value_pair[0][1] ,'','','','', now)         # 將使用者 id、第二按鈕 每日運勢 [中文運勢 + 卡牌文字] 一次，建立 ~ 資料庫
            db.session.add(datafortune)
            db.session.commit()
            print()

            message = [
                TextSendMessage(  #傳送文字
                    text = fortune
                ),
                ImageSendMessage (  #傳送圖片
                    original_content_url = (key_value_pair[0][0]),
                    preview_image_url = (key_value_pair[0][0]),
                )
            ]
            line_bot_api.reply_message(event.reply_token, message)                           #  line-bot 回傳給 使用者 訊息 [運勢文字 與 卡牌圖片]
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
         
    elif mtext == '@抽五張卡':              # 每次 洗完卡牌後，抽 前五張 不同 的卡牌
        try: 
            key_value_pair=list(name.items())
            random.shuffle(key_value_pair)
            print()
            print(key_value_pair)
            print()
            print(key_value_pair[0][0],  key_value_pair[0][1])        # 前面是 網址，後面 是卡牌名稱
            print(key_value_pair[1][0],  key_value_pair[1][1])
            print(key_value_pair[2][0],  key_value_pair[2][1])
            print(key_value_pair[3][0],  key_value_pair[3][1])
            print(key_value_pair[4][0],  key_value_pair[4][1])
            print()

            datafivecards = LineBot_Tarol_Record(UserId, '', '','1.' + key_value_pair[0][1] + '、2.' + key_value_pair[1][1] + '、3.' +  key_value_pair[2][1] + '、4.' + key_value_pair[3][1] + '、5.' + key_value_pair[4][1],'','','', now)         # 將使用者 id、第三按鈕 抽五張卡 (五張卡牌名稱)， 建立 ~ 資料庫
            db.session.add(datafivecards)
            db.session.commit()
            print()

            message = [ 
                ImageSendMessage(  #傳送圖片
                    original_content_url = (key_value_pair[0][0]),
                    preview_image_url = (key_value_pair[0][0]),
                ),  
                ImageSendMessage (  #傳送圖片 #串列   
                    original_content_url = (key_value_pair[1][0]),
                    preview_image_url = (key_value_pair[1][0])  
                ),
                ImageSendMessage(  #傳送圖片
                    original_content_url = (key_value_pair[2][0]),
                    preview_image_url = (key_value_pair[2][0])  
                ),
                ImageSendMessage(  #傳送圖片
                    original_content_url = (key_value_pair[3][0]),
                    preview_image_url = (key_value_pair[3][0])      
                ),
                ImageSendMessage(  #傳送圖片
                    original_content_url = ( key_value_pair[4][0] ),
                    preview_image_url = ( key_value_pair[4][0] )   
                )
            ]
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

    elif mtext == '@慎入':
        datacautious_entry = LineBot_Tarol_Record(UserId, '', '','', 1,'','', now)         # 將使用者 id、第四按鈕 慎入 一次， 建立 ~ 資料庫
        db.session.add(datacautious_entry)
        db.session.commit()
        print()
        try:
            message = [    # Linr-bot 限制 最多只能 五則 訊息
                TextSendMessage(  #傳送文字
                    text = "算牌累了，需要點能量 ~ 只好望梅止渴 ~ 提前吃明天 的 披薩！ "
                ),
                StickerSendMessage(  #傳送 line 貼圖
                    package_id = "6362",           # line 官方貼圖 需查表
                    sticker_id = "11087923"        # line 官方貼圖 https://developers.line.biz/en/docs/messaging-api/sticker-list/#sticker-definitions 
                ),
                ImageSendMessage(  #傳送圖片
                    original_content_url = "https://i.imgur.com/4QfKuz1.png",
                    preview_image_url = "https://i.imgur.com/4QfKuz1.png"    
                ), 
                VideoSendMessage(
                    original_content_url = videourl + 'Tarot_landscape.mp4',  # [音樂檔名 不能有中文 & 也不能有空格]， 聲音檔置於static資料夾 > 這首 4分12秒
                    preview_image_url = videourl + 'Tarot_landscape.mp4'
                ),
                AudioSendMessage(
                    original_content_url = audiourl + 'AJ_introduce_Tarol.mp3',  # [Goole小姐_AJ_腳本_塔羅介紹]， 聲音檔置於static資料夾 
                    duration=30000  #聲音長度最多顯示100秒，這設定30秒, 使用者圖示 x分30秒，實際上使用者可播完整首
                )
            ]     
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

    elif mtext == '@傳送位置':
        datalocation = LineBot_Tarol_Record(UserId, '', '','', '', 1,'', now)         # 將使用者 id、第五按鈕 傳送位置 一次， 建立 ~ 資料庫
        db.session.add(datalocation)
        db.session.commit()
        print()
        try:
            message = LocationSendMessage(
                title='Eden 塔羅占星催眠',
                address='106台北市大安區東豐街66號5樓',
                latitude=25.036096314041558,  #緯度
                longitude=121.54855949841298  #經度
            )
            line_bot_api.reply_message(event.reply_token, message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
            
    if mtext == '@快速選單':
        try:
            message = TextSendMessage (
                text='請選擇最喜歡的程式語言',
                quick_reply=QuickReply(       # 最多 13個選項
                    items=[
                        QuickReplyButton(
                            action=MessageAction(label="Python", text="Python")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="Java", text="Java")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="C#", text="C#")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="C", text="C")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="Android", text="Android")  # label 為 介面 文字，text為 linebot 回傳 給使用者的 文字 
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="Ios", text="Ios-系統")
                        )
                    ]
                ) 
            )
            dataquickmenu = LineBot_Tarol_Record(UserId, '', '','', '', '', 1, now)         # 將使用者 id、第六按鈕 快速選單 一次，  建立 ~ 資料庫
            db.session.add(dataquickmenu)
            db.session.commit()
            print()
            
            line_bot_api.reply_message(event.reply_token,message)
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

if __name__ == '__main__':
    app.run(port=80)
