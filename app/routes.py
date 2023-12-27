from flask import Flask,  request, jsonify, send_file, send_from_directory
from app.pdf_parser.pdf import process_pdf
from werkzeug.utils import secure_filename 
from flask_cors import CORS
import os
from app.utils import handle_month_year

app = Flask(__name__)
cors = CORS(app, origins="*")

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

script_dir = os.path.dirname(os.path.abspath(__file__))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'


@app.route('/', methods=['GET'])
def processar_pdf():
    dados_faturas = []

    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        try:
            dados_extraidos = process_pdf(filepath)
            dados_faturas.append(dados_extraidos)
        except Exception as e:
            pass

    return jsonify(dados_faturas)


@app.route('/download', methods=['POST'])
def download():
    month = request.json.get('billMonth')
    num_client = request.json.get('installationNumber')

    if not month or not num_client:
        return 'Parâmetros "billMonth" e "customerNumber" são obrigatórios', 400
    
    month, year = handle_month_year(month)
    
    pdf_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'uploads')
    filename = f"{num_client}-{month}-{year}.pdf"

    file_path = os.path.join(pdf_folder, filename)
    try:
        if not os.path.exists(file_path):
            return f'Arquivo "{filename}" não encontrado', 404

        return send_from_directory(pdf_folder, filename)
    except Exception as e:
        return f'Erro ao processar o arquivo: {str(e)}', 500


   