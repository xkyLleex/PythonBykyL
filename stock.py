import requests, bs4 , smtplib , time , re , os
#save img
import matplotlib.pyplot as plt  
#stock data
import pandas_datareader.data as web 
import datetime
#---kline
from selenium import webdriver
#---email
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def analysis(stocknum):
    end=datetime.date.today()
    passyear=datetime.timedelta(days=365*3)
    start=end-passyear
    company=["{}.TW".format(stocknum)]
    stockfind=web.DataReader(company,"yahoo",start,end)
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
    if re.search(r"\d{2}\.\d{2}\.\d{2}",settime)!=None:
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
                stocknum=input("輸入股票代碼如(輸入1477)對應聚陽[限定上市公司](按Enter換下一個股票)\n請輸入代號:")
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
                time.sleep(1)#frush
                stocklow = stockcheck(data["num"])
                stockhigh = data["hstock"]
                nowtime = time.strftime("%H.%M.%S")
                if nowtime == data["time"]:
                    print("股票{}的時間({})已經到了，並沒有到期望值{}".format(stockname,data["time"],data["hstock"]))
                    datalist.pop(i)
                    i-=1
                if float(stockhigh) < float(stocklow):#high期望值low當時值
                    analysis(data["num"])
                    print()
                    emailsend(stockname,stocklow,emailuser)
                    print()
                    print("股票{}已經到期望值{}，到的時間為{}".format(stockname,data["hstock"],nowtime))
                    os.remove(r"{}/{}({}).png".format(os.path.dirname(__file__),datetime.date.today(),stockname))
                    datalist.pop(i)
                    i-=1
                i+=1
            print(nowtime)
            if len(datalist) == 0:
                print("股票全數完畢")
                break
        break
