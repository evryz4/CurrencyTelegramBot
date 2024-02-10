import requests
import asyncio
from bs4 import BeautifulSoup as bs

urls = {'usd': 'https://currency.me.uk/convert/usd/rub',
        'eur': 'https://currency.me.uk/convert/eur/rub'}

class Currency:
    def __new__(cls, *args, **kwargs):
        ret = super().__new__(cls)
        asyncio.run(ret.update())
        return ret
    
    def get(self) -> tuple[str: float]:
        return self.rates

    async def update(self) -> None:
        rates = {}
        for url in urls:
            r = requests.get(urls[url])
            soup = bs(r.text, 'lxml')
            curs = soup.find('span', {'class' : 'mini ccyrate'}).text
            rate = curs[curs.find('=')+2:-(curs[::-1].find(' '))-1]
            rates[url] = float(rate)
        self.rates = rates