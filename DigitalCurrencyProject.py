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

#Code below was provided from RapidAPI
for currency in creds.crypto_list:
	querystring = {"assetId":f"{currency}"}
	headers = {
	"Authorization": f"Bearer {auth}",
	"X-RapidAPI-Key": f"{creds.xrapidAPIkey}",
	"X-RapidAPI-Host": "bravenewcoin.p.rapidapi.com"
	}
	response = requests.request("GET", url, headers=headers, params=querystring)
	data = json.loads(response.text) 

	for par in data['content']:
		assetId = (par['assetId'])
		timeStamp = (par['timestamp'])
		price = (par['price'])

	#print(type(response.text)) #NOTE: response.text class = str
	#print(type(data)) # data class = dict
	#print(type(data['content'])) # data['content'] class = list

	#print(json.dumps(data, indent=2)) #Prints out all data properties
	#jVar = json.dumps(data, indent=2)
	#print(type(jVar)) #jVar class = str
	#print("\n")
	#print(jVar)
	#print("\n")