import sqlite3
def datasearch(num=0):
    try:
        conn = sqlite3.connect('bookstock.db')
        sql = "select * from stockdata;"
        data = conn.execute(sql)
        i=1
        for rec in data:
            if num == 0:
                if i==1:
                    print("-"*40)
                    print("編號   日期        時間    股票代碼  期望值")
                print("{:>2}  {} | {} | {:>4} |{:>7}".format(i,rec[0],rec[1],rec[2],rec[3]))
            elif num == i:
                print("刪除中...")
                conn.execute('''
                delete from stockdata where date='{}' and stock={};
                '''.format(rec[0],rec[2]))
                conn.commit()
                print("完畢")
            i+=1
        if(num == 0 and i == 1) or (num != 0 and i == 1):
            print("資料庫無資料！請先預訂股票後才可查詢跟刪除。")
            return "NO"
        if num != 0 and num >= i:print("請輸入正確編號！")
    except sqlite3.Error as e:
        print("\n資料庫錯誤:{}".format(e))
        return
    except Exception as e:
        print("\n發生錯誤:{}\n".format(e))
        return
    finally:
        if "conn" in dir():conn.close()
def delete():
    if datasearch() == "NO":return
    while(True):
        delnum = input("請選擇要刪除的編號(按Enter已結束):")
        if delnum == "":break
        try:
            datasearch(int(delnum)) if int(delnum) > 0 else print("請輸入正確編號！(0以上)")
        except:print("請輸入數字")