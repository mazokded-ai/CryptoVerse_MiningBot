from fastapi import FastAPI
from pydantic import BaseModel, Field
import sqlite3,time
app=FastAPI(title="CryptoVerse API")
DB="cryptoverse.db"
def db():
 c=sqlite3.connect(DB)
 c.execute("CREATE TABLE IF NOT EXISTS users(user_id INTEGER PRIMARY KEY,balance REAL DEFAULT 0,rate REAL DEFAULT 0.1,last_ts INTEGER,last_daily INTEGER DEFAULT 0)")
 c.commit();return c
class User(BaseModel): user_id:int=Field(gt=0)
@app.get("/api/state")
def state(user_id:int):
 now=int(time.time());c=db();r=c.execute("SELECT balance,rate,last_ts,last_daily FROM users WHERE user_id=?",(user_id,)).fetchone()
 if not r:
  c.execute("INSERT INTO users(user_id,last_ts) VALUES(?,?)",(user_id,now));c.commit();r=(0,0.1,now,0)
 balance,rate,last_ts,last_daily=r;balance+=max(0,now-last_ts)*rate
 c.execute("UPDATE users SET balance=?,last_ts=? WHERE user_id=?",(balance,now,user_id));c.commit();c.close()
 return {"balance":round(balance,4),"rate":rate,"daily_available":now-last_daily>=86400}
@app.post("/api/daily")
def daily(p:User):
 now=int(time.time());c=db();r=c.execute("SELECT last_daily FROM users WHERE user_id=?",(p.user_id,)).fetchone()
 if not r:
  c.execute("INSERT INTO users(user_id,last_ts) VALUES(?,?)",(p.user_id,now));r=(0,)
 if now-r[0]<86400:c.close();return {"ok":False,"message":"Бонус уже получен сегодня"}
 c.execute("UPDATE users SET balance=balance+50,last_daily=?,last_ts=? WHERE user_id=?",(now,now,p.user_id));c.commit();c.close()
 return {"ok":True,"message":"+50 CV получено!"}
@app.post("/api/upgrade")
def upgrade(p:User):
 c=db();r=c.execute("SELECT balance,rate FROM users WHERE user_id=?",(p.user_id,)).fetchone()
 if not r:c.close();return {"ok":False,"message":"Сначала открой майнинг"}
 balance,rate=r;cost=round(25*(rate/0.1),2)
 if balance<cost:c.close();return {"ok":False,"message":f"Нужно {cost} CV"}
 c.execute("UPDATE users SET balance=balance-?,rate=rate+0.05,last_ts=? WHERE user_id=?",(cost,int(time.time()),p.user_id));c.commit();c.close()
 return {"ok":True,"message":"Майнер улучшен!"}
