# _LineBot-Chat_Tarol-Record_
## _塔羅牌每日運勢、抽卡紀錄 (PostgreSQL_pgAdmin4)_

### 1. *須先自行 安裝 ngrok*
### 2. *每重新開一次 ngrok，Webhook URL 必須跟著設定最新的，請參考    https://developers.line.biz/console/

### 、https://developers.line.biz/console/channel/自己的channel-id/
### 3. *在使用這六個 linebot 按鈕時，ngrok 必須一直開著*

-----------------------------------------
### AJ-Tarol-LineBot _basic_ 條碼 _ID_:  
### @760qdhvn
------------------------------------------
#### I. code 裡面 line_bot_api = LineBotApi('自己的 Channel access token') # Line-GUI_Channel access token
<br>

#### II. code 裡面 handler = WebhookHandler('自己的 Channel secret') # Line-GUI_Channel secret
<br>

#### III. code 裡面 audiourl = 'https://自己最新的.ngrok.io/static/' # ngrok。 聲音
<br>

#### IV. code 裡面 videourl = 'https://自己最新的.ngrok.io/static/' # ngrok。 影像
<br>

### IV-2. code 裡面 *Tarot_landscape.mp4* 由於 GitHub 限制容量100mb，即使壓縮後 也無法上傳
<br>

### *首先在 _imgur_ 網站上* 存放44張圖片，並透過 _imgur_ 產生每張gif 的網址*
<br>

### *設計了 六個按鈕*: 分別是 1._傳送文字_ 2._每日運勢_ 3._抽五張卡_ 4._慎入_ 5._傳送位置_ 6._快速選單_*
<br>

