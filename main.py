import emailtest, stock 
while True:
    num=input("輸入編號來指定功能(按Enter已結束程式)\n1.股票功能\n2.測試Email\n請輸入編號:")
    if num=="":break
    #send email stock and analysis
    if num=="1":stock.stockgo()
    #email test
    elif num=="2":emailtest.testgo()
    else:print("並無此代號")

"""
0. chose a num
1.input email
2.0 number===>list
2.1 stocknum===>list
2.2 hopestock===>list
2.3 time===>list
3.data===>dict stocknum hpestock time
4. 1sec check stock ===>use load data dict 1 by 1
4.if times up ===>show what num time up and now time on console
4.if stock up to hopestock ===>send email to user and show on console
4.if something happen ===>show on console or send email to user if email doesn't broken
"""