from time import sleep
import requests
from requests.exceptions import Timeout
# -------------------------------------------------------------------------------------------------

def fetch_crypto_prices(*crypto_list):
	crypto_list_prices = {}
	cryptocom_url = "https://api.crypto.com/v2/public/get-ticker"

	print('Retrieving crypto prices..')

	for crypto in crypto_list:
		params = {'instrument_name': f'{crypto.upper()}_USD'}
	
		try:
			response = requests.get(cryptocom_url, params=params, timeout=5)
		except Timeout:
			print(f'{crypto} price (USD): [UNSUCCESSFUL RETRIEVAL - Timed out..]')
		else:
			if response.json().get('code') == 0:
				price = response.json()['result']['data'][0]['a']
				crypto_list_prices[crypto] = float(price)
				print(f'{crypto.upper()} price (USD):', crypto_list_prices[crypto])
			else:
				print(f'{crypto.upper()}:', response.json())

	print(f'SUCCESSFULLY RETRIEVED: {len(crypto_list_prices)}/{len(crypto_list)}')
	return crypto_list_prices

def fetch_nft_fp(OPENSEA_API_KEY, *nft_collection_slug_list):
	nft_floor_prices = {}
	headers = {
		'accept'   : 'application/json',
		'x-api-key': OPENSEA_API_KEY
	}

	print('Retrieving NFT floor prices..')

	for slug in nft_collection_slug_list:
		opensea_url = f"https://api.opensea.io/api/v2/collections/{slug.lower()}/stats"
	
		while True:
			try:
				response = requests.get(opensea_url, headers=headers, timeout=5)
			except Timeout:
				print(f'{slug.lower()}: [UNSUCCESSFUL RETRIEVAL - Timed out..]')
				break

			if response.status_code == 200 and 'total' in response.json():
				fp = response.json()['total']['floor_price']
				nft_floor_prices[slug] = round(fp, 3)
				print(f'{slug.lower()}:', nft_floor_prices[slug])
				break
			elif response.status_code == 429:
				print(f'[Request for "{slug.lower()}" was throttled, retrying in 1 second..]')
				sleep(1)
			else:
				print(f'{slug.lower()}: [{response.status_code} {response.reason}]')
				break
	
	print(f'SUCCESSFULLY RETRIEVED: {len(nft_floor_prices)}/{len(nft_collection_slug_list)}')
	return nft_floor_prices

def get_eth_balances(ETHERSCAN_API_KEY, *eth_addresses):
	eth_balances = {}
	eth_addresses = ','.join(eth_addresses)

	etherscan_url = "https://api.etherscan.io/api"
	params = dict(
		module='account',
		action='balancemulti',
		address=eth_addresses,
		tag='latest',
		apikey=ETHERSCAN_API_KEY
	)

	print('Retrieving ETH balances..')

	try:
		response = requests.get(etherscan_url, params=params, timeout=5)
	except Timeout:
		error_msg = '[UNSUCCESSFUL RETRIEVAL - Timed out..]'
		print(error_msg)
		return

	if response.json().get('status') == '1':
		account_list = response.json()['result']

		for account in account_list:
			address = account['account']
			wei_balance = int(account['balance'])

			eth_balances[address] = wei_balance / 1_000_000_000**2
			print(f'{address}:', eth_balances[address])
	else:
		print(response.json())

	return eth_balances
