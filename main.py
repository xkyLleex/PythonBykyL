import emailtest, bookstock , startstock , search
while True:
    print("\n請輸入編號選擇您想要的功能(按Enter直接結束程式)\
    \n1.執行程式(請先至2.設定欲追蹤的股票)\n2.預設股票\n3.查詢預設股票\n4.刪除預設股票\n5.測試Email")
    num=input("請輸入編號:")
    if num=="":break
    #send email stock and analysis
    if num=="1":startstock.startstockgo()
    #book stock(only future or now)
    elif num=="2":bookstock.bookstockgo()
    #search book stock data in the database
    elif num=="3":search.datasearch()
    #delete book stock data in the database
    elif num=="4":search.delete()
    #email test
    elif num=="5":emailtest.testgo()
    else:print("查無此編號，請重新輸入")
print()