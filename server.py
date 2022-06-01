import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from PIL import Image
import torch 
from torchvision import transforms 

UPLOAD_FOLDER = './uploaded_images' 
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'} 

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            print(eval(Image.open(file))) # TODO -> Capture the output and display it nicely 
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # return redirect(url_for('download_file', name=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

def eval(image): 
    # Load data transformer and model file using CPU only 
    data_transform = transforms.Compose([transforms.Resize((224, 224)), transforms.ToTensor()]) 
    model = torch.load('badresnet18.pt', map_location=torch.device('cpu')) 
    model.eval() 
    image = data_transform(image).unsqueeze(0) # Transform the image 
    out = model(image) # Run the image against the model 
    return out 