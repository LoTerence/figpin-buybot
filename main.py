# shopify buy bot
# for buying funkos and figpin drops

"""needs to do 4 things in order:
1. check for availability (shopify monitor
2. add to cart
3. check out cart
4. check if buy was successful"""

import sys
import requests
import avCheck as av
import addToCart as atc
import buyProduct as bp

productName = "Dabi (#241)"

# variantID will either be a string representing the id if availability_check is successful, or it will be boolean False
variantId = av.availability_check(productName)

if not variantId:
    sys.exit(productName + " is not available / does not exist")

# make a request session
s = requests.Session()

# add to cart
status_code = atc.add_to_cart(variantId, s)

if status_code != 200:
    sys.exit("Add to cart failed")

# checkout cart and pay
bp.buy(s)






