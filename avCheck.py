# 1 - check availability of the item / refresh and monitor
import requests
import json


'''def availability_check(product_name):
    r = requests.get('https://funko.com/products.json')
    products = json.loads(r.text)['products']

    with open(f'jsons/products.json', 'w') as filehandle:
        json.dump(products, filehandle, indent=2)
        print('\nSaved products json to jsons/products.json')
    filehandle.close()

    for product in products:
        print("title: ", product['title'])

        if product['title'] == product_name:
            print("variant id: ", product['variants'][0]['id'])
            print("available: ", product['variants'][0]['available'])
            if product['variants'][0]['available']:
                return product['variants'][0]['id']

            # producturl = 'https://figpin.com/products/' + product['handle']
            # return producturl

    return False


print(availability_check())'''

r = requests.get('https://funko.com/products.json')
print(r.status_code)
print(r.text)

'''with open(f'jsons/products.json', 'w') as filehandle:
    json.dump(products, filehandle, indent=2)
    print('\nSaved products json to jsons/products.json')
filehandle.close()'''
