import requests , bs4 , sqlite3
def one():
    url = "https://movies.yahoo.com.tw/chart.html?.tsrc=xl"
    html = requests.get(url)
    if html.status_code != 200:
        print('網址無效:', html.url)
        return
    soup = bs4.BeautifulSoup(html.text, 'html.parser')
    try:
        filmDate=soup.select_one("div.rank_list.table.rankstyle1 > div:nth-of-type(2) > div:nth-of-type(5)").text
    except:
        print("網頁發生錯誤")
        return
    database.execute("drop table if exists 'films';")
    database.execute('''
                 create table films
                 (
                         filmRank   integer primary key autoincrement,
                         filmName   text                     not null,
                         filmDate   text                     not null,
                         filmRating real                     not null
                         );
                ''')
    for i in range(2, 12):
        filmDate=soup.select_one("div.rank_list.table.rankstyle1 > div:nth-of-type({}) > div:nth-of-type(5)".format(i)).text
        filmRating=soup.select_one("div.rank_list.table.rankstyle1 > div:nth-of-type({}) > div.td.starwithnum > h6".format(i)).text
        if i == 2:filmName = soup.select_one("div.rank_list.table.rankstyle1 > div:nth-of-type(2) > div:nth-of-type(4) > a > dl > dd > h2").text
        else:filmName = soup.select_one("div.rank_list.table.rankstyle1 > div:nth-of-type({}) > div:nth-of-type(4) > a > div".format(i)).text
        sql = "INSERT INTO films(filmName, filmDate, filmRating) VALUES ('{}','{}',{});".format(filmName, filmDate, float(filmRating))
        database.execute(sql)
    database.commit()
    print("change {} records".format(database.total_changes))
def two():
    try:
        filmsdata = database.execute("select * from films;")
    except:
        print("資料庫錯誤:no such table:filmes")
        return
    print("------------------------------------------------")
    print("排名  放映日期   推薦   片名")
    print("------------------------------------------------")
    for record in filmsdata:
        print(" {:>2}  {}   {}   {}".format(record[0],record[2],record[3],record[1]))
    print("------------------------------------------------")
def three():
    try:
        database.execute("DELETE FROM films;")
        database.execute("DELETE FROM sqlite_sequence WHERE name = 'films';")
        database.commit()
        print("change {} records".format(database.total_changes))
    except:
        print("資料庫錯誤:no such table:filmes")
while True:
    num = input("\n請輸入你想執行的功能，直接Enter則離開\n1. 即時擷取資料\n2. 查詢電影排行\n3. 清除資料\n=>")
    if num == "":break
    database = sqlite3.connect('movieList.db')
    if num == "1":one()
    elif num == "2":two()
    elif num == "3":three()
    else:print("並無此代碼")
    database.close()
