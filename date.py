import sys
"""
coding: utf-8
2018/10/6 05.15pm
By kyL
"""
year=int(input("請輸入年份(ex:2018)："))
month=int(input("請輸入月份(ex:9)："))
day=int(input("請輸入日期(ex:26)："))
"""
閏年介紹
閏年是每4年一次(ex:2016,2020,...)，而那年的二月就會有29天
除了100的倍數以外(ex:100,200,300...)
但如果是400的倍數就一定是閏年(ex:400,800,1200,1600,2000,2400....)
"""
#----------------------------------------------除錯程式
if year<0:
    print("Error:年分輸入錯誤")
    sys.exit()
else:
    if month<0 or month>12:
        print("Error:月份輸入錯誤")
        sys.exit()
    else:
        if (month==4 or month==6 or month==9 or month==11) and (day<0 or day>30)==True:
            print("Error:日期輸入錯誤")
            sys.exit()
        elif month!=2 and (day<0 or day>31)==True:
            print("Error:日期輸入錯誤")
            sys.exit()
        elif (year%400==0 or (year%100!=0 and year%4==0)) and (day<0 or day>29)==True:
            print("Error:日期輸入錯誤")
            sys.exit()
        elif day<0 or day>28 ==True:
            print("Error:日期輸入錯誤")
            sys.exit()
#----------------------------------------------主程式
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
print("從西元1年1月1日至西元"+str(year)+"年"+str(month)+"月"+str(day)+"日是"+str(count)+"天")
count=count%7
{
    0 : lambda: print("而那天是星期日"),
    1  : lambda: print("而那天是星期一"),
    2  : lambda: print("而那天是星期二"),
    3  : lambda: print("而那天是星期三"),
    4  : lambda: print("而那天是星期四"),
    5  : lambda: print("而那天是星期五"),
    6  : lambda: print("而那天是星期六")
}.get(count)()