import os
from flask import Flask, request, redirect, url_for, send_from_directory  
from werkzeug.utils import secure_filename
from PIL import Image
import torch 
from torchvision import transforms 

UPLOAD_FOLDER = './uploaded_images' 
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'} 

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Helper function from Flask documentation to determine if an uploaded filename 
# is an ALLOWED_EXTENSIONS file type 
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    prediction=""
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files: 
            return redirect(request.url) 
        
        file = request.files['file']
        # check if valid filename was provided 
        if file.filename == '': 
            return redirect(request.url) 
        
        # valid file upload 
        if file and allowed_file(file.filename): 
            # Save image locally for easy displaying 
            filename = secure_filename(file.filename) 
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) 
            image_url = url_for('uploaded_file', filename=filename) 
            
            # Run prediction model 
            prediction=eval(Image.open(file)) 
            labels = ["akiec (Actinic Keratoses and Bowen’s Disease)", "bcc (Basal Cell Carcinoma)", "bkl (Benign Keratosis-like Lesions)", "df (Dermatofibroma)", "mel (Melanoma)", "nv (Melanocytic nevi)", "vasc (Vascular Lesions)"] 
            
            # return template for uploaded images 
            return '''
            <h1>Classification prediction: {}<h1>
            <img src= "{}"/> 
            <h3>Upload new File</h3>
            <form method=post enctype=multipart/form-data>
            <input type=file name=file>
            <input type=submit value=Upload>
            </form>
            '''.format(labels[prediction.argmax()],image_url)

    # return template for when no image has been uploaded 
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

# Handler for uploaded files for displaying 
@app.route('/uploads/<filename>') 
def uploaded_file(filename): 
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename) 

# Classify the image using the downloaded model 
def eval(image): 
    # Load data transformer and model file using CPU only 
    data_transform = transforms.Compose([transforms.Resize((224, 224)), transforms.ToTensor()]) 
    model = torch.load('resnet18_off_prod_10epoch_pretrained_aug.pth', map_location=torch.device('cpu')) 
    model.eval() 
    image = data_transform(image).unsqueeze(0) # Transform the image 
    out = model(image) # Run the image against the model 
    return out 