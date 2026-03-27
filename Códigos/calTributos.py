class CalTributos:

    def __init__(self, estado, valor_prod):
        self.estado = estado
        self.valor_prod = valor_prod
        self.aliquotas = self.valor_es(estado)

    def valor_cbs(self):
        if not self.aliquotas:
            return 0
        return self.valor_prod * self.aliquotas['CBS']

    def valor_ibs(self):
        if not self.aliquotas:
            return 0
        return self.valor_prod * self.aliquotas['IBS']

    def valor_is(self):
        if not self.aliquotas:
            return 0
        return self.valor_prod * self.aliquotas['IS']

    def calcular_json(self):

        cbs = self.valor_cbs()
        ibs = self.valor_ibs()
        is_ = self.valor_is()

        total = cbs + ibs + is_

        resultado = {
            "estado": self.estado,
            "base_calculo": self.valor_prod,
            "CBS": round(cbs, 2),
            "IBS": round(ibs, 2),
            "IS": round(is_, 2),
            "total_impostos": round(total, 2)
        }

        return resultado

    @staticmethod
    def valor_es(estado):
        dict_imp_estado = {
            'SP': {'IBS': 0.0177, 'CBS': 0.0088, 'IS': 0.020},
            'RJ': {'IBS': 0.018, 'CBS': 0.0088, 'IS': 0.020}
        }
        return dict_imp_estado.get(estado)