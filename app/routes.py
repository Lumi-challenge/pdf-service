from flask import Flask,  request, jsonify
from app.pdf_parser.pdf import process_pdf
from werkzeug.utils import secure_filename 
from flask_cors import CORS
import os

app = Flask(__name__)
ors = CORS(app, origins="*")

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
