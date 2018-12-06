import requests, bs4 , smtplib , time ,re
from email.mime.text import MIMEText

def emailsend(stockname,stock,emailuser):
    mailmsg = """
    <p>股票{}的股票成交價已到{}，請趕快下單</p>
    """.format(stockname,stock)
    msg = MIMEText(mailmsg,"html","utf-8")      #文字
    msg['Subject'] = '股票{}通知'.format(stockname)     #標題
    msg['From'] = emailuser
    msg['To'] = emailuser
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(emailuser, userpd)
    server.send_message(msg)
    server.quit()
    print('Email成功傳出')

def stockcheck(stocknum):
    url = "https://tw.finance.yahoo.com/q/ts?s={}".format(stocknum)
    html = requests.get(url)
    if html.status_code != 200:
        print('網址無效:', html.url)
        return "no"
    soup = bs4.BeautifulSoup(html.text, 'html.parser')
    stocks = soup.find_all("",["high","low"])
    if(len(stocks)==0):
        print("並無此代碼({})，請重新輸入".format(stocknum))
        return "no"
    global stockname
    name = soup.find_all("b")
    stockname = name[1].text
    target=0
    for stock in stocks:
        if(target==2):
            return stock.text
        target+=1
            
def emailcheck(mailuser):
    if mailuser == "":return 1
    if re.search(r'[a-zA-Z0-9_.+-]+@gmail+\.[a-zA-Z0-9-.]+',mailuser)==None:return 2
    global userpd
    userpd = input("請輸入Email密碼:")
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(mailuser,userpd)
    except:return 3
    else:return 4
    #1 space 2 not gmail or not email 3 email has something worng
    
def timecheck():
    settime=input("設定從現在到幾點ex(輸入09.06.01 or 12.16.21)24H制\n請輸入時間(按Enter上一步):")
    if settime=="":return 1
    if re.search(r"\d{2}.\d{2}.\d{2}",settime)!=None:
        (hour,mins,sec)=settime.split(".")
        try:
            if 24 > int(hour) >= 0 and 60 > int(mins) >= 0 and 60 > int(sec) >= 0:
                if 14 > int(hour) > 8:return settime
                return 5
            else:return 3
        except:return 4
    else:return 2
    #1 空白 2 時間格式錯誤 3 時間數值錯誤 4 數字 5 9-13 6 ok
    
def stockgo():
    datalist=[]
    while(True):
#email check-----------------------------------------------------------
        emailuser = input("請輸入Email帳號(只支援Gmail，按Enter結束程序):")
        emailnum = emailcheck(emailuser)
        if emailnum == 1:break
        elif emailnum == 2:
            print("email格式錯誤或使用非Gmail的帳號")
            continue
        elif emailnum == 3:
            print("email發生不明錯誤")
            continue
#stock count----------------------------------------------------------------------
        while(True):
            count=input("輸入你需要幾支股票(按Enter上一步):")
            if count == "":break
            try:
                if 1 > int(count) or int(count) > 50:
                    print("請輸入1-50的數字")
                    continue
            except:
                print("請輸入數字")
                continue
            i=0
            while(True):
                if int(count) == i:break
                i+=1
                everydict={}
#check stock-------------------------------------------------------
                stocknum=input("輸入股票代碼如(輸入1477)對應聚陽(按Enter換下一個股票)\n請輸入代號:")
                if stocknum == "":
                    yorn=input("你確定要換下一個股票(Y/N):")
                    if yorn == "y":
                        continue
                    elif yorn == "n":
                        i-=1
                        continue
                    else:
                        print("因為你輸入不是Y跟N的字元所以直接換下一個")
                        continue
                if stockcheck(stocknum) == "no":#代碼不存在
                    i-=1
                    continue
#hope stock--------------------------------------------------------
                while(True):
                    print("股票:{}".format(stockname))
                    stockhigh=input("請輸入期望值(按Enter上一步):")
                    if stockhigh=="":
                        i-=1
                        break
                    try:
                        if int(stockhigh) < 0 :
                            print("期望值不能小於0")
                            continue
                    except:
                        print("只能是數字")
                        continue
#time check---------------------------------------------------------
                    while(True):
                        settime=timecheck()
                        if settime == 1 :break
                        elif settime == 2 :
                            print("時間[格式]錯誤")
                            continue
                        elif settime == 3:
                            print("時間[數值]錯誤")
                            continue
                        elif settime == 4:
                            print("請輸入[數字]")
                            continue
                        elif settime == 5:
                            print("請輸入9-13之間的時間")
                            continue
#run-------------------------------------------------------------
                        everydict["num"]=stocknum
                        everydict["hstock"]=stockhigh
                        everydict["time"]=settime
                        datalist.append(everydict)
                        break
                    break
            break
#check-------------------------------------------------------------
        print(datalist)
        print("Gmail:{}\nPassword:{}".format(emailuser,userpd))
        chose = input("輸入確認是否正確(y/n):")
        if chose == "y":print("開始運算中.....")
        elif chose == "n":
            print("如果有錯，請重新打！")
            continue
        else:
            print("誰叫你不輸入Y或N兩個字元，請重新打")
            continue
#action------------------------------------------------------------
        while(True):
            i=0
            for data in datalist:
                stocklow = stockcheck(data["num"])
                stockhigh = data["hstock"]
                nowtime = time.strftime("%H.%M.%S")
                if nowtime == data["time"]:
                    print("股票{}的時間({})已經到了，並沒有到期望值{}".format(stockname,data["time"],data["hstock"]))
                    datalist.pop(i)
                    i-=1
                if float(stockhigh) < float(stocklow):#high期望值low當時值
                    emailsend(stockname,stocklow,emailuser)
                    print("股票{}已經到期望值{}，到的時間為{}".format(stockname,data["hstock"],nowtime))
                    datalist.pop(i)
                    i-=1
                i+=1
            time.sleep(1)#frush
            print(nowtime)
            if len(datalist) == 0:
                print("股票全數完畢")
                break
        break
