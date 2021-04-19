from flask import Flask
from flask import render_template, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

import os
import requests
import time

from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions, MobileNetV2

UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "secret key"

inference_model = MobileNetV2()

def getPrediction(filename):
    image = load_img('static/uploads/' + filename, target_size=(224, 224))
    image = img_to_array(image)
    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
    image = preprocess_input(image)

    all_result = inference_model.predict(image)
    result = decode_predictions(all_result)[0]
    result = [(img_class, label, str(round(acc * 100, 4)) + '%') for img_class, label, acc in result]
    return result

def get_instance_info():
    try:
        public_ip = requests.get("http://169.254.169.254/latest/meta-data/public-ipv4", timeout=2).text
        instance_id = requests.get("http://169.254.169.254/latest/meta-data/instance-id", timeout=2).text
        instance_type = requests.get("http://169.254.169.254/latest/meta-data/instance-type", timeout=2).text
        region = requests.get("http://169.254.169.254/latest/meta-data/placement/region", timeout=2).text
        avail_zone = requests.get("http://169.254.169.254/latest/meta-data/placement/availability-zone", timeout=2).text

        for info in [public_ip, instance_id, instance_type, avail_zone]:
            flash(info)
    except:
        for i in range(4):
            flash('Error')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    for i in range(10):
        flash('')
    get_instance_info()
    return render_template('index.html')

@app.route('/', methods=['POST'])
def submit_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            result = getPrediction(filename)
            for top_result in result:
                flash(top_result[1])
                flash(top_result[2])
            get_instance_info()
            return render_template('index.html', filename=filename)
        else:
            flash('Allowed image types are -> png, jpg, jpeg, gif')
            return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
	return redirect(url_for('static', filename='uploads/' + filename), code=301)
        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80 ,debug=True)
