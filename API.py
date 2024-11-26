import requests

# Базовая ссылка, вместе с токеном
# Поскольку использование не бесконечное, может получиться что токен не работает, тогда нужно предоставить свой
base_url = 'https://v6.exchangerate-api.com/v6/486048c3e01702ebc4efbd29/'


# Выдает список списков всех поддерживаемых валют
# Список имеет формат [0] - код валюты [1] - имя валюты
# Пример [["USD","United States Dollar"],["ZWL","Zimbabwean Dollar"]]
def get_codes():
    response = requests.get(base_url + 'codes')
    data = response.json()
    if data['result'] == 'success':
        return data['supported_codes']
    else:
        return False


# Выдает курс для выданной валюты по сравнению со всей другой валютой
# Курс выдан в формате словаря, где первое это код валюты и второе это сколько будет если перевести 1 переданную валюту
# Пример передав USD {"USD":1,"AED":3.6725, "AFN":68.0851}
def get_rates(currency):
    response = requests.get(base_url + 'latest/' + currency)
    data = response.json()
    if data['result'] == 'success':
        return data['conversion_rates']
    else:
        return False
