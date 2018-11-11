import pprint,time,os
def lastlog():
    try:os.rename("log.txt",time.strftime("%m%d%H%M.log"))
    except IOError:print("檔案已存在("+time.strftime("%m%d%H%M")+".log)或是讀取檔案失敗")
    except:print("不明ERROR，請關閉程式來檢查ERROR的原因(3)")
def wlog(move,name):
    try:
        file=open("log.txt", "a",encoding="UTF-8")
        file.write(name+time.strftime(",%Y-%m-%d %H:%M:%S,")+move+"\n")
        file.close
    except IOError:print("讀取失敗")
    except:print("不明ERROR，請關閉程式來檢查ERROR的原因(8)")
def login(acc,pwd,datalist):
    i=0
    for data in datalist:
        if(data["acc"]==acc):
            if(data["pwd"]==pwd):
                wlog("登入",acc)
                return i
        i+=1
    return -1
def bmi(name):
    wlog("BMI計算",name)
    w=float(input("體重："))
    h=float(input("身高："))
    print("你的BMI指數為：%.2f\n"%(w/(h*h/10000))) if w>0 and h>0 else print("輸入數值錯誤\n")      
def bweight(name):
    wlog("最佳體重計算",name)
    h=float(input("身高："))
    print("你的最佳體重為：%.1f\n"%(22*h*h/10000)) if h>0 else print("輸入數值錯誤\n")
def log(name):
    wlog("觀看log",name)
    dataloglist=[]
    try:
        file=open("log.txt", "r",encoding="UTF-8")
        for line in file:
            line=line.strip('\n')
            datalogdict={}
            (name,times,act)=line.split(",")
            datalogdict["action"]=act
            datalogdict["datatime"]=times
            datalogdict["username"]=name
            dataloglist.append(datalogdict)
        file.close
        pprint.pprint(dataloglist)
    except IOError:print("讀取失敗")
    except:print("不明ERROR，請關閉程式來檢查ERROR的原因(35)")
logindatalist=[]
try:
    file=open("accounts.txt", "r")
    for line in file:
        logindatadict={}
        (role,acc,pwd) = line.split(",")
        logindatadict["acc"]=acc
        logindatadict["pwd"]=int(pwd)
        logindatadict["role"]=role
        logindatalist.append(logindatadict)
    file.close
    while(True):
        acc=input("輸入帳密進行登入，直接Enter則離開\n帳號：")
        if(acc==""):break
        pwd=int(input("密碼："))
        find=login(acc,pwd,logindatalist)
        if(find==-1):print("帳號密碼輸入錯誤\n")
        else:
            while(True):
                role=logindatalist[find]
                name=role["acc"]
                print("\n請輸入你想執行的功能，直接Enter則重新登入")
                if(role["role"]=="user"):
                    num=input("1. BMI計算\n2. 最佳體重計算\n\n=>")
                    if(num=="1"):bmi(name)
                    elif(num=="2"):bweight(name)
                    elif(num==""):break
                    else:print("編號{}功能不存在，請輸入正確編號".format(num))
                else:
                    num=input("1. BMI計算\n2. 最佳體重計算\n9. 觀看log\n\n=>")
                    if(num=="1"):bmi(name)
                    elif(num=="2"):bweight(name)
                    elif(num=="9"):log(name)
                    elif(num==""):break
                    else:print("編號{}功能不存在，請輸入正確編號".format(num))
            wlog("登出",name)
except IOError:print("讀取失敗")
except:print("不明ERROR，請關閉程式來檢查ERROR的原因(51)")
finally:
    lastlog()
    print("\n再見!")