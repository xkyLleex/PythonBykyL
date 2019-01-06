import smtplib , re , msvcrt
from email.mime.text import MIMEText

def fixerror():
    while True:
        num = input("請輸入上述代碼，選擇欲解決的問題(直接按Enter,可重新輸入帳密):")
        if num=="":break
        elif num=="1":print("\n請自行檢視並重新輸入\n")
        elif num=="2":print("\n請將「安全性較低的應用程式存取權限」設為「啟用」\n")
        elif num=="3":print("\n進入此網頁https://accounts.google.com/b/0/DisplayUnlockCaptcha點擊「繼續」\n")
        elif num=="4":
            print("\n1.進入此網頁https://accounts.google.com/b/0/SmsAuthConfig?hl=zh_TW進行啟用兩步驟驗證\n")
            print("2.進入此網頁https://security.google.com/settings/security/apppasswords?pli=1產生一組應用程式專用密碼\n")
            print("3.把「寄件程式」內的Google密碼換成這組應用程式密碼(注意此專用密碼只能登入一個地方)\n")
        elif num=="5":print("\n抱歉，我也無解...\n")
        else:print("\n查無此代碼，請重新輸入！！\n")

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
    else:
        try:
            server.login(mailuser, mailpassword)
            server.send_message(msg)
        except smtplib.SMTPException:
            print("\n\n帳號出現錯誤!!!\n可能錯誤的原因如下:\n1.帳密錯誤\n",end="")
            print("2.尚未允許低安全性應用程式存取您的帳戶\n3.有人機驗證鎖定\n4.未啟用兩步驟驗證跟設定應用程式專用密碼\n5.不明錯誤")
            fixerror()
        else:print('Email成功傳出')
    finally:server.quit()

def pwdstar():    
    chars = []   
    while True:  
        try:  
            nchar = msvcrt.getch().decode()  
        except:
            return input("請輸入Email密碼:")
        if nchar in "\r\n": #如果是換行，則輸入結束
             break
        elif nchar == "\b": #如果是退格，則刪除密碼末尾一位並且刪除一個星號  
             if chars:
                 chars.pop()
                 msvcrt.putch(b"\b") #光標退一格  
                 msvcrt.putch(b" ")  #用空格覆蓋原來的星號
                 msvcrt.putch(b"\b") #光標回退一格來接受新的輸入                   
        else:  
            chars.append(nchar)
            msvcrt.putch(b"*") #顯示為星號
    return ("".join(chars))

def testgo():
    while True:
        mailuser = input("\n請輸入Email帳號(本程式只支援Gmail，不輸入請直接按Enter回到最初的功能選擇):")
        if mailuser=="":break
        if re.search(r'[a-zA-Z0-9_.+-]+@gmail+\.[a-zA-Z0-9-.]+',mailuser)!=None:
            print("(注意)您如果不是在cmd命令行下執行，密碼將無法隱藏！",end="",flush=True)
            mailpassword = pwdstar()
            emailgo(mailuser,mailpassword)
        else:print("email格式錯誤或使用非Gmail的帳號")