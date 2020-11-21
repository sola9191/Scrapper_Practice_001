import os
import requests
from bs4 import BeautifulSoup
from babel.numbers import format_currency

os.system("clear")

"""
Use the 'format_currency' function to format the output of the conversion
format_currency(AMOUNT, CURRENCY_CODE, locale="ko_KR" (no need to change this one))
"""

url = "https://www.iban.com/currency-codes"



countries = []
request = requests.get(url)
soup = BeautifulSoup(request.text, "html.parser")

table = soup.find("table")
tbody = soup.find("tbody")
rows = tbody.find_all("tr")

for row in rows:
  country = row.find_all("td")
  country_name = country[0].text
  country_code = country[2].text

  countries.append(
    {
     "country_name" : country_name.capitalize(), 
     "country_code" : country_code 
    }
  )
print("Welcome to CurrencyConvert PRO 2000 ")
for index, country in enumerate(countries):
  print(f"# {index} {country['country_name']}")


def ask_con():
  while True:
    print("Where are you from? Choose a country by number")
    nationality = input("#: ")
    try:
      nationality = int(nationality)
      if nationality>=0 and nationality < len(countries):
        m_country = countries[nationality]
        print(m_country['country_name'])
        print("Now choose another country.")
        another_country = input("#: ")
        try:
          another_country = int(another_country)
          if another_country>=0 and another_country < len(countries):
            a_country = countries[another_country]
            print(a_country['country_name'])
            print(f"How many {m_country['country_code']} do you want to cover to {a_country['country_code']}")
            try:
              amount = int(input("#: ")) # 여기서 숫자 입력안하면 걸러야함
            
              return get_result(m_country['country_code'], a_country['country_code'], amount)
            except:
              print("That isn't number")   
          else:
            print("this number is out of range")
        except ValueError:
          if '.' in another_country:
            print("You can use only integer.")
          else:
            print("That isn't number") 
      else:
        print("this number is out of range")
    except ValueError:
      if '.' in nationality:
        print("You can use only integer.")
      else:
        print("That isn't number")

def get_result(m_country, a_country, amount):
  
  url=f"https://transferwise.com/gb/currency-converter/{m_country}-to-{a_country}-rate?amount={amount}"
  request = requests.get(url)
  print(request) #200 뜨나 확인용
  if request.status_code==200:
    soup = BeautifulSoup(request.text, "html.parser")
    div = soup.find("h3", {"class":"cc__source-to-target"})
    rate = div.find_all("span")[2].text
    con_after = float(rate) * float(amount)
    add_cur_amount = format_currency(amount, m_country , locale="ko_KR")

    add_cur_con_after = format_currency(con_after, a_country , locale="ko_KR")
    print(f"{add_cur_amount} is {add_cur_con_after}")
  else:
    print("There is no information")
  

ask_con()