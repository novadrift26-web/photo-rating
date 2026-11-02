import os
from flask import Flask, request, jsonify
import cloudinary
import cloudinary.uploader

app = Flask(__name__)

# 配置 Cloudinary（它会自动读取你在 Vercel 里设置的密钥）
cloudinary.config(
    cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME'),
    api_key = os.environ.get('CLOUDINARY_API_KEY'),
    api_secret = os.environ.get('CLOUDINARY_API_SECRET'),
    secure = True
)

@app.route('/')
def home():
    return "Photo Rating App is running!"

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
        
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
        
    if file:
        # 直接把图片上传到云端，不会再报错了
        upload_result = cloudinary.uploader.upload(file)
        image_url = upload_result.get('secure_url')
        
        return jsonify({
            "message": "Upload success!",
            "url": image_url
        })

if __name__ == '__main__':
    app.run(debug=True)
