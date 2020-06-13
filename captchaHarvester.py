import harvester
from harvester import CaptchaKindEnum, BrowserEnum
from threading import Thread, Timer
import logging

# programmatic example showing how to access the harvester api from
# within your own script without having to use the fetch module


def get_captcha_token():

    # setup defaults
    server_address = ('127.0.0.1', 5000)
    domain = 'figpin.com'
    sitekey = '6LeoeSkTAAAAAA9rkZs5oS82l69OEYjKRZAiKdaF'

    # silence server logs
    logging.getLogger('harvester').setLevel(logging.CRITICAL)

    # run the server in a separate thread to keep from
    # blocking the rest of the program
    server_thread = Thread(target=harvester.server.start,
                           args=(server_address, domain,
                                 CaptchaKindEnum.RECAPTCHA, sitekey),
                           daemon=True)
    server_thread.start()

    # launch a browser instance where we can solve the captchas
    harvester.browser.launch(domain, server_address, BrowserEnum.CHROME)

    token = ""

    try:
        while True:
            # block until we get sent a captcha token and repeat
            token = harvester.tokens.get()
            print('we just received a token:', token)
    except KeyboardInterrupt:
        # print("Something went wrong with the captcha harvester")
        print("Ended captcha harvesting")

    return token

