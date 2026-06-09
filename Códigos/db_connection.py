from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()


class Database_integration:
    def __init__(self, chave_nfe:str, data_nfe:str, values_list:list, estado:str, validation:bool):
        self.validation  = validation
        self.estado = estado
        self.values_list = values_list
        self.chave_nfe = chave_nfe
        self.data_nfe = data_nfe
        self.client = MongoClient(os.getenv("MONGO_URI"))
        self.db = self.client[os.getenv("database")]
        self.collection_new = self.db[os.getenv("collection_new")]
        self.collection_old = self.db[os.getenv("collection_old")]


    def insert_document_new(self):
        format_json = {
            'Nota': self.chave_nfe,
            'estado_nota': 'SP',
            'vnota': self.values_list[0],
            'vnotaibs': self.values_list[1],
            'vnotacbs': self.values_list[2],
            'vnotais': self.values_list[3],
            'vappibs': self.values_list[4],
            'vappcbs': self.values_list[5],
            'vappis': self.values_list[6],
            'status': self.validation,
            'invoice_date': self.data_nfe
        }

        self.collection_new.insert_one(format_json)

    def insert_document_old(self):
        format_json = {
            'Nota': self.chave_nfe,
            'estado_nota': self.estado,
            'vnota': self.values_list[0],
            'vsimuibs': self.values_list[1],
            'vsimucbs': self.values_list[2],
            'vsimuis': self.values_list[3],
            'invoice_date': self.data_nfe
        }
        self.collection_old.insert_one(format_json)

    def check_duplicates(self, chave_nfe, tipo_nota):
        filtro = {}

        if chave_nfe:
            filtro["Nota"] = chave_nfe

        if tipo_nota:
            resultado = list(self.collection_new.find(
                filtro,
                {"_id": 0}
            ))
            if len(resultado):
                return False

            else:
                return True

        else:
            resultado = list(self.collection_old.find(
                filtro,
                {"_id": 0}
            ))
            if len(resultado):
                return False
            else:
                return True




class init_db:
    def __init__(self):
        self.client = MongoClient(os.getenv("MONGO_URI"))
        self.db = self.client[os.getenv("database")]
        self.collection_new = self.db[os.getenv("collection_new")]
        self.collection_old = self.db[os.getenv("collection_old")]

    def get_info_from_db(self, chave_nfe):
        format_json = {}

        if chave_nfe:
            format_json["Nota"] = chave_nfe

        for collection in [self.collection_new, self.collection_old]:
            resultado = list(collection.find(
                format_json,
                {"_id": 0}
            ))

            if len(resultado):
                return resultado
            else:
                continue