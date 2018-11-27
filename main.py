import emailtest, stock , time
while True:
    num=input("輸入編號來指定功能(按Enter已結束程式)\n1.股票功能\n2.測試Email\n請輸入編號:")
    if num=="":
        break
    if num=="1":
        print("現在時間[{}]".format(time.strftime("%Y/%m/%d-%H:%M:%S")))
    elif num=="2":emailtest.testgo()
    else:print("並無此代號")