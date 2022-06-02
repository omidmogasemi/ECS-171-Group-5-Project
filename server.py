import os
from flask import Flask, render_template, request 
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
    res = "Not calculated" # Return no calculation if no image was properly uploadedm 
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return render_template('index.html', res=res) 
        
        file = request.files['file'] # extract file from request 
        # If no file submitted (and thus a default empty string) 
        if file.filename == '':
            return render_template('index.html', res=res) 
        
        # Properly uploaded file 
        if file and allowed_file(file.filename): 
            res = eval(Image.open(file)) 
    
    return render_template('index.html', res=res) 

# Classify the image using the downloaded model 
def eval(image): 
    # Load data transformer and model file using CPU only 
    data_transform = transforms.Compose([transforms.Resize((224, 224)), transforms.ToTensor()]) 
    model = torch.load('badresnet18.pt', map_location=torch.device('cpu')) 
    model.eval() 
    image = data_transform(image).unsqueeze(0) # Transform the image 
    out = model(image) # Run the image against the model 
    
    # Assign the class label with the highest probability argument 
    labels = ["akiec (Actinic Keratoses and Bowen’s Disease)", "bcc (Basal Cell Carcinoma)", "bkl (Benign Keratosis-like Lesions)", "df (Dermatofibroma)", "mel (Melanoma)", "nv (Melanocytic nevi)", "vasc (Vascular Lesions)"] 
    return labels[out.argmax()] 