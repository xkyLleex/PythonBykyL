import tkinter as tk
import tkinter.messagebox as msg
import requests, bs4 , smtplib , time , re , os , sqlite3
import matplotlib.pyplot as plt
import pandas_datareader.data as web
import datetime
from selenium import webdriver
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def stockcheck(stocknum):
    try:
        url = "https://tw.finance.yahoo.com/q/ts?s={}".format(stocknum)
        html = requests.get(url)
        if html.status_code != 200:
            msg.showerror('網址無效:', html.url)
            return "no"
        soup = bs4.BeautifulSoup(html.text, 'html.parser')
        stocks = soup.find_all("",["high","low"])
        if(len(stocks)==0):
            msg.showwarning("股票","並無此代碼({})\n請重新輸入".format(stocknum))
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
        msg.showerror("股票","發生錯誤:{}".format(e))
        return "no"

def startstock():
    def analysis(stocknum):
        end=datetime.date.today()
        passyear=datetime.timedelta(days=365*3)
        start=end-passyear
        company=["{}.TW".format(stocknum)]
        try:
            stockfind=web.DataReader(company,"yahoo",start,end)
        except:
            msg.showerror("股票","發生錯誤\n你輸入的號碼可能不是*上市公司*")
            return
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
            msg.showerror("股票","發生錯誤\n{}".format(e))
            return
        
    def emailsend(stockname,stock,email,pwd):
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
        emsg = MIMEMultipart("")      #文字
        emsg['Subject'] = '股票{}通知'.format(stockname)     #標題
        emsg['From'] = email
        emsg['To'] = email
        emsg.attach(MIMEText(mailmsg, "html", "utf-8"))
        aimage = open("{}({}).png".format(datetime.date.today(),stockname), "rb")
        msgImage = MIMEImage(aimage.read())
        aimage.close()
        msgImage.add_header("Content-ID", "<analysis>")
        emsg.attach(msgImage)
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(email, pwd)
        server.send_message(emsg)
        server.quit()
        print("{}\nEmail成功傳出".format(stockname))
    
    datalist=[]
    def startgo(email,pwd):
        i=0
        for data in datalist:
            time.sleep(1)#frush
            stocklow = stockcheck(data["num"])
            if stocklow == "no":continue
            stockhigh = data["hstock"]
            Hour = int(time.strftime("%H"))
            if float(stockhigh) < float(stocklow):#high期望值low當時值
                analysis(data["num"])
                emailsend(stockname,stocklow,email,pwd)
                msg.showinfo("股票資訊","股票{}已經到期望值{}\n到的時間為{}"
                      .format(stockname,data["hstock"],time.strftime("%H:%M:%S")))
                os.remove("{}({}).png".format(datetime.date.today(),stockname))
                datalist.pop(i)
                i-=1
                continue
            if Hour > 13:
                msg.showinfo("股票資訊","股票{}的時間已經超過13點\n並沒有到期望值{}"
                      .format(stockname,data["hstock"]))
                datalist.pop(i)
                i-=1
            i+=1
        if len(datalist) == 0:
            msg.showinfo("股票","在{}的時候\n股票全數完畢".format(time.strftime("%Y/%m/%d(%H.%M.%S)")))
            return
        startmain.after(1000, startgo())
    
    def checkall():
        error = True
        email = emailuser.get()
        pwd = emailpwd.get()
        if re.search(r'[a-zA-Z0-9_.+-]+@gmail+\.[a-zA-Z0-9-.]+',email)==None:
            msg.showwarning("EMAIL錯誤", "Email格式錯誤")
            warnemail.configure(text="Email格式錯誤")
            error = False
        if pwd == "":
            msg.showwarning("PASSWORD錯誤","密碼不能空白")
            warnpwd.configure(text="密碼不能空白")
            error = False
        else:
            try:
                server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                server.ehlo()
                server.login(email,pwd)
            except:
                msg.showerror("SMTPError","Email發生不明錯誤\n請確認帳密是否正確！")
                return
        if error == True:
            warnemail.configure(text="")
            warnpwd.configure(text="")
            yorn = msg.askquestion("infocheck","請確認帳密是否正確\nEmail:{}\nPassword:{}"
                                   .format(email,pwd[0]+"*"*(len(pwd)-1)))
            if yorn == "yes":
                if readdata() != 1:startgo(email,pwd)
            else:return
    rundata = False
    def readdata():
        errormsg.configure(text="讀取資料庫中...")
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
            conn.commit()
            sql = "select * from stockdata;"
            recs = conn.execute(sql)
            i=0
            for rec in recs:
                if rec[0] == time.strftime("%Y-%m-%d"):
                    if rundata == True:
                        everydict={}
                        everydict["num"]=rec[1]
                        everydict["hstock"]=rec[2]
                        datalist.append(everydict)
                        conn.execute("delete from stockdata where date='{}' and stock={};"
                                     .format(rec[0],rec[1]))
                        conn.commit()
                    i+=1
        except sqlite3.Error as e:
            msg.showerror("DataBase","資料庫錯誤\n{}".format(e))
            return 1
        except Exception as e:
            msg.showerror("DataBase","發生錯誤\n{}".format(e))
            return 1
        finally:
            if "conn" in dir():conn.close()
        if i == 0:
            msg.showinfo("股票","今日並無預定股票")
            errormsg.configure(text="今日無預定股票")
            return 1
        else:
            errormsg.configure(text="讀取完成")
        
    startmain = tk.Toplevel(main)
    startmain.title("開始股票功能")
    startmain.geometry("330x200")
    #Email
    emailuser = tk.StringVar()
    tk.Label(startmain,text="UserEmail:").place(x=0,y=10)
    tk.Label(startmain,text="注意:Email只能用在Gmail上(建議先測試)",fg="red").place(x=0,y=30)
    warnemail = tk.Label(startmain,text="",fg="red")
    warnemail.place(x=230,y=30)
    tk.Entry(startmain,textvariable=emailuser,width=30).place(x=65,y=10)
    #Password
    emailpwd = tk.StringVar()
    tk.Label(startmain,text="Password:").place(x=0,y=50)
    warnpwd = tk.Label(startmain,text="",fg="red")
    warnpwd.place(x=230,y=70)
    tk.Entry(startmain,textvariable=emailpwd,show="*",width=30).place(x=65,y=50)
    #sure
    startyes = tk.Button(startmain,text="確認",width=20,height=3,command=checkall)
    startyes.place(x=10,y=90)
    
    errormsg = tk.Label(startmain,text="",fg="red")
    errormsg.place(x=0,y=150)
    
    readdata()
    rundata = True
    
def bookstock():
    def datecheck(settime):
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
                        if int(time.strftime("%H")) > 13:return 6
                return settime
            except:return 4
        else:return 2
    #2 時間格式錯誤 3 時間數值錯誤 4 數字 5 未來notnow 6 今天股票時間已結束
    def bookstart():
        error = True
        stock = stocknum.get()
        hstock = hope_stock.get()
        bdate = date.get()
        #stock
        if stock == "" or stockcheck(stock) == "no":
            warnstocknum.configure(text="股票代碼錯誤")
            error = False
        #hope stock
        if hstock == "":
            warnhstock.configure(text="請輸入期望值")
            error = False
        else:
            try:
                if float(hstock) < 0:
                    warnhstock.configure(text="期望值不能為負數")
                    error = False
            except:
                warnhstock.configure(text="期望值要是數字")
                error = False
        #date
        if bdate == "":
            warndate.configure(text="日期不能空白")
            error = False
        elif datecheck(bdate) == 2:
            warndate.configure(text="日期格式錯誤")
            error = False
        elif datecheck(bdate) == 3:
            warndate.configure(text="日期數值錯誤")
            error = False
        elif datecheck(bdate) == 5:
            warndate.configure(text="只能輸入今天以後的日期")
            error = False
        elif datecheck(bdate) == 6:
            warndate.configure(text="今天股票時間已結束")
            error = False
        if error == True:
            warnstocknum.configure(text="")
            warnhstock.configure(text="")
            warndate.configure(text="")
            yorn = msg.askquestion("infocheck","請確認是否正確\n股票代碼:{}\n期望值:{}\n日期:{}"
                                   .format(stockname,hstock,bdate))
            if yorn == "yes":
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
                    sql = "select count(*) from stockdata where date='{}' and stock={};".format(bdate,int(stock))
                    data = conn.execute(sql)
                    match = data.fetchone()
                    if match[0] == 0:
                        conn.execute('''
                            insert into stockdata(date, stock, hstock) values ('{}',{},{});
                            '''.format(bdate,int(stock),float(hstock)))
                        conn.commit()
                        msg.showinfo("資料庫","寫入完成")
                    else:msg.showwarning("資料庫","\n資料庫已有這筆資料了({}股票代碼:{})，請更換或把它刪除！".format(bdate,stock))
                except sqlite3.Error as e:msg.showerror("資料庫","資料庫錯誤\n{}".format(e))
                except Exception as e:msg.showerror("資料庫","錯誤\n{}".fomrat(e))
                finally:
                    if "conn" in dir():conn.close()         
    bookmain = tk.Toplevel(main)
    bookmain.title("預定股票")
    bookmain.geometry("240x220")
    #stocknum
    stocknum = tk.StringVar()
    tk.Label(bookmain,text="股票代碼:").place(x=0,y=10)
    tk.Label(bookmain,text="注意:只有上市公司可以用",fg="red").place(x=0,y=30)
    warnstocknum = tk.Label(bookmain,text="",fg="red")
    warnstocknum.place(x=150,y=30)
    tk.Entry(bookmain,textvariable=stocknum,width=20).place(x=65,y=10)
    #hopstock
    hope_stock = tk.StringVar()
    tk.Label(bookmain,text="  期望值:").place(x=0,y=50)
    warnhstock = tk.Label(bookmain,text="",fg="red")
    warnhstock.place(x=150,y=70)
    tk.Entry(bookmain,textvariable=hope_stock,width=20).place(x=65,y=50)
    #date
    date = tk.StringVar()
    tk.Label(bookmain,text="預定日期:").place(x=0,y=90)
    tk.Label(bookmain,text="*注意*\n只能輸入未來日期(格式為2018-12-29)",fg="red").place(x=0,y=130)
    warndate = tk.Label(bookmain,text="",fg="red")
    warndate.place(x=120,y=110)
    tk.Entry(bookmain,textvariable=date,width=20).place(x=65,y=90)
    #sure
    bookyes = tk.Button(bookmain,text="確認",width=20,height=3,command=bookstart)
    bookyes.place(x=10,y=170)

def search_delete():
    def updata():
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
            conn.commit()
            sql = "select * from stockdata;"
            data = conn.execute(sql)
            i=0
            for line in data:
                if i == 0:
                    listsd.insert("end","日期              股票代碼 期望值")
                listsd.insert("end","{} | {:>4} | {:>7}".format(line[0],line[1],line[2]))
                i+=1
            if i==0:listsd.insert("end","資料庫無資料")
        except sqlite3.Error as e:
            msg.showerror("DataBase","\n資料庫錯誤:{}".format(e))
        except Exception as e:
            msg.showerror("DataBase","\n發生錯誤:{}\n".format(e))
        finally:
            if "conn" in dir():conn.close()            
            listsd.pack()
            
    def deletestock():
        value = listsd.curselection()
        allvalue = listsd.get(0,"end")
        try:
            conn = sqlite3.connect('bookstock.db')
            dataline = str(allvalue[value[0]])
            (date,stock,hstock)=dataline.split(" | ")
            conn.execute('''
                delete from stockdata where date='{}' and stock={};
                '''.format(date.replace(" ",""),int(stock)))
            conn.commit()
            msg.showinfo("DataBase","刪除成功")
            listsd.delete(0,"end")
            updata()
        except sqlite3.Error as e:
            msg.showerror("DataBase","\n資料庫錯誤:{}".format(e))
        except:
            msg.showerror("chose","選擇一個值")
        finally:
            if "conn" in dir():conn.close()
            return
    sdmain = tk.Toplevel(main)
    sdmain.title("查詢/刪除股票")
    sdmain.geometry("400x250")
    listsd = tk.Listbox(sdmain,width=50)
    updata()
    delete = tk.Button(sdmain,text="刪除",width=20,height=3,command=deletestock)
    delete.pack()
    
def emailtest():        
    def fixerror():
        def fixthis():
            value = listfix.curselection()
            try:
                if value[0] == 0:
                    lablefix.configure(text="帳號錯誤請自行檢討及查詢")
                elif value[0] == 1:
                    lablefix.configure(text="請將「安全性較低的應用程式存取權限」設為「啟用」")
                elif value[0] == 2:
                    lablefix.configure(text="進入此網頁\nhttps://accounts.google.com/b/0/DisplayUnlockCaptcha\n點擊「繼續」")
                elif value[0] == 3:
                    lablefix.configure(text='''
                1.進入此網頁\nhttps://accounts.google.com/b/0/SmsAuthConfig?hl=zh_TW\n進行啟用兩步驟驗證\n
                2.進入此網頁\nhttps://security.google.com/settings/security/apppasswords?pli=1\n產生一組應用程式專用密碼\n
                然後把「寄件程式」內的Google密碼換成這組應用程式密碼，\n注意此專用密碼只能登入一個地方
                                   ''')
                elif value[0] == 4:
                    lablefix.configure(text="不明錯誤=>去詢問作者ㄅ")
            except:
                lablefix.configure(text="請選擇")
            fixmain.after(250,fixthis)
            
        fixmain = tk.Toplevel(testmain)
        fixmain.title("FixError")
        fixmain.geometry("500x500")
        listfix = tk.Listbox(fixmain,width=50)
        fixmean = ["Email帳密錯誤","沒允許低安全性應用程式存取您的帳戶","有設定人機驗證鎖定",
                   "有啟用兩步驟驗證跟設定應用程式專用密碼","不明錯誤"]
        for line in fixmean:
            listfix.insert("end",line)
        listfix.pack()
        lablefix = tk.Label(fixmain,text="",width=80,height=30)
        lablefix.pack()
        fixthis()
    def emailgo(mailuser,mailpassword):
        mailmsg = """
        <p>此為測試郵件</p>
        """
        #html or plain(純文字)
        emsg = MIMEText(mailmsg,"html","utf-8")
        emsg["Subject"] = "測試郵件"
        emsg["From"] = mailuser
        emsg["To"] = mailuser

        try:
            server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            server.ehlo()
        except smtplib.SMTPException:
            msg.showerror("Email","SMTP伺服器錯誤")
        else:
            try:
                server.login(mailuser, mailpassword)
                server.send_message(emsg)
            except smtplib.SMTPException as e:msg.showerror("Email","帳號出現錯誤!!!\n請去參考錯誤解決提示\n{}".format(e))
            except Exception as e:msg.showerror("Email","不明錯誤!!!\n請去參考錯誤解決提示\n{}".format(e))
            else:msg.showinfo("Email",'Email成功傳出')
        finally:server.quit()
    
    def emailcheck():
        error = True
        email = emailuser.get()
        pwd = emailpwd.get()
        if re.search(r'[a-zA-Z0-9_.+-]+@gmail+\.[a-zA-Z0-9-.]+',email)==None:
            msg.showwarning("EMAIL錯誤", "Email格式錯誤")
            warnemail.configure(text="Email格式錯誤")
            error = False
        if pwd == "":
            msg.showwarning("PASSWORD錯誤","密碼不能空白")
            warnpwd.configure(text="密碼不能空白")
            error = False
        else:
            try:
                server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                server.ehlo()
                server.login(email,pwd)
            except:
                msg.showerror("SMTPError","Email發生不明錯誤\n請確認帳密是否正確！")
                return
        if error == True:
            warnemail.configure(text="")
            warnpwd.configure(text="")
            emailgo(email,pwd)
            
    testmain = tk.Toplevel(main)
    testmain.title("Email測試")
    testmain.geometry("300x200")
    #Email
    emailuser = tk.StringVar()
    tk.Label(testmain,text="UserEmail:").place(x=0,y=10)
    tk.Label(testmain,text="注意:Email只能用在Gmail上",fg="red").place(x=0,y=30)
    warnemail = tk.Label(testmain,text="",fg="red")
    warnemail.place(x=170,y=30)
    tk.Entry(testmain,textvariable=emailuser,width=30).place(x=65,y=10)
    #Password
    emailpwd = tk.StringVar()
    tk.Label(testmain,text="Password:").place(x=0,y=50)
    warnpwd = tk.Label(testmain,text="",fg="red")
    warnpwd.place(x=170,y=70)
    tk.Entry(testmain,textvariable=emailpwd,show="*",width=30).place(x=65,y=50)
    #sure
    startyes = tk.Button(testmain,text="確認",width=20,height=3,command=emailcheck)
    startyes.place(x=10,y=90)
    #fixerror
    startyes = tk.Button(testmain,text="錯誤解決提示",width=20,height=3,command=fixerror)
    startyes.place(x=150,y=90)
    
    
main = tk.Tk()
main.title("Stock")

start = tk.Button(main,text="開始股票功能",width=20,height=3,command=startstock)
start.pack()

book = tk.Button(main,text="預定股票",width=20,height=3,command=bookstock)
book.pack()

search = tk.Button(main,text="查詢/刪除股票",width=20,height=3,command=search_delete)
search.pack()

test = tk.Button(main,text="Email測試",width=20,height=3,command=emailtest)
test.pack()

def update_clock():
    now = time.strftime("TIME:%Y/%m/%d %H:%M:%S")
    toptext.configure(text=now)
    main.after(1000, update_clock)
toptext = tk.Label(main,text="")
toptext.pack()
update_clock()

main.mainloop()
