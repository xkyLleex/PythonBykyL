import emailtest, bookstock , startstock , search
while True:
    print("輸入編號來指定功能(按Enter已結束程式)\
    \n1.開始股票功能\n2.預定股票(未來限定)\n3.測試Email\n4.查詢預定的股票\n5.刪除預定的股票")
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
    else:print("並無此代號")
    print()