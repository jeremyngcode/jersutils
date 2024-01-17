import requests
from requests.exceptions import Timeout
# -------------------------------------------------------------------------------------------------

def get_currency_rate(WISE_API_KEY, currency, convert_to):
	currency_pair = f'{currency.upper()}/{convert_to.upper()}'

	wise_url = "https://api.transferwise.com/v1/rates"
	params = {
		'source': currency,
		'target': convert_to
	}
	headers = {'Authorization': f'Bearer {WISE_API_KEY}'}

	try:
		response = requests.get(wise_url, params=params, headers=headers, timeout=5)
	except Timeout:
		result = '[UNSUCCESSFUL RETRIEVAL - Timed out..]'
		print(f'{currency_pair}: {result}')
	else:
		if response.status_code == 200:
			currency_rate = response.json()[0]['rate']
			result = round(currency_rate, 4)
		else:
			result = f'[{response.status_code} {response.reason}]'

	print(f'{currency_pair}: {result}')
	return result
