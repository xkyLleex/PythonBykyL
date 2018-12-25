import requests, bs4 , smtplib , time , re , os , msvcrt , sqlite3
import matplotlib.pyplot as plt
import pandas_datareader.data as web
import datetime
from selenium import webdriver
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def pwdstar():    
    chars = []  
    while True:  
        try:  
            nchar = msvcrt.getch().decode()  
        except:
            return input("(注意)你可能不是在cmd命令行下運行，密碼輸入將不能隱藏:")
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

def analysis(stocknum):
    end=datetime.date.today()
    passyear=datetime.timedelta(days=365*3)
    start=end-passyear
    company=["{}.TW".format(stocknum)]
    try:
        stockfind=web.DataReader(company,"yahoo",start,end)
    except:
        print("發生錯誤:你輸入的號碼可能不是*上市公司*")
        quit()
    stockfind["100d"]=round(stockfind["Adj Close"].rolling(window=100).mean(),2)
    stockfind.dropna(inplace=True)
    print(stockfind["Adj Close"].plot(color="black"))
    print(stockfind["100d"].plot(color="orange",legend="100d"))
    global datastock,infodata
    datastock=[]
    for line in round(stockfind.mean(),2):
        datastock.append(line)
    plt.savefig("{}({}).png".format(end,stockname))
    #------------infodata 0:kline data:1 2 3 4 5...
    infodata=[]
    try:
        driver = webdriver.Chrome()
        driver.get("https://tw.screener.finance.yahoo.net/screener/screen02.html?symid={}".format(stocknum))
        time.sleep(1)
        infodata.append(driver.find_element_by_id("Kline").text)
        for i in range(1,4):
            line=driver.find_element_by_xpath("//*[@id='DIQ_IO']/tbody/tr[{}]".format(i)).text
            linedata=line.split(" ")
            for info in linedata:
                infodata.append(info)
        driver.close()
    except Exception as e:
        print("發生錯誤:{}".format(e))
        quit()
    
def emailsend(stockname,stock,emailuser):
    mailmsg = """
    <pre>
    您追蹤的股票：<span style="color:#E60000;">{}</span>，目前已經來到<span style="color:#E60000;">{}</span>的價格囉，提醒您放下手邊工作儘速下單！
    ---------------------------------
    在您所關注的區間內，這支股票各項指標的平均值：
    High     {:>14}
    Low      {:>14}
    Open     {:>14}
    Close    {:>14}
    Volume   {:>14}
    Adj Close{:>14}
    ---------------------------------
    前一天的K值：<span style="color:#00FFFF;">{}</span>
    <span style="color:#DB0000;">(提醒：K值大於80時，為超買訊號，表示市場過熱；K值小於20時，為超賣訊號，表示市場過冷。)</span>
    ---------------------------------
    前三天三大法人的交易狀況：
     日期  外資  投信 自營商  合計
    {} {:>4}  {:>4} {:>4}   {:>4}
    {} {:>4}  {:>4} {:>4}   {:>4}
    {} {:>4}  {:>4} {:>4}   {:>4}
    ---------------------------------
    股價與20週均線的走勢圖與近半年的成交量:
    <span style="color:#DB0000;">(提醒：當股價向上突破20週均線，代表「空翻多」；當股價跌破20週均線，代表「多翻空」。)</span>
    <img src="cid:analysis">
    </pre>
    """.format(stockname,
    stock,datastock[0],datastock[1],datastock[2],datastock[3],datastock[4],datastock[5],
    infodata[0],
    infodata[1],infodata[2],infodata[3],infodata[4],infodata[5],
    infodata[6],infodata[7],infodata[8],infodata[9],infodata[10],
    infodata[11],infodata[12],infodata[13],infodata[14],infodata[15])
    msg = MIMEMultipart("")      #文字
    msg['Subject'] = '股票{}通知'.format(stockname)     #標題
    msg['From'] = emailuser
    msg['To'] = emailuser
    msg.attach(MIMEText(mailmsg, "html", "utf-8"))
    aimage = open("{}({}).png".format(datetime.date.today(),stockname), "rb")
    msgImage = MIMEImage(aimage.read())
    aimage.close()
    msgImage.add_header("Content-ID", "<analysis>")
    msg.attach(msgImage)
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(emailuser, userpwd)
    server.send_message(msg)
    server.quit()
    print('Email成功傳出')

def stockcheck(stocknum):
    try:
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
    except Exception as e:
        print("發生錯誤:{}".format(e))
        quit()
        
def emailcheck(mailuser):
    if mailuser == "":return 1
    if re.search(r'[a-zA-Z0-9_.+-]+@gmail+\.[a-zA-Z0-9-.]+',mailuser)==None:return 2
    global userpwd
    print("請輸入Email密碼:",end="",flush=True)
    userpwd = pwdstar()
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(mailuser,userpwd)
    except:return 3
    else:return 4
    #1 space 2 not gmail or not email 3 email has something worng
    
def startstockgo():
    emailstart=False
    datalist=[]
#email check-----------------------------------------------------------
    while(True):
        try:
            emailuser = input("\n請輸入Email帳號(只支援Gmail，按Enter結束程序):")
        except Exception as e:
            print("發生錯誤:{}".format(e))
            quit()
        emailnum = emailcheck(emailuser)
        if emailnum == 1:break
        elif emailnum == 2:
            print("email格式錯誤或使用非Gmail的帳號")
            continue
        elif emailnum == 3:
            print("\nemail發生不明錯誤")
            continue
#checkemail-------------------------------------------------------------
        pwdstarchar=[]
        for star in range(0,len(userpwd)):
            if star == 0:pwdstarchar.append(userpwd[0])
            else:pwdstarchar.append("*")
        print("\n\nGmail:{}\nPassword:{}".format(emailuser,"".join(pwdstarchar)))
        try:
            chose = input("輸入確認是否正確(y/n):")
        except Exception as e:
            print("發生錯誤:{}\n".format(e))
            quit()
        if chose.lower() == "y":
            emailstart = True
            break
        elif chose.lower() == "n":
            print("如果有錯，請重新打！")
            continue
        else:
            print("誰叫你不輸入Y或N兩個字元，請重新打")
            continue
#loadbookstock-----------------------------------------------------
    if emailstart == True:
        print("\n\n讀取預定股票檔案...")
        try:
            conn = sqlite3.connect('bookstock.db')
            sql = "select * from stockdata;"
            recs = conn.execute(sql)
            for rec in recs:
                if rec[0] == time.strftime("%Y-%m-%d"):
                    everydict={}
                    everydict["time"]=rec[1]
                    everydict["num"]=rec[2]
                    everydict["hstock"]=rec[3]
                    datalist.append(everydict)
                    conn.execute("delete from stockdata where stock={};".format(rec[2]))
                    conn.commit()
        except sqlite3.Error as e:
            print("\n資料庫錯誤:{}\n".format(e))
            return
        except Exception as e:
            print("\n發生錯誤:{}\n".format(e))
            return
        finally:
            if "conn" in dir():conn.close()
        if len(datalist) == 0:
            print("\n今日並無預定股票\n")
            return
#Start------------------------------------------------------------
        print("開始運算中.....")
        while(True):
            i=0
            for data in datalist:
                time.sleep(1)#frush
                stocklow = stockcheck(data["num"])
                stockhigh = data["hstock"]
                (dhour,dmin,dsec)=data["time"].split(".")
                Hour = int(time.strftime("%H"))
                Min = int(time.strftime("%M"))
                Sec = int(time.strftime("%S"))
                if Hour > int(dhour) or (Hour == int(dhour) and Min > int(dmin))\
                or (Hour == int(dhour) and Min == int(dmin) and Sec == int(dsec)):
                    print("\n股票{}的時間({})已經到了，並沒有到期望值{}"
                          .format(stockname,data["time"],data["hstock"]))
                    datalist.pop(i)
                    i-=1
                if float(stockhigh) < float(stocklow):#high期望值low當時值
                    analysis(data["num"])
                    print()
                    emailsend(stockname,stocklow,emailuser)
                    print("\n股票{}已經到期望值{}，到的時間為{}時{}分{}秒"
                          .format(stockname,data["hstock"],Hour,Min,Sec))
                    os.remove(r"{}/{}({}).png".format(os.path.dirname(__file__),datetime.date.today(),stockname))
                    datalist.pop(i)
                    i-=1
                i+=1
            if len(datalist) == 0:
                print("\n在{}".format(time.strftime("%Y/%m/%d(%H.%M.%S)")))
                print("股票全數完畢\n")
                break