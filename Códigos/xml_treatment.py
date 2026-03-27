import xml.etree.ElementTree as ET
from calTributos import CalTributos
import os
#apenas para developer, depois o caminho vai dar pela tela do tkinter
caminho = os.getcwd()

class Xml_Treatment:
    def __init__(self, path):
        self.path = path
        self.root = self._xml_tree()
        self.ns = {"nfe": "http://www.portalfiscal.inf.br/nfe"}
        self.state = self._state()

    @property
    def return_string_invoice(self):
        with open(self.path, "r", encoding="utf-8") as f:
            conteudo = f.read()
        return conteudo

    @property
    def return_elements_taxes(self):
        if self._isnew_invoice():
            return self._return_values_new_inv()
        else:
            return self._return_values_old_inv()
# ______________________________________________________________________________________________________________________
# Funções de análise de classe, não usar métodos

    def _isnew_invoice(self):
        root = self._xml_tree()
        # os valores de ibs e cbs estão dentro da mesma tag IBCCBSTot
        ibs_cbs = root.findall(".//nfe:IBSCBSTot", self.ns)

        # is_imposto = root.findall(".//nfe:IS", self.ns) esta dando erro quando a nota n tem mas ela é valida (validar)

        #define lógica se é nota nova ou não
        if len(ibs_cbs):
            return True
        return False

    def _xml_tree(self):
        tree = ET.parse(self.path)
        root = tree.getroot()
        return root

    def _return_values_old_inv(self):
        valores_impostos = {
            'BASE_CALC': None,
        }
        #desenvolver lógica para notas antigas

        return valores_impostos

    def _return_values_new_inv(self):
        valores_impostos = {
            'BASE_CALC': None,
            'IBS': None,
            'CBS': None,
            'IS': None,

        }
        tag_base_calculo = self.root.find(".//nfe:ICMSTot", self.ns)
        tag_ibs = self.root.find(".//nfe:IBSCBSTot", self.ns).find('nfe:gIBS', self.ns)
        tag_cbs = self.root.find(".//nfe:IBSCBSTot", self.ns).find('nfe:gCBS', self.ns)
        tag_is = self.root.find(".//nfe:ISTot", self.ns)

        if tag_base_calculo is not None:
            vbc = tag_base_calculo.find("nfe:vBC", self.ns)
        else:
            vbc = None

        if tag_ibs is not None:
            vibs = tag_ibs.find('nfe:vIBS', self.ns)
        else:
            vibs = None

        if tag_cbs is not None:
            vcbs = tag_cbs.find("nfe:vCBS", self.ns)
        else:
            vcbs = None

        if tag_is is not None:
            vis = tag_is.find("nfe:vIS", self.ns)
        else:
            vis = None

        valores_impostos['BASE_CALC'] = self.get_float(vbc)
        valores_impostos['IBS'] = self.get_float(vibs)
        valores_impostos['CBS'] = self.get_float(vcbs)
        valores_impostos['IS'] = self.get_float(vis)
        return valores_impostos

    def _state(self):
        estado_nota = self.root.find(".//nfe:emit", self.ns).find('nfe:enderEmit', self.ns).find('nfe:UF', self.ns).text
        return estado_nota if estado_nota else 0

    @staticmethod
    def get_float(tag):
        return float(tag.text) if tag is not None else 0.0

if __name__ == "__main__":
    # rodar em loop de acordo com o numero de notas
    cont = 0
    for i in os.listdir(f'{caminho.split('Códigos')[0]}\\Notas\\'):
        caminho_nota = f'{caminho.split('Códigos')[0]}\\Notas\\{i}'
        # inicia a classe e pega os valores presentes na nota
        resultado = Xml_Treatment(caminho_nota)
        valores_notas = resultado.return_elements_taxes
        estado = resultado.state
        # chama a classe de calcular o tributo
        cal_trib = CalTributos(estado, valores_notas['BASE_CALC'])
        print(f'Valores da nota {cont + 1} do estado de {estado}: \n{valores_notas}\n\nValor dos impostos\n{cal_trib.calcular_json()}\n')
        cont +=1
