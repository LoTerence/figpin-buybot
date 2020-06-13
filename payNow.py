# 3d - pay now - post credit card info and billing address

# for clicking on the pay now button and submitting the final request
# input credit card info and billing address

import requests
import json
from bs4 import BeautifulSoup

# read cookies.json to get cookies
with open('jsons/cookies.json', 'r') as f:
    cookies = json.load(f)

# get the data for inputting into the form (credit card info, billing address)
with open('formData.json', 'r') as f:
    formData = json.load(f)


# var for storing the url of the shipping page get request:
payment_url = cookies['paymentURL']
payment_path = payment_url[18:]  # remove the first 18 chars(https://figpin.com) of the url to get the path
print(payment_path)

# TODO get the res checkout cookies
# request headers for the get request for shipping html page
req_headers1 = {
    "authority": "figpin.com",
    "method": "GET",
    "path": payment_path,
    "scheme": "https",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "no-cache",
    "cookie": "checkout=eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaEpJaVZtWVRnMVltWTRNak14TVdSallUVTROMlV5TURVeU5qWXdPR1ppTXpnMU1BWTZCa1ZVIiwiZXhwIjoiMjAyMC0wNi0xOFQwMDoyMToyNS43MzhaIiwicHVyIjoiY29va2llLmNoZWNrb3V0In19--b73e0a7068b3eeaf41351e5f6a479a270e40a637; "
              "tracked_start_checkout=75fb2d200554845faccbb52b28cdc69b; "
              "checkout_token=eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaEpJaVUzTldaaU1tUXlNREExTlRRNE5EVm1ZV05qWW1JMU1tSXlPR05rWXpZNVlnWTZCa1ZVIiwiZXhwIjoiMjAyMS0wNS0yOFQwMDoyMToyNS43MzlaIiwicHVyIjoiY29va2llLmNoZWNrb3V0X3Rva2VuIn19--40f97d1827490a1afffe4831d4404c64ea248fb0; "
              "cart_currency=USD; "
              "cart=1ce104339fdcc7ddf142a4f9743626c3; "
              "cart_sig=b34ab38aafe7ea3ccc7336576666abea; "
              "secure_customer_sig=; "
              "cart_ts=1590624365; "
              "_orig_referrer=https%3A%2F%2Ffigpin.com%2Fcart; "
              "_secure_session_id=d33aeca66b7443cd8bc705155f2c4912; "
              "_landing_page=%2F5443715170%2Fcheckouts%2F75fb2d200554845faccbb52b28cdc69b ",
    "pragma": "no-cache",
    "referer": "https://figpin.com/",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
}