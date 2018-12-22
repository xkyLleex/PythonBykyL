import re , bs4 , time , requests

def writein(data):
    print("寫入資料中.....")
    try:
        file=open("BookStock.log", "a",encoding="UTF-8")
        file.write(data["date"] + "|")
        file.write(data["time"] + "|")
        file.write(data["stocknum"] + "|")
        file.write(data["hopestock"] + "\n")
        file.close()
        print("完成.....")
    except Exception as e:
        print("發生錯誤:{}".format(e))
        quit()
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
def timecheck(date):
    try:
        settime=input("\n設定從現在到幾點ex(輸入09.06.01 or 12.16.21)24H制\n請輸入時間(9-13)(按Enter上一步):")
    except Exception as e:
        print("發生錯誤:{}".format(e))
        quit()
    if settime=="":return 1
    if re.search(r"\d{2}\.\d{2}\.\d{2}",settime)!=None:
        (hour,mins,sec)=settime.split(".")
        try:
            if 24 > int(hour) >= 0 and 60 > int(mins) >= 0 and 60 > int(sec) >= 0:
                if 20 > int(hour) > 8:
                    if date != time.strftime("%Y-%m-%d"):return settime
                    if int(hour) < int(time.strftime("%H")):return 6
                    if int(hour) == int(time.strftime("%H")):
                        if int(mins) < int(time.strftime("%M")):return 6
                        elif int(mins) == int(time.strftime("%M")) and int(sec) <= int(time.strftime("%s")):
                            return 6
                    return settime
                else:return 5
            else:return 3
        except:return 4
    else:return 2
    #1 空白 2 時間格式錯誤 3 時間數值錯誤 4 數字 5 9-13 6 未來
def datecheck():
    try:
        settime=input("\n設定預定日期ex(輸入2018-02-17)\n請輸入日期(按Enter上一步):")
    except Exception as e:
        print("發生錯誤:{}".format(e))
        quit()
    if settime=="":return 1
    if re.search(r"\d{4}-\d{2}-\d{2}",settime)!=None:
        (stryear,strmonth,strday)=settime.split("-")
        try:
            year = int(stryear)
            month = int(strmonth)
            day = int(strday)
            if 13 < month or month < 0 :return 3
            if month != 2:
                if day <= 0:return 3
                if month < 8:
                    if month % 2 == 1:
                        if day > 31:return 3
                    else:
                        if day > 30:return 3  
                else:
                    if month % 2 == 1:
                        if day > 30:return 3
                    else:
                        if day > 31:return 3
            else:
                if year % 400 == 0 or (year % 100 != 0 and year % 4 == 0):
                    if day > 29:return 3
                else:
                    if day > 28:return 3
            if year < int(time.strftime("%Y")):return 5
            if year == int(time.strftime("%Y")):
                if month < int(time.strftime("%m")):return 5
                if month == int(time.strftime("%m")) and day < int(time.strftime("%d")):return 5
                if month == int(time.strftime("%m")) and day == int(time.strftime("%d")):
                    if int(time.strftime("%H")) > 13:return settime
            return settime
        except:return 4
    else:return 2
    #1 空白 2 時間格式錯誤 3 時間數值錯誤 4 數字 5 未來notnow 6 今天股票時間已結束
def bookstockgo():
    data = False
#check stock-------------------------------------------------------
    while(True):
        stockdata={}
        stocknum=input("\n輸入股票代碼如(輸入1477)對應聚陽[限定上市公司](按Enter返回目錄)\n請輸入代碼:")
        if stocknum == "":break
        if stockcheck(stocknum) == "no":#代碼不存在
            continue
        print("股票:{}".format(stockname))
#hope stock--------------------------------------------------------
        while(True):
            stockhigh=input("\n請輸入期望值(按Enter上一步):")
            if stockhigh=="":
                break
            try:
                if float(stockhigh) < 0 :
                    print("期望值不能小於0")
                    continue
            except:
                print("只能是數字")
                continue
#date check---------------------------------------------------------
            while(True):
                setdate=datecheck()
                if setdate == 1 :break
                elif setdate == 2 :
                    print("時間[格式]錯誤")
                    continue
                elif setdate == 3:
                    print("時間[數值]錯誤")
                    continue
                elif setdate == 4:
                    print("請輸入[數字]")
                    continue
                elif setdate == 5:
                    print("請輸入未來的日期")
                    continue
                elif setdate == 6:
                    print("今天股票時間已結束，請換一個日期")
                    continue
#time check---------------------------------------------------------
                while(True):
                    settime=timecheck(setdate)
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
                    elif settime == 6:
                        print("請輸入未來的時間")
                        continue
#run------------------------------------------------------------
                    stockdata["stocknum"]=stocknum
                    stockdata["hopestock"]=stockhigh
                    stockdata["date"]=setdate
                    stockdata["time"]=settime
                    data = True
                    break
                if data == True:
                    break
            if data == True:
                break
        if data == True:
            print('\n股票代碼:{}\n期望值:{}\n預定日期:{}\n預定截止時間:{}\n'.format(
            stockdata["stocknum"],stockdata["hopestock"],stockdata["date"],stockdata["time"],))
            yorn=input("確認資料是否正確(y/n):")
            data = False
            if yorn.lower() == "y":writein(stockdata)
            elif yorn.lower() == "n":
                print("如果有錯，請重新打！")
                continue
            else:
                print("誰叫你不輸入Y或N兩個字元，請重新打")
                continue    