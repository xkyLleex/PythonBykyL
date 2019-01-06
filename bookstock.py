import re , bs4 , time , requests , sqlite3

def bookweek(year,month,day):
    count=0
    count+=(year-1)*365+(year-1)/4-(year-1)/100+(year-1)/400
    count=int(count)
    for i in range(month):
        if i==1:count+=31
        elif i==2:
            if (year%400==0) or ((year%100!=0) and (year%4==0))==True:count+=29
            else:count+=28
        elif i==3:count+=31
        elif i==4:count+=30
        elif i==5:count+=31
        elif i==6:count+=30
        elif i==7:count+=31
        elif i==8:count+=31
        elif i==9:count+=30
        elif i==10:count+=31
        elif i==11:count+=30
    count+=day
    count=count%7
    if count == 0:return 0      #日
    elif count == 1:return 1    #一
    elif count == 2:return 2    #二
    elif count == 3:return 3    #三
    elif count == 4:return 4    #四
    elif count == 5:return 5    #五
    elif count == 6:return 6    #六
        
def writein(data):
    print("\n寫入資料中.....")
    date=data["date"]
    stock=data["stocknum"]
    hstock=data["hopestock"]
    try:
        conn = sqlite3.connect('bookstock.db')
        conn.execute('''
        create table if not exists stockdata
            (
             date    text      not null,
             stock   integer   not null,
             hstock  REAL      not null
            );
        ''')
        sql = "select count(*) from stockdata where date='{}' and stock={};".format(date,stock)
        data = conn.execute(sql)
        match = data.fetchone()
        if match[0] == 0:
            conn.execute('''
            insert into stockdata(date, stock, hstock) values ('{}',{},{});
            '''.format(date,stock,hstock))
            conn.commit()
            print("\n設定成功！！\n如要執行程式請點1.")
        else:print("\n資料庫已經有這筆資料了({}股票代碼:{})，請重新輸入或將他刪除！".format(date,stock))
    except sqlite3.Error as e:print("\n資料庫錯誤:{}".format(e))
    except Exception as e:print("\n錯誤:{}".fomrat(e))
    finally:
        if "conn" in dir():conn.close()
        
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
            print("查無此代碼({})，請重新輸入".format(stocknum))
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
        
def datecheck():
    try:
        settime=input("\n設定預定日期ex(輸入2018-02-17)\n請輸入日期(按Enter回到上一步):")
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
            if 12 < month or month < 1 :return 3
            if day <= 0:return 3
            if month != 2:
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
                    if int(time.strftime("%H")) > 13 and int(time.strftime("%M")) > 30:return 6
            return settime
        except:return 4
    else:return 2
    #1 空白 2 時間格式錯誤 3 時間數值錯誤 4 數字 5 未來notnow 6 今天股票時間已結束
    
def bookstockgo():
    data = False
#check stock-------------------------------------------------------
    while(True):
        stockdata={}
        try:
            stocknum=input("\n輸入股票代碼如1477(注意，僅限上市公司)(按Enter回到最初的功能選擇)\n請輸入代碼:")
        except Exception as e:
            print("出現錯誤:{}".format(e))
            quit()
        if stocknum == "":break
        if stockcheck(stocknum) == "no":#代碼不存在
            continue
        print("股票:{}".format(stockname))
#hope stock--------------------------------------------------------
        while(True):
            try:
                stockhigh=input("\n請輸入期望值(按Enter回到上一步):")
            except Exception as e:
                print("出現錯誤:{}".format(e))
                quit()
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
#run------------------------------------------------------------
                (stryear,strmonth,strday)=setdate.split("-")
                week=bookweek(int(stryear),int(strmonth),int(strday))
                stockdata["stocknum"]=int(stocknum)
                stockdata["hopestock"]=round(float(stockhigh),2)
                stockdata["date"]=setdate
                if  week == 0:stockdata["week"]="日"      #日
                elif week == 1:stockdata["week"]="一"    #一
                elif week == 2:stockdata["week"]="二"    #二
                elif week == 3:stockdata["week"]="三"    #三
                elif week == 4:stockdata["week"]="四"    #四
                elif week == 5:stockdata["week"]="五"    #五
                elif week == 6:stockdata["week"]="六"    #六
                data = True
                break
            if data == True:
                break
        if data == True:
            print("\n股票代碼:{}\n期望值:{}\n預定日期:{}(星期{})\n(注意:星期六、日及國定假日沒有股市)\n"
                 .format(stockdata["stocknum"],stockdata["hopestock"],stockdata["date"],stockdata["week"]))
            yorn=input("確認資料是否正確(y/n):")
            data = False
            if yorn.lower() == "y":writein(stockdata)
            elif yorn.lower() == "n":
                print("如果有錯，請重新設定！")
                continue
            else:
                print("誰叫你不輸入y或n，請重新設定吧！！")
                continue    