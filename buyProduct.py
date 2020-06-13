# 3. check out cart
# 4. check if buy was successful
# All in one session

import requests
import json
from bs4 import BeautifulSoup
import captchaHarvester as ch


# start a request session
# should keep cookies throughout all requests and responses
# s = requests.Session()

'''
# --------------------------- 2 - add item to cart -------------------------------
# make a dict for form data and request headers
form_data = {
    'form_type': 'product',
    'utf8': True,
    'id': '31399726645346',  # TODO: change this to new products variantID (get from shopifyMonitor/avCheck)
    'quantity': 1
}

request_headers = {
    'authority': 'figpin.com',
    'method': 'POST',
    'path': '/cart/add.js',
    'scheme': 'https',
    'accept': 'text/plain, */*; q=0.01',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://figpin.com',
    'pragma': 'no-cache',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest'
}

# save request headers to session request
s.headers.update(request_headers)

# make the add.js to cart POST request
print('Adding item id xxxxx to cart...')   # change xxx to itemid variable
r = s.post('https://figpin.com/cart/add.js', data=form_data)

# check status code
print('Add to Cart request Status Code: ' + str(r.status_code))

"""# Save cookies to json to double check work during debugging
cart_cookies = {
    'cart': r.cookies['cart'],
    'cart_sig': r.cookies['cart_sig'],
    'cart_ts': r.cookies['cart_ts']
}
with open(f'jsons/cookies.json', 'w') as filehandle:
    json.dump(dict(cart_cookies), filehandle, indent=2)
    print('\nSaved cart cookies to jsons/cookies.json')
filehandle.close()"""

print("\nEnd 2")'''


def buy(s):

    # --------------------------- 3a - check out cart -------------------------------
    # make a dict for checking out cart form data and req headers
    form_data = {
        'updates[]': '1',  # might need to change this, not sure what it means
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
        'content-type': 'application/x-www-form-urlencoded',
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

    # save request headers to session request
    s.headers.update(request_headers)

    # make the checkout from cart POST request
    print("Checking out cart, making post request...")
    r = s.post('https://figpin.com/cart', data=form_data)

    # getting the checkout url
    checkOutUrl = "url"
    if r.history:
        print("Request was redirected")
        for resp in r.history:
            print(resp.status_code, resp.url)
        print("Final destination:")
        checkOutUrl = r.url
        print(r.status_code, checkOutUrl)
    else:
        print("Request was not redirected")
    # print(checkOutUrl)  # should be https://figpin.com/5443715170/checkouts/ + checkout hex code

    checkOutID = checkOutUrl[40:]  # getting just the checkout identifier
    print("Checkout Id: ", checkOutID)

    # check status code
    print('\nCheck out cart Status Code: ' + str(r.status_code))

    print("\nEnd 3a")

    # --------------------------- 3b - continue to shipping -------------------------------
    # get the data for inputting into the form (name, address, etc)
    with open('formData.json', 'r') as f:
        formData = json.load(f)

    # var for storing the url of the request:
    req_url = checkOutUrl    # checkOutUrl should always be the same, req_url can change
    req_path = req_url[18:]  # remove the first 18 chars(https://figpin.com) of the url to get the path
    print(req_path)  # checkouts/ + checkout hex code

    # make the request headers for getting the authenticity token. Need to make a get request for the html page and then parse it
    request_headers = {
        "authority": "figpin.com",
        "method": "GET",
        "path": req_path,
        "scheme": "https",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
    }

    # save request headers to session request
    s.headers.update(request_headers)

    # make the get request for the html page
    r = s.get(req_url)

    # getting the authenticity_token:
    soup = BeautifulSoup(r.content, "html.parser")
    auth_token = soup.select_one('input[name="authenticity_token"]')
    # auth_token = auth_token[0]['value']
    print("3b auth_token: ")
    print(auth_token['value'])
    print('\n...')

    # getting the captcha token using captcha harvester:
    captcha_token = ch.get_captcha_token()

    form_data = {
        '_method': 'patch',
        'authenticity_token': auth_token['value'],
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
        'g-recaptcha-response': captcha_token,
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
        'content-type': 'application/x-www-form-urlencoded',
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

    # save request headers to session request
    s.headers.update(request_headers)

    # make the continue to shipping POST request
    print("Making the continue to shipping post request... ")
    r = s.post(req_url, data=form_data)

    # get the url of the redirect to shipping step
    shippingUrl = "url"
    if r.history:
        print("Request was redirected")
        for resp in r.history:
            print(resp.status_code, resp.url)
        print("Final destination:")
        shippingUrl = r.url
        print(r.status_code, shippingUrl)
    else:
        print("Request was not redirected")

    # check status code
    print('\nStatus Code: ' + str(r.status_code))

    print("\nEnd 3b")


    # ------------------------------- 3c - continue to payment - post shipping method (USPS first class 2 business days) ---------------------------------
    # var for storing the url of the shipping page get request:
    shipping_path = shippingUrl[18:]  # remove the first 18 chars(https://figpin.com) of the url to get the path
    print(shipping_path)

    # request headers for the get request for shipping html page
    request_headers = {
        'authority': 'figpin.com',
        'method': 'GET',
        'path': shipping_path,
        'scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'referer': 'https://figpin.com/',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
    }
    # save request headers to session request
    s.headers.update(request_headers)
    # make the get request for the html page
    r = s.get(shippingUrl)

    # getting the authenticity_token with bs4:
    soup = BeautifulSoup(r.content, "html.parser")
    auth_token = soup.select_one('input[name="authenticity_token"]')
    print(auth_token['value'])

    # -------- make a request to usps server to get the shipping rate -----------------
    # var for storing the url of the shipping rates page get request:
    shipping_rates_url = checkOutUrl+"/shipping_rates?step=shipping_method"

    # request headers for the get request for shipping rates html page
    request_headers = {
        "authority": "figpin.com",
        "method": "GET",
        "path": shipping_rates_url[18:],
        "scheme": "https",
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "referer": "https://figpin.com/",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
    }
    # save request headers to session request
    s.headers.update(request_headers)
    # make the get request for the html page
    r = s.get(shipping_rates_url)

    # getting the shipping rate with bs4:
    soup = BeautifulSoup(r.content, "html.parser")
    shipping_rate = soup.select_one('input[class="radio-wrapper"]')
    print("Shipping rate: ")
    print(shipping_rate['data-shipping-method'])


    # form data for post request to continue to payment
    form_data = {
        "_method": "patch",
        "authenticity_token": auth_token['value'],
        "previous_step": "shipping_method",
        "step": "payment_method",
        # "checkout[shipping_rate][id]": "usps-FirstPackage-3.93",
        "checkout[shipping_rate][id]": shipping_rate['data-shipping-method'],
        "checkout[client_details][browser_width]": "1036",
        "checkout[client_details][browser_height]": "695",
        "checkout[client_details][javascript_enabled]": "1",
        "checkout[client_details][color_depth]": "24",
        "checkout[client_details][java_enabled]": "false",
        "checkout[client_details][browser_tz]": "420"
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

    # save request headers to session request
    s.headers.update(request_headers)
    # make the continue to payment POST request
    print("Making the continue to payment post request... ")
    r = s.post(req_url, data=form_data)

    # get the url of the redirect to payment step
    paymentUrl = "url"
    if r.history:
        print("Request was redirected")
        for resp in r.history:
            print(resp.status_code, resp.url)
        print("Final destination:")
        paymentUrl = r.url
        print(r.status_code, paymentUrl)
    else:
        print("Request was not redirected")

    print("\nEnd 3c")

    # ------------------------------- 3d - pay now - post credit card info ---------------------------------
    # var for storing the url of the payment page get request:
    payment_path = paymentUrl[18:]  # remove the first 18 chars(https://figpin.com) of the url to get the path
    print(payment_path)

    # request headers for the get request for shipping html page
    request_headers = {
        'authority': 'figpin.com',
        'method': 'GET',
        'path': payment_path,
        'scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'referer': 'https://figpin.com/',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
    }
    # save request headers to session request
    s.headers.update(request_headers)
    # make the get request for the html page
    r = s.get(paymentUrl)

    # instantiating soup
    soup = BeautifulSoup(r.content, "html.parser")

    # getting the authenticity_token with bs4:
    auth_token = soup.select_one('input[name="authenticity_token"]')
    print(auth_token['value'])

    # getting the total price with bs4:
    total_price = soup.select_one('input[name="checkout[total_price]"]')
    print(total_price['value'])

    # getting the "s" value with bs4:
    s_value = soup.select_one('input[name="s"]')
    sv = ""
    if s_value["value"]:
        sv = s_value["value"]

    #   ------------- request to shopify server for submitting credit card info ----------------
    request_headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Length": "118",
        "Content-Type": "application/json",
        "DNT": "1",
        "Host": "deposit.us.shopifycs.com",
        "Origin": "https://checkout.us.shopifycs.com",
        "Pragma": "no-cache",
        "Referer": "https://checkout.us.shopifycs.com/number?identifier="+checkOutID+"&location=https%3A%2F%2Ffigpin.com%2F5443715170%2Fcheckouts%2F"+checkOutID+"%3Fprevious_step%3Dshipping_method%26step%3Dpayment_method&dir=ltr",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"
    }
    # the credit card info is the payload data
    payload = {
        "credit_card": {
                "number": formData["ccNumber"],
                "name": formData["ccName"],
                "month": formData["ccMonth"],
                "year": formData["ccYear"],
                "verification_value": formData["ccVerificationValue"]
        }
    }
    # save request headers to session request
    s.headers.update(request_headers)
    # make the submit credit card post request with payload as a param
    print("Making the submit credit card post request to shopify sessions server... ")
    r = s.post("https://deposit.us.shopifycs.com/sessions", params=payload)
    print("submitted credit card post request ", r.status_code)
    print("\n...")
    #   ------------- END: request to shopify server for submitting credit card info ----------------

    # payment page form data
    form_data = {
        "_method": "patch",
        "authenticity_token": auth_token['value'],
        "previous_step": "payment_method",
        "step": "",
        "s": sv,
        "checkout[payment_gateway]": "26080378978",  # what
        "checkout[credit_card][vault]": "false",
        "checkout[different_billing_address]": formData["checkout[different_billing_address]"],
        "checkout[billing_address][first_name]": formData["checkout[billing_address][first_name]"],
        "checkout[billing_address][last_name]": formData["checkout[billing_address][last_name]"],
        "checkout[billing_address][address1]": formData["checkout[billing_address][address1]"],
        "checkout[billing_address][address2]": formData["checkout[billing_address][address2]"],
        "checkout[billing_address][city]": formData["checkout[billing_address][city]"],
        "checkout[billing_address][country]": formData["checkout[billing_address][country]"],
        "checkout[billing_address][province]": formData["checkout[billing_address][province]"],
        "checkout[billing_address][zip]": formData["checkout[billing_address][zip]"],
        "checkout[billing_address][phone]": formData["checkout[billing_address][phone]"],
        "checkout[remember_me]": "false",
        "checkout[remember_me]": "0",
        "checkout[vault_phone]": "",
        "checkout[total_price]": total_price['value'],
        "complete": "1",
        "checkout[client_details][browser_width]": "1519",
        "checkout[client_details][browser_height]": "754",
        "checkout[client_details][javascript_enabled]": "1",
        "checkout[client_details][color_depth]": "24",
        "checkout[client_details][java_enabled]": "false",
        "checkout[client_details][browser_tz]": "420"
    }
    # payment request headers
    request_headers = {
        "authority": "figpin.com",
        "method": "POST",
        "path": req_path,
        "scheme": "https",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
        "cache-control": "no-cache",
        "content-length": "1680",
        "content-type": "application/x-www-form-urlencoded",
        "dnt": "1",
        "origin": "https://figpin.com",
        "pragma": "no-cache",
        "referer": "https://figpin.com/",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"
    }

    # save request headers to session request
    s.headers.update(request_headers)

    # make the pay now POST request
    print("Making the pay now post request... ")
    r = s.post(req_url, data=form_data)

    # get the url of the redirect to shipping step
    processingUrl = "url"
    if r.history:
        print("Request was redirected")
        for resp in r.history:
            print(resp.status_code, resp.url)
        print("Final destination:")
        processingUrl = r.url
        print(r.status_code, processingUrl)
    else:
        print("Request was not redirected")

    print("\nEnd of buyproduct.py")









