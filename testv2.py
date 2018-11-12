import pprint,time
def lastlog():
    file=open(time.strftime("%m%d%H%M.log"), "a",encoding="UTF-8")
    for dict in dataloglist:
        file.write(dict["username"]+dict["datatime"]+dict["action"]+"\n")
    file.close
def wlog(move,name):
    datalogdict={}
    datalogdict["action"]=move
    datalogdict["datatime"]=time.strftime(",%Y-%m-%d %H:%M:%S,")
    datalogdict["username"]=name
    return datalogdict
def login(acc,pwd,datalist):
    i=0
    for data in datalist:
        if(data["acc"]==acc):
            if(data["pwd"]==pwd):
                dataloglist.append(wlog("登入",acc))
                return i
        i+=1
    return -1
def bmi(name):
    dataloglist.append(wlog("BMI計算",name))
    w=float(input("體重："))
    h=float(input("身高："))
    print("你的BMI指數為：%.2f\n"%(w/(h*h/10000))) if w>0 and h>0 else print("輸入數值錯誤\n")      
def bweight(name):
    dataloglist.append(wlog("最佳體重計算",name))
    h=float(input("身高："))
    print("你的最佳體重為：%.1f\n"%(22*h*h/10000)) if h>0 else print("輸入數值錯誤\n")
dataloglist=[]
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
                    elif(num=="9"):
                        dataloglist.append(wlog("觀看log",name))
                        pprint.pprint(dataloglist)
                    elif(num==""):break
                    else:print("編號{}功能不存在，請輸入正確編號".format(num))
            dataloglist.append(wlog("登出",name))
    lastlog()
except IOError:print("讀取失敗")
except:print("不明ERROR，請關閉程式來檢查ERROR的原因(51)")
finally:
    print("\n再見!")