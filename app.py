import os
import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
DATA_FILE = 'ratings.json'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@app.route('/')
def index():
    data = load_data()
    return render_template('index.html', photos=data)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'photo' not in request.files:
            return redirect(request.url)
        file = request.files['photo']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            data = load_data()
            if filename not in data:
                data[filename] = {"total": 0, "count": 0, "average": 0.0}
                save_data(data)
                
            return redirect(url_for('index'))
    return render_template('upload.html')

@app.route('/rate/<filename>/<int:score>', methods=['POST'])
def rate_photo(filename, score):
    data = load_data()
    if filename in data and 1 <= score <= 5:
        data[filename]["total"] += score
        data[filename]["count"] += 1
        data[filename]["average"] = round(data[filename]["total"] / data[filename]["count"], 1)
        save_data(data)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)