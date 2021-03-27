import requests
import pprint
r=requests.get('https://api.coincap.io/v2/assets/bitcoin')
s=requests.get('https://api.coincap.io/v2/assets/ripple')

def databaseCreator():
    import mysql.connector
    
    #connection start
    conn=mysql.connector.connect(user='root',host='localhost',passwd='Subinsk284@')

    cur=conn.cursor()
    cur.execute('create database if not exists crypto')
    cur.execute('use crypto')
    cur.execute('create table if not exists cryptodata(SNo int primary key auto_increment,Name varchar(20) not null unique,Market_Cap varchar(20) not null,Price varchar(20) not null,Volume varchar(20) not null,Circulating_Supply varchar(20) not null,Change_24h varchar(10) not null)')
    cur.execute('select * from cryptodata')
    fetchdata=cur.fetchall()

    if fetchdata==[]:
        cur.execute('insert into cryptodata(Name,Market_Cap,Price,Volume,Circulating_Supply,Change_24h) values(%s,%s,%s,%s,%s,%s)',(r.json()['data']['id'],r.json()['data']['marketCapUsd'],'$7200.20','$22917521651','18068650 BTC','-0.39%'))
        cur.execute('insert into cryptodata(Name,Market_Cap,Price,Volume,Circulating_Supply,Change_24h) values(%s,%s,%s,%s,%s,%s)',(s.json()['data']['id'],'$16042430757','$147.58','$7837436868','108702955 ETH','-0.44%'))
        cur.execute('insert into cryptodata(Name,Market_Cap,Price,Volume,Circulating_Supply,Change_24h) values(%s,%s,%s,%s,%s,%s)',('XRP','$9549596416','$0.220546','$1388391306','43299885509 XRP','-0.02%'))
        cur.execute('insert into cryptodata(Name,Market_Cap,Price,Volume,Circulating_Supply,Change_24h) values(%s,%s,%s,%s,%s,%s)',('Tether','$4174187062','$1.02','$24593296896','4108044456 USDT','1.47%'))
        cur.execute('insert into cryptodata(Name,Market_Cap,Price,Volume,Circulating_Supply,Change_24h) values(%s,%s,%s,%s,%s,%s)',('Bitcoin_Cash','$3865731673','$213.17','$1895892271','18134463 BCH','0.54%'))
        cur.execute('insert into cryptodata(Name,Market_Cap,Price,Volume,Circulating_Supply,Change_24h) values(%s,%s,%s,%s,%s,%s)',('Litecoin','$2996135038','$47.02','$2714116613','63713713 LTC','0.68%'))
        cur.execute('insert into cryptodata(Name,Market_Cap,Price,Volume,Circulating_Supply,Change_24h) values(%s,%s,%s,%s,%s,%s)',('EOS','$2478735475','$2.63','$1938961995','941829982 EOS','1.84%'))
        cur.execute('insert into cryptodata(Name,Market_Cap,Price,Volume,Circulating_Supply,Change_24h) values(%s,%s,%s,%s,%s,%s)',('Binance_Coin','$2420116753','$15.56','$217680490','155536713 BNB','0.14%'))
        cur.execute('insert into cryptodata(Name,Market_Cap,Price,Volume,Circulating_Supply,Change_24h) values(%s,%s,%s,%s,%s,%s)',('Bitcoin_SV','$1935591848','$107.13','$567268298','18068415 BSV','0.02%'))
        cur.execute('insert into cryptodata(Name,Market_Cap,Price,Volume,Circulating_Supply,Change_24h) values(%s,%s,%s,%s,%s,%s)',('Stellar','$1153565849','$0.057521','$226231786','20054779554 XLM','-1.58%'))
        conn.commit()

    cur.close()
    conn.close()
