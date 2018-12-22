import emailtest, bookstock , startstock
while True:
    num=input("輸入編號來指定功能(按Enter已結束程式)\n1.開始股票功能\n2.預定股票(未來限定)\n3.測試Email\n請輸入編號:")
    if num=="":break
    #send email stock and analysis
    if num=="1":startstock.startstockgo()
    #book stock(only future)
    elif num=="2":bookstock.bookstockgo()
    #email test
    elif num=="3":emailtest.testgo()
    else:print("並無此代號")
