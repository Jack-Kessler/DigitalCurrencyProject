import requests
import json
import creds


#GetToken

url = "https://bravenewcoin.p.rapidapi.com/oauth/token"

payload = {
	"audience": "https://api.bravenewcoin.com",
	"client_id": f"{creds.client_id}",
	"grant_type": "client_credentials"
}
headers = {
	"content-type": "application/json",
	"X-RapidAPI-Key": f"{creds.xrapidAPIkey}",
	"X-RapidAPI-Host": "bravenewcoin.p.rapidapi.com"
}

response = requests.request("POST", url, json=payload, headers=headers)

data = json.loads(response.text)
#print(json.dumps(data, indent=2))
auth = data['access_token']
#NOTE: auth is of type string

#----------------------------------------------------------------------------------------------

#Get Single AssetTicker

url = "https://bravenewcoin.p.rapidapi.com/market-cap"

for currency in creds.crypto_list:
	querystring = {"assetId":f"{currency}"}
	headers = {
	"Authorization": f"Bearer {auth}",
	"X-RapidAPI-Key": f"{creds.xrapidAPIkey}",
	"X-RapidAPI-Host": "bravenewcoin.p.rapidapi.com"
	}
	response = requests.request("GET", url, headers=headers, params=querystring)
	data = json.loads(response.text)
	print(json.dumps(data, indent=2))
	print("\n")
	#NOTE: response.text (or variable "data") is class = dictionary




#print(response.text)
#print("\n")



#print(type(data['content'])) 
#NOTE: data['content'] is of type list.

#for par in data['content']:
#	print(par['price'])

#Prints out only price




