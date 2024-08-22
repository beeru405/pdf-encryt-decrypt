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
        # Create the upload folder if it does not exist
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        # Save Bank ID to a text file named bankid.txt
        bank_id_file_path = os.path.join(UPLOAD_FOLDER, 'bankid.txt')
        try:
            with open(bank_id_file_path, 'w') as bank_id_file:
                bank_id_file.write(bank_id)
        except Exception as e:
            return jsonify({'error': f'Failed to write bankid.txt: {str(e)}'}), 500

        # Check if the key file exists
        key_file_path = os.path.join(UPLOAD_FOLDER, f'{bank_id}.key')
        if not os.path.exists(key_file_path):
            return jsonify({'error': 'Key file not found'}), 404

        # Save the uploaded PDF file
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        try:
            file.save(file_path)
        except Exception as e:
            return jsonify({'error': f'Failed to save file: {str(e)}'}), 500

        return jsonify({'message': 'File uploaded, Bank ID stored, and key file validated successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
