"This should be schedule to run in crontab at set times per day"

from requests import get, post
from lightdb import LightDB

"""
db file example

{
    "ifttt_event" : "event_name",
    "ifttt_key" : "key",
    "crypto" : ["dogecoin", "ripple", "decentraland", "shiba-inu" ,"helium", "basic-attention-token", "micropets"]
}
"""

# get db from json file with keys
db = LightDB("keys.json")
ifttt_event = db.get("ifttt_event") # get the event
ifttt_key = db.get("ifttt_key") # get the key

prices = []
s = "" # string to hold all the values we'll push to IFTTT

coins = db.get("crypto")
for coin in coins:
    x = get(f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids={coin}").json()[0]
    price = round(float(x['current_price']), 2)
    if price == 0:
        price = round(float(x['current_price'])*1000, 2) # if the price is super low multiply it so we can see it scale
        if price == 0:
            price = round(float(x['current_price'])*100000, 2) # if the price is still super low
    prices.append(f"{x['symbol']}: {price}")
value = " | ".join(prices) # create one big string for all the prices that we'll use to pipe into the variable to IFTTT

data = {
    "value1" : value
}

# push prices to IFTTT notification on phone 
post(f'https://maker.ifttt.com/trigger/{ifttt_event}/with/key/{ifttt_key}', data=data)