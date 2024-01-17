import time
import hmac
import hashlib

import requests
from requests.exceptions import Timeout
# -------------------------------------------------------------------------------------------------

def get_cryptocom_user_balance(CRYPTOCOM_API_KEY, CRYPTOCOM_SECRET_KEY, *instrument_names):
	user_balance = {}

	cryptocom_url = "https://api.crypto.com/exchange/v1/"
	method = 'private/user-balance'
	headers = {
		'Content-Type': 'application/json'
	}
	req = {
		'id': 1,
		'method': method,
		'api_key': CRYPTOCOM_API_KEY,
		'params': {},
		'nonce': int(time.time() * 1000)
	}

	payload_str = req['method'] + str(req['id']) + req['api_key'] + str(req['nonce'])

	req['sig'] = hmac.new(
		key=bytes(CRYPTOCOM_SECRET_KEY, 'utf-8'),
		msg=bytes(payload_str, 'utf-8'),
		digestmod=hashlib.sha256
	).hexdigest()

	print('Retrieving crypto.com user balances..')

	try:
		response = requests.post(f'{cryptocom_url}{method}',
			json=req, headers=headers, timeout=5
		)
	except Timeout:
		error_msg = '[UNSUCCESSFUL RETRIEVAL - Timed out..]'
		print(error_msg)
		return

	if response.json().get('code') == 0:
		position_balances = response.json()['result']['data'][0]['position_balances']

		if instrument_names:
			for instrument in instrument_names:
				for item in position_balances:
					if instrument.upper() == item['instrument_name']:
						user_balance[instrument] = float(item['quantity'])
						print(f'{instrument.upper()}:', user_balance[instrument])
						break
				else:
					print(f'{instrument.upper()}: [Invalid instrument name / zero holdings.]')

		else:
			for item in position_balances:
				instrument = item['instrument_name']
				quantity = float(item['quantity'])

				user_balance[instrument] = quantity
				print(f'{instrument}:', user_balance[instrument])

	else:
		print(response.json())

	return user_balance
