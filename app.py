import os
from flask import Flask, request, jsonify
import cloudinary
import cloudinary.uploader

app = Flask(__name__)

# 配置 Cloudinary 雲端存儲
cloudinary.config(
    cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME'),
    api_key = os.environ.get('CLOUDINARY_API_KEY'),
    api_secret = os.environ.get('CLOUDINARY_API_SECRET'),
    secure = True
)

@app.route('/')
def home():
    return "Photo Rating App is running successfully!"

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
        
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
        
    if file:
        upload_result = cloudinary.uploader.upload(file)
        image_url = upload_result.get('secure_url')
        
        return jsonify({
            "message": "Upload success!",
            "url": image_url
        })

if __name__ == '__main__':
    app.run(debug=True)
