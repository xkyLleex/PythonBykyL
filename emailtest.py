import smtplib , re 
from email.mime.text import MIMEText

def fixerror():
    while True:
        num = input("輸入代碼以選擇解決方式(按Enter已結束程式):")
        if num=="":break
        elif num=="1":print("帳號錯誤請自行檢討及查詢\n")
        elif num=="2":print("將「安全性較低的應用程式存取權限」設為「啟用」\n")
        elif num=="3":print("進入此網頁https://accounts.google.com/b/0/DisplayUnlockCaptcha點擊「繼續」\n")
        elif num=="4":
            print("1.進入此網頁https://accounts.google.com/b/0/SmsAuthConfig?hl=zh_TW進行啟用兩步驟驗證\n")
            print("2.進入此網頁https://security.google.com/settings/security/apppasswords?pli=1產生一組應用程式專用密碼\n")
            print("然後把「寄件程式」內的Google密碼換成這組應用程式密碼，注意此專用密碼只能登入一個地方\n")
        elif num=="5":print("去詢問作者ㄅ\n")

def emailgo(mailuser,mailpassword):
    mailmsg = """
    <p>此為測試郵件</p>
    """
    #html or plain(純文字)
    msg = MIMEText(mailmsg,"html","utf-8")
    msg["Subject"] = "測試郵件"
    msg["From"] = mailuser
    msg["To"] = mailuser

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.ehlo()
    except smtplib.SMTPException:
        print("SMTP伺服器錯誤")
    finally:
        try:
            server.login(mailuser, mailpassword)
            server.send_message(msg)
        except smtplib.SMTPException:
            print("\n帳號出現錯誤!!!\n可能錯誤地方:\n1.Email帳密錯誤\n",end="")
            print("2.沒允許低安全性應用程式存取您的帳戶\n3.有人機驗證鎖定\n4.沒啟用兩步驟驗證跟設定應用程式專用密碼\n5.不明錯誤")
            fixerror()
        else:
            server.quit()
            print('Email成功傳出')
def testgo():
    while True:
        mailuser = input("請輸入Email帳號(只支援Gmail，按Enter已結束):")
        if mailuser=="":break
        if re.search(r'[a-zA-Z0-9_.+-]+@gmail+\.[a-zA-Z0-9-.]+',mailuser)!=None:
            mailpassword = input("請輸入Email密碼:")
            emailgo(mailuser,mailpassword)
        print("email格式錯誤或使用非Gmail的帳號")