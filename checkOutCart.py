# 3a - check out cart from figpin.com/cart redirects to a cart checkout page
import requests
import json

# read cookies.json to get cart cookies
with open('jsons/cookies.json', 'r') as f:
    cookies = json.load(f)

# make a dict for form data and req headers
form_data = {
    'updates[]': '1',
    'checkout': 'Check Out'
}

request_headers = {
    'authority': 'figpin.com',
    'method': 'POST',
    'path': '/cart',
    'scheme': 'https',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'content-length': '34',   # might need to modify this
    'content-type': 'application/x-www-form-urlencoded',
    'cookie': '_shopify_country=United+States; '
              'cart_currency=USD; '
              'secure_customer_sig=; '
              'cart='+cookies['cart']+'; '
              'cart_ts='+cookies['cart_ts']+'; '
              'cart_sig='+cookies['cart_sig']+'; ',
    'dnt': '1',
    'origin': 'https://figpin.com',
    'pragma': 'no-cache',
    'referer': 'https://figpin.com/cart',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
}

# make the checkout from cart POST request
r = requests.post('https://figpin.com/cart', data=form_data, headers=request_headers)

# getting the checkout url for next step (cont to shipping)
checkOutUrl = "url"
if r.history:
    print("Request was redirected")
    i = 0
    for resp in r.history:
        print(resp.status_code, resp.url)
        cookies['cart_ts'] = resp.cookies['cart_ts']
    print("Final destination:")
    checkOutUrl = r.url
    print(r.status_code, checkOutUrl)
else:
    print("Request was not redirected")

# check status code
print('\nStatus Code: ' + str(r.status_code))

# save res headers to json file
with open(f'jsons/checkOutCart_res_headers.json', 'w') as filehandle:
    json.dump(dict(r.headers), filehandle, indent=2)
    print('\nSaved response headers to jsons/checkOutCart_res_headers.json')
filehandle.close()

"""
# save res content to txt file
with open(f'jsons/checkOutCart_res_content.txt', 'w') as filehandle:
    filehandle.write(r.text)
    print('\nSaved response content to jsons/checkOutCart_res_content.txt')
filehandle.close()"""

# TODO: pass checkout token cookies to the next step
# For now lets save the checkout cookies to json. When we put everything together in main, use a python object/dict
cookies['checkout'] = r.cookies['checkout']
cookies['checkout_token'] = r.cookies['checkout_token']
cookies['tracked_start_checkout'] = r.cookies['tracked_start_checkout']
cookies['_secure_session_id'] = r.cookies['_secure_session_id']

cookies['checkOutURL'] = checkOutUrl

with open(f'jsons/cookies.json', 'w') as filehandle:
    json.dump(dict(cookies), filehandle, indent=2)
    print('\nSaved checkout cookies to jsons/cookies.json')
filehandle.close()

