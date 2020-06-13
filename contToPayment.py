# 3c - continue to payment - post shipping method (USPS first class 2 business days)

# for pressing the continue to payment button
# select shipping method

import requests
import json
from bs4 import BeautifulSoup

# read cookies.json to get cookies
with open('jsons/cookies.json', 'r') as f:
    cookies = json.load(f)

# var for storing the url of the shipping page get request:
shipping_url = cookies['shippingURL']
shipping_path = shipping_url[18:]  # remove the first 18 chars(https://figpin.com) of the url to get the path
print(shipping_path)

# TODO: update cookies for the req header
# request headers for the get request for shipping html page
req_headers1 = {
    'authority': 'figpin.com',
    'method': 'GET',
    'path': '/5443715170/checkouts/7d65565d63f9cecb9af55e04b4f11911?previous_step=contact_information&step=shipping_method',
    'scheme': 'https',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'cookie': 'checkout=eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaEpJaVZpTnpneVlUSmhaalkzTm1VMll6YzFNbVl3TURKaE16aGpNMk0xT0RkaE9RWTZCa1ZVIiwiZXhwIjoiMjAyMC0wNi0xOVQwMzozMzozNy4yMDBaIiwicHVyIjoiY29va2llLmNoZWNrb3V0In19--4ccf93dcfdf7ab9e335cfb5563078be992809adc; '
              'tracked_start_checkout=7d65565d63f9cecb9af55e04b4f11911; '
              'checkout_token=eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaEpJaVUzWkRZMU5UWTFaRFl6WmpsalpXTmlPV0ZtTlRWbE1EUmlOR1l4TVRreE1RWTZCa1ZVIiwiZXhwIjoiMjAyMS0wNS0yOVQwMzozMzozNy4yMDBaIiwicHVyIjoiY29va2llLmNoZWNrb3V0X3Rva2VuIn19--2aac717bf1282d3b8a53a7a02434671dc8b3a1e8; '
              '__cfduid=d1d2967187f8915cba5ff9775b0c74fac1590717735; '
              '_y=aab67577-1ac0-486d-8bff-4a3f410f4744; '
              'cart_currency=USD; '
              '_orig_referrer=https%3A%2F%2Ffigpin.com%2F; '
              'secure_customer_sig=; '
              '_landing_page=%2Fcollections%2Fnew-releases%2Fproducts%2Fryuji-sakamoto-448; '
              '_shopify_y=aab67577-1ac0-486d-8bff-4a3f410f4744; '
              '_shopify_fs=2020-05-29T02%3A02%3A16.194Z; '
              'cart=30184109d1d9b354f8a9a5a83d6efa39; '
              'cart_sig=0d273edd5d5ce1335b001970557db7ce; '
              'cart_ts=1590717746; '
              '_secure_session_id=bfcb45e966291048f0e0e2263bbe01f2',
    'pragma': 'no-cache',
    'referer': 'https://figpin.com/',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
}

# make the get request for the html page
res1 = requests.get(shipping_url, headers=req_headers1)

# getting the authenticity_token with bs4:
soup = BeautifulSoup(res1.content, "html.parser")
auth_token_inputs = soup.select('input[name="authenticity_token"]')
auth_token0 = auth_token_inputs[0]['value']
print(auth_token0)


# ------------------------------- making the post request  ----------------------------
req_url = cookies['checkOutURL']
req_path = req_url[18:]  # remove the first 18 chars(https://figpin.com) of the url to get the path
print(req_path)

# form data for the continue to payment post request
form_data = {
    "method": "patch",
    "authenticity_token": auth_token0,
    "previous_step": "shipping_method",
    "step": "payment_method",
    "checkout[shipping_rate][id]": "usps-FirstPackage-3.93",  # TODO get the correct price here based off shipping info
    "checkout[client_details][browser_width]": "1536",
    "checkout[client_details][browser_height]": "758",
    "checkout[client_details][javascript_enabled]": "1",
    "checkout[client_details][color_depth]": "24",
    "checkout[client_details][java_enabled]": "false",
    "checkout[client_details][browser_tz]": "420",
}

request_headers = {
    "authority": "figpin.com",
    "method": "POST",
    "path": req_path,
    "scheme": "https",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "no-cache",
    "content-length": "540",
    "content-type": "application/x-www-form-urlencoded",
    "cookie": "checkout="+cookies['checkout']+"; "
              "tracked_start_checkout="+cookies['tracked_start_checkout']+"; "
              "checkout_token="+cookies['checkout_token']+"; "
              "cart_currency=USD; "
              "cart="+cookies['cart']+"; "
              "cart_sig="+cookies['cart_sig']+"; "
              "secure_customer_sig=; "
              "cart_ts="+cookies['cart_ts']+"; "
              "_orig_referrer=https%3A%2F%2Ffigpin.com%2Fcart; "
              "_secure_session_id="+cookies['_secure_session_id']+"; "
              "_landing_page=%2F5443715170%2Fcheckouts%2F"+req_url[39:]+"; ",
    "origin": "https://figpin.com",
    "pragma": "no-cache",
    "referer": "https://figpin.com/",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
}

# make the continue to payment POST request
r = requests.post(req_url, data=form_data, headers=request_headers)

# get the url of the redirect to shipping step
paymentUrl = "payment url"
if r.history:
    print("Request was redirected")
    for resp in r.history:
        print(resp.status_code, resp.url)
    print("Final destination:")
    paymentUrl = r.url
    print(r.status_code, r.url)
else:
    print("Request was not redirected")

# check status code
print('\nStatus Code: ' + str(r.status_code))

# save res headers to json file
with open(f'jsons/contToPayment_res_headers.json', 'w') as filehandle:
    json.dump(dict(r.headers), filehandle, indent=2)
    print('\nSaved response headers to jsons/contToPayment_res_headers.json')
filehandle.close()

# TODO pass cookies to next step
# For now lets save the checkout cookies to json. When we put everything together in main, use a python object/dict
cookies['checkout'] = r.cookies['checkout']
cookies['checkout_token'] = r.cookies['checkout_token']
cookies['paymentURL'] = paymentUrl
with open(f'jsons/cookies.json', 'w') as filehandle:
    json.dump(dict(cookies), filehandle, indent=2)
    print('\nSaved checkout cookies to jsons/cookies.json')
filehandle.close()

