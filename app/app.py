from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
UPLOAD_FOLDER = '/app/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    bank_id = request.form.get('bank_id')

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and bank_id:
        # Create a folder for uploads if it does not exist
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        # Save the uploaded PDF file
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        try:
            file.save(file_path)
        except Exception as e:
            return jsonify({'error': f'Failed to save file: {str(e)}'}), 500

        # Save Bank ID to a text file in the same directory as the PDF
        bank_id_file_path = os.path.join(UPLOAD_FOLDER, 'bankid.key')
        try:
            with open(bank_id_file_path, 'w') as bank_id_file:
                bank_id_file.write(bank_id)
        except Exception as e:
            return jsonify({'error': f'Failed to write bankid.key: {str(e)}'}), 500

        return jsonify({'message': 'File uploaded and Bank ID stored successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
