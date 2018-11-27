import requests, bs4 , smtplib , time ,re
from email.mime.text import MIMEText

def email(stockname,stock):
    mailmsg = """
    <p>股票{}的股票成交價為{}</p>
    """.format(stockname,stock)
    msg = MIMEText(mailmsg,"html","utf-8")      #文字
    msg['Subject'] = '股票'     #標題
    msg['From'] = "ncutemail123@gmail.com"
    msg['To'] = 'ncutemail123@gmail.com'
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login("ncutemail123@gmail.com", "Email123")
    server.send_message(msg)
    server.quit()
    print('Email成功傳出')

def stockallcheck(num):
    url = "https://tw.finance.yahoo.com/q/ts?s={}".format(stocknum)
    html = requests.get(url)
    if html.status_code != 200:
        print('網址無效:', html.url)
        quit()
    soup = bs4.BeautifulSoup(html.text, 'html.parser')
    stocks = soup.find_all("",["high","low"])
    if(len(stocks)==0):
        print("並無此代碼({})".format(stocknum))
    #-----------------4
    if(num=="4"):
        url = "https://tw.finance.yahoo.com/q/ts?s={}&t=50".format(stocknum)
        html = requests.get(url)
        if html.status_code != 200:
            print('網址無效:', html.url)
            quit()
        soup = bs4.BeautifulSoup(html.text, 'html.parser')
        tablelist=soup.find_all("table")
        targettablelist=tablelist[7].find_all("td")
        chinese=1
        sort=0
        for line in targettablelist:
            if(sort==5):
                if(chinese==1):
                    print("{:<6s}".format(line.text.replace(' ', '')),end="\n")
                    chinese=0
                else:
                    print("{:<8s}".format(line.text.replace(' ', '')),end="\n")
                sort=0
                continue
            if(chinese==1):print("{:<6s}".format(line.text.replace(' ', '')),end="  ")
            else:print("{:<8s}".format(line.text.replace(' ', '')),end="  ")
            sort+=1
    #------------3
    if(num=="3"):
        tablelist=soup.find_all("table")
        targettablelist=tablelist[7].find_all("td")
        chinese=1
        sort=0
        for line in targettablelist:
            if(sort==5):
                if(chinese==1):
                    print("{:<6s}".format(line.text.replace(' ', '')),end="\n")
                    chinese=0
                else:
                    print("{:<8s}".format(line.text.replace(' ', '')),end="\n")
                sort=0
                continue
            if(chinese==1):print("{:<6s}".format(line.text.replace(' ', '')),end="  ")
            else:print("{:<8s}".format(line.text.replace(' ', '')),end="  ")
            sort+=1
    #------------------
    global stockname
    stockname = soup.find("b").text
    target=0
    for stock in stocks:
        if(target==2):
            if(num=="1"):print("{}的股票成交價為{}".format(stockname,stock.text))
            if(num=="2"):email(stockname,stock.text)
            if(num=="5"):return stock.text
        target+=1

def stockgo():
    while(True):
        stocknum=input("輸入股票代碼如(輸入1477)對應聚陽(按Enter已結束程序)\n請輸入代號:")
        if(stocknum==""):break
        stockhigh=input("請輸入期望值:")
        settime=input("設定從{}到幾點\nex(輸入09.06.01)24制:".format(time.strftime("%H:%M:%S")))
        else:
            while(True):
                num = input("請輸入Email帳號(只支援Gmail，按Enter已結束):")
                if(num==""):
                    break
                    stocklow=stockallcheck(num)
                if(stockhigh<stocklow):
                    email(stockname,stocklow)
                    stockallcheck(num)

#print('-'*26+"\n"+soup.title.text+"\n"+'-'*26)
#tablelist=soup.find_all("table")
#targettablelist=tablelist[7].find_all("td")
#time=[]
#stockdata=[]
#target=0
#for line in targettablelist:
#    found=line.text
#    if(target>5):
#        if(re.match(r"\d\d:\d\d:\d\d",found)!=None):
#            time.append(found)
#            continue
#        stockdata.append(found)
#        continue
#    target+=1
#print(time)
#print()
#print(stockdata)