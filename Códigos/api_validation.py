import requests
from json import loads

class Api_validation:
    def __init__(self, xml_string: str = None, invoice_price: float = None):
        self.xml = xml_string
        self.api_parameters()
        self._xmlvalidate()
        # self._cotacaovalidate(invoice_price)

    def api_parameters(self):
        self.dict_parameters = {
            'url': 'https://piloto-cbs.tributos.gov.br/servico/calculadora-consumo/api/calculadora/xml/validate?tipo=nfe&subtipo=NOTA',
            'method': 'POST',
            'headers': {
                      "Accept": "application/json, text/plain, */*",
                      "Content-Type": "application/xml",
                      "Origin": "https://piloto-cbs.tributos.gov.br",
                      "Referer": "https://piloto-cbs.tributos.gov.br/servico/calculadora-consumo/calculadora/validador-xml"
                    },
            'xml': self.xml
        }

    def _xmlvalidate(self):
        try:
            response = requests.request(self.dict_parameters['method'], self.dict_parameters['url'], headers=self.dict_parameters['headers'], data=self.dict_parameters['xml'])
            if response.status_code == 200:
                self.status_code = response.status_code
                self.response = 'Sucesso na Validação'
            else:
                self.response = loads(response.text)['detail']
                self.status_code = response.status_code


        except Exception as e:
            self.response = 'Erro no except:\n'+ str(e)

    def _cotacaovalidate(self, invoice_price):
        url = "https://api-xml-scan.vercel.app"

        payload = {
            "user": "admin",
            "senha": "admin",
            "preco": float(invoice_price)
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