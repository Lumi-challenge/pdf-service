from PyPDF2 import PdfReader
import re

def process_pdf(pdf_path):
    with open(pdf_path, "rb") as pdf_file:
        pdf_reader = PdfReader(pdf_file)
        num_pages = len(pdf_reader.pages)
        result = {}
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            match_num_cliente_instalacao = re.search(r"Nº DA INSTALAÇÃO(.+?)Referente a", text, re.DOTALL)
            if match_num_cliente_instalacao:
                numero_cliente_instalacao_text = list(filter(lambda x: x != "", match_num_cliente_instalacao.group(1).strip().split(" ")))
                result['customerNumber'] = numero_cliente_instalacao_text[0]
                result['installationNumber'] = numero_cliente_instalacao_text[1]

            match_mes_referencia = re.search(r"\b[A-Z]{3}/\d{4}\b", text)
            if(match_mes_referencia):
                result['billMonth'] = match_mes_referencia.group()

            match_energia_eletrica = re.search(r"Energia Elétrica kWh(.+?)Energia SCEE s/ ICMS kWh ", text, re.DOTALL)
            if match_energia_eletrica:
                match_energia_eletrica_text = list(filter(lambda x: x != "", match_energia_eletrica.group(1).strip().split(" ")))
                result['energyQuantityKWh'] = float(match_energia_eletrica_text[0].replace(".", "").replace(",", "."))
                result['energyValue'] = float(match_energia_eletrica_text[2].replace(".", "").replace(",", "."))
                
            match_energia_scee = re.search(r"Energia SCEE s/ ICMS kWh (.+?)Energia compensada GD I kWh", text, re.DOTALL)
            if match_energia_scee:
                match_energia_scee_text = list(filter(lambda x: x != "", match_energia_scee.group(1).strip().split(" ")))
                result['energySCEEEWithoutICMSQuantityKWh'] = float(match_energia_scee_text[0].replace(".", "").replace(",", "."))
                result['energySCEEEWithoutICMSValue'] = float(match_energia_scee_text[2].replace(".", "").replace(",", "."))
                
            match_energia_compensada = re.search(r"Energia compensada GD I kWh(.+?)Contrib Ilum Publica Municipal", text, re.DOTALL)
            if match_energia_compensada:
                match_energia_compensada_text = list(filter(lambda x: x != "", match_energia_compensada.group(1).strip().split(" ")))
                result['compensatedEnergyGDIQuantityKWh'] = float(match_energia_compensada_text[0].replace(".", "").replace(",", "."))
                result['compensatedEnergyGDIValue'] = float(match_energia_compensada_text[2].replace(".", "").replace(",", "."))
                
            match_ilu_public = re.search(r"Contrib Ilum Publica Municipal(.+?)TOTAL", text, re.DOTALL)
            if match_ilu_public:
                match_ilu_public_text = list(filter(lambda x: x != "", match_ilu_public.group(1).strip().split(" ")))
                result['municipalPublicLightingContribution'] = float(match_ilu_public_text[0].replace(".", "").replace(",", "."))

            return result
