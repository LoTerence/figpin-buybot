# 3b - continue to shipping - post shipping address information and solves captcha, should redirect to next page

# for pressing the continue to shipping button
# input shipping information
# deal with google captcha
# should wait 3 secs before post requesting so we don't get flagged for autofill

import requests
import json
from bs4 import BeautifulSoup

# get the data for inputting into the form (name, address, etc)
with open('formData.json', 'r') as f:
    formData = json.load(f)

# read cookies.json to get cookies
with open('jsons/cookies.json', 'r') as f:
    cookies = json.load(f)

# var for storing the url of the request:
req_url = cookies['checkOutURL']
req_path = req_url[18:]  # remove the first 18 chars(https://figpin.com) of the url to get the path
print(req_path)

req_headers1 = {
    "authority": "figpin.com",
    "method": "GET",
    "path": req_path,
    "scheme": "https",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    "cache-control": "no-cache",
    "cookie": "checkout="+cookies['checkout']+"; "
              "tracked_start_checkout="+cookies['tracked_start_checkout']+"; "
              "checkout_token="+cookies['checkout_token']+"; "
              "_shopify_country=United+States; "
              "cart_currency=USD; "
              "secure_customer_sig=; "
              "cart="+cookies['cart']+"; "
              "cart_sig="+cookies['cart_sig']+"; "
              "cart_ts="+cookies['cart_ts']+"; "
              "_orig_referrer=; "
              "_landing_page=%2F; "
              "_secure_session_id="+cookies['_secure_session_id']+"; ",
    "pragma": "no-cache",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
}


# TODO get the res cookies
# make the get request for the html page
res1 = requests.get(req_url, headers=req_headers1)

# getting the authenticity_token with bs4:
soup = BeautifulSoup(res1.content, "html.parser")
auth_token_inputs = soup.select('input[name="authenticity_token"]')
auth_token0 = auth_token_inputs[0]['value']
print(auth_token0)


# ------------ TODO insert captcha harvest code here: --------------------


# ------------ end captcha harvest code -------------------


# make a dict for form data and req headers
# previous_step variable might be important
# TODO change the captcha token
form_data = {
    '_method': 'patch',
    'authenticity_token': auth_token0,
    'previous_step': 'contact_information',
    'step': 'shipping_method',
    'checkout[email]': formData["email"],
    'checkout[buyer_accepts_marketing]': '0',
    'checkout[shipping_address][first_name]': formData["shipping_address-first_name"],
    'checkout[shipping_address][last_name]': formData["shipping_address-last_name"],
    'checkout[shipping_address][address1]': formData["shipping_address-address1"],
    'checkout[shipping_address][address2]': formData["shipping_address-address2"],
    'checkout[shipping_address][city]': formData["shipping_address-city"],
    'checkout[shipping_address][country]': formData["shipping_address-country"],
    'checkout[shipping_address][province]': formData["shipping_address-province"],
    'checkout[shipping_address][zip]': formData["shipping_address-zip"],
    'checkout[shipping_address][phone]': formData["shipping_address-phone"],
    'checkout[shipping_address][first_name]': formData["shipping_address-first_name"],
    'checkout[shipping_address][last_name]': formData["shipping_address-last_name"],
    'checkout[shipping_address][address1]': formData["shipping_address-address1"],
    'checkout[shipping_address][address2]': formData["shipping_address-address2"],
    'checkout[shipping_address][city]': formData["shipping_address-city"],
    'checkout[shipping_address][country]': formData["shipping_address-country"],
    'checkout[shipping_address][province]': formData["shipping_address-province"],
    'checkout[shipping_address][zip]': formData["shipping_address-zip"],
    'checkout[shipping_address][phone]': formData["shipping_address-phone"],
    'g-recaptcha-response': '03AGdBq25kDRpecqhY075gg0iG_FPclqN0Qztxw43iZbTHCV1wmYzIV7rEJ_GMt5OTP3-0kYv5AR8ELwBp0Dt5BLVy-z4iZU3vRQXw2MlnEdKc8wBZanSqAZVc2GpVqS2aDWmYrm-YoArLDDPl7pz-WpJwpsNhfzNfvPxA-T337-rLlG9jh7Ckq38xuTaY5Hp53grBz8xTxQpMmSDOLsCwSHQ8Qddp-b-ymyEpsqhjjaQWoZEaoKInUr9YcUDpaGK7KvMEiuJj7KcTuFJM101luim-hBCvpmNBGpcFeIWIt1-T8mnp7P_LvJSrzbVDXD4vVoab00eARIsMQ7UVlKiKxwzlqU1wLhIjPoJDTsa0WeBLihaF-o60wPzSXqq5yoe0_fkgNafoeEst',
    'checkout[client_details][browser_width]': '1519',
    'checkout[client_details][browser_height]': '754',
    'checkout[client_details][javascript_enabled]': '1',
    'checkout[client_details][color_depth]': '24',
    'checkout[client_details][java_enabled]': 'false',
    'checkout[client_details][browser_tz]': '420'
}

# look into what previous checkout token is
request_headers = {
    'authority': 'figpin.com',
    'method': 'POST',
    'path': req_path,
    'scheme': 'https',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'content-length': '1964',  # this is different? what is the content length?
    'content-type': 'application/x-www-form-urlencoded',
    'cookie': 'checkout='+cookies['checkout']+'; '
              'checkout_token='+cookies['checkout_token']+'; '
              'tracked_start_checkout='+cookies['tracked_start_checkout']+'; '
              '_shopify_country=United+States; '
              'cart_currency=USD; '
              '_orig_referrer=; '
              '_landing_page=%2F; '
              'secure_customer_sig=; '
              'cart='+cookies['cart']+'; '
              '_secure_session_id='+cookies['_secure_session_id']+'; '
              'shopify_pay_redirect=pending; '
              'cart_sig='+cookies['cart_sig']+'; '
              'cart_ts='+cookies['cart_ts']+'',
    'origin': 'https://figpin.com',
    'pragma': 'no-cache',
    'referer': 'https://figpin.com/',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
}

# make the continue to shipping POST request
r = requests.post(req_url, data=form_data, headers=request_headers)

# get the url of the redirect to shipping step
shippingUrl = "url"
if r.history:
    print("Request was redirected")
    for resp in r.history:
        print(resp.status_code, resp.url)
    print("Final destination:")
    shippingUrl = r.url
    print(r.status_code, r.url)
else:
    print("Request was not redirected")

# check status code
print('\nStatus Code: ' + str(r.status_code))

# save res headers to json file
with open(f'jsons/contship_res_headers.json', 'w') as filehandle:
    json.dump(dict(r.headers), filehandle, indent=2)
    print('\nSaved response headers to jsons/contship_res_headers.json')
filehandle.close()

# TODO pass cookies to next step
# For now lets save the checkout cookies to json. When we put everything together in main, use a python object/dict
cookies['checkout'] = r.cookies['checkout']
cookies['checkout_token'] = r.cookies['checkout_token']
cookies['shippingURL'] = shippingUrl
with open(f'jsons/cookies.json', 'w') as filehandle:
    json.dump(dict(cookies), filehandle, indent=2)
    print('\nSaved checkout cookies to jsons/cookies.json')
filehandle.close()
