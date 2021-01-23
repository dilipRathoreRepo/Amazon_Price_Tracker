import requests
from bs4 import BeautifulSoup
import smtplib

URL = "https://www.amazon.com.au/Ghost-of-Tsushima-PlayStation-4/dp/B0848TGCRP/ref=sr_1_1?crid=2PGC4LYE1WNGA&dchild=1&keywords=ghost+of+tsushima&qid=1611364462&s=videogames&sprefix=ghost+of%2Caps%2C359&sr=1-1"
header = {"Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
          "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"}

response = requests.get(URL, headers=header)

soup = BeautifulSoup(response.content, "lxml")

data = soup.find(name="span", class_="a-size-medium a-color-price priceBlockBuyingPriceString")
price = data.getText()
price_without_dollar = float(price.replace("$", ""))
print(price_without_dollar)

# Send email
title = soup.find(id="productTitle").get_text().strip()
print(title)

BUY_PRICE = 40
if price_without_dollar < BUY_PRICE:
    message = f'Price of {title} is {price_without_dollar} which is lower than {BUY_PRICE}'

    SMTP_ADDRESS = "smtp.gmail.com"
    EMAIL_ADDRESS = "<EMAIL_ADDRESS>"
    EMAIL_PASSWORD = "<EMAIL_PASSWORD>"
    SMTP_PORT = 587

    with smtplib.SMTP(SMTP_ADDRESS, port=SMTP_PORT) as connection:
        connection.starttls()
        result = connection.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        connection.sendmail(
            from_addr=EMAIL_ADDRESS,
            to_addrs=EMAIL_ADDRESS,
            msg=f'Subject:Amazon Price Alert!\n\n{message}\n{URL}'
        )

