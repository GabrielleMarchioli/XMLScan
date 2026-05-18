import requests
from json import loads

class Api_cotacao:
    def __init__(self, invoice_price: float = None):
        self.invoice_price = invoice_price
        self._cotacaovalidate()


    def _cotacaovalidate(self):
        url = "https://api-xml-scan.vercel.app"

        payload = {
            "user": "admin",
            "senha": "admin",
            "preco": float(self.invoice_price)
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                self.status_code = response.status_code
                self.response = loads(response.text)
            else:
                self.response = loads(response.text)['mensagem']
                self.status_code = response.status_code

        except Exception as e:
            self.response = 'Erro no except:\n'+ str(e)