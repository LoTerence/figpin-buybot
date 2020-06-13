# 2 - add an item to cart
import requests
import json


# function add_to_cart: adds an item to the cart by using the variantid. Must have a request session to work
# returns status code
def add_to_cart(variantid, s):

    # make a dict for form data and request headers
    form_data_dict = {
        'form_type': 'product',
        'utf8': True,
        # 'id': '31399726645346',
        'id': variantid,
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
        'content-length': '61',
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
    r = s.post('https://figpin.com/cart/add.js', data=form_data_dict)

    # check status code
    print('Status Code: ' + str(r.status_code))
    return r.status_code

    '''# save response content which happens to be a json to json file
    with open(f'jsons/addToCart_content.json', 'w') as filehandle:
        json.dump(r.json(), filehandle, indent=2)
        print('\nSaved response content to jsons/addToCart_content.json')
    filehandle.close()'''

    '''# save res headers to json file
    with open(f'jsons/addToCart_res_headers.json', 'w') as filehandle:
        json.dump(dict(r.headers), filehandle, indent=2)
        print('\nSaved response headers to jsons/addToCart_ res_headers.json')
    filehandle.close()'''

    '''# TODO: Pass these cart cookies to the next step
    # For now lets save the cookies to json. When we put everything together in main, use a session
    cart_cookies = {
        'cart': r.cookies['cart'],
        'cart_sig': r.cookies['cart_sig'],
        'cart_ts': r.cookies['cart_ts']
    }
    with open(f'jsons/cookies.json', 'w') as filehandle:
        json.dump(dict(cart_cookies), filehandle, indent=2)
        print('\nSaved cart cookies to jsons/cookies.json')
    filehandle.close()'''

