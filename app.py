import io
import os
import PySimpleGUI as sg
from PIL import Image
import torch 
from torchvision import transforms 

# A list of supported file types for the file browser (not supported on OSX) 
file_types = [("JPEG (*.jpg)", "*.jpg"), ("PNG (*.png)", "*.png")]

# Set UI Theme 
sg.theme('Reddit') 

def main():
    curImage = None # the current image variable being evaluated on 

    # create main window layout 
    layout = [
        [sg.Image(key="IMAGEKEY")], # unique key to reference image 
        [
            sg.Input(size=(30, 1), key="FILEKEY"), # unique key to reference file path 
            sg.FileBrowse(file_types=file_types), 
            sg.Button("Load Image"), 
            sg.Button("Run Model"), 
        ],
    ]
    window = sg.Window("ECS 171 Group 5 Project", layout, size=(500, 500)) # create main window 
    
    onboarding() # call onboarding modal 
    
    while True: # event-listener 
        event, values = window.read() 
        if event == "Exit" or event == sg.WIN_CLOSED: # Kill Program 
            break
        if event == "Load Image": # Load Image 
            filename = values["FILEKEY"]
            if os.path.exists(filename):
                image = Image.open(values["FILEKEY"])
                curImage = image 
                image.thumbnail((400, 400))
                bio = io.BytesIO()
                image.save(bio, format="PNG")
                window["IMAGEKEY"].update(data=bio.getvalue())
        if event == "Run Model" and curImage != None: # Run model if image is selected 
            eval_popup(eval(curImage)) 
    window.close()

def onboarding():
    layout = [
        [sg.Text('Welcome to Group 5\'s ECS 171 Project!\n\nTo run our demo, you can upload one of the 5 pre-selected images under the images folder, or upload an image of your own! All major file types are supported.\n\nUpon seeing your image successfully uploaded, you can then press the "Run" button to have your image classified and see basic statistics relative to our classifications!')], 
        [sg.Push(), sg.Button('OK')],
    ]
    sg.Window('ECS 171 Group Project', layout, modal=True).read(close=True) 

def eval_popup(res): 
    labels = ["akiec", "bcc", "bkl", "df", "mel", "nv", "vasc"] 
    
    layout = [ 
        # [sg.Text('Your image has been classified as: ' + str(res.argmax()))], 
        [sg.Text(f'Classification Prediction: {labels[res.argmax()]}')], 
        [sg.Text(f'\nClassification Probabilities:')], 
        [sg.Text(f'akiec: {res[0][0].item():.2f}')],
        [sg.Text(f'bcc: {res[0][1].item():.2f}')],
        [sg.Text(f'bkl: {res[0][2].item():.2f}')],
        [sg.Text(f'df: {res[0][3].item():.2f}')],
        [sg.Text(f'mel: {res[0][4].item():.2f}')],
        [sg.Text(f'nv: {res[0][5].item():.2f}')],
        [sg.Text(f'vasc: {res[0][6].item():.2f}')],
        [sg.Push(), sg.Button('OK')], 
    ] 
    sg.Window('Image Classification', layout, modal=True).read(close=True) 

def eval(image): 
    # Load data transformer and model file using CPU only 
    data_transform = transforms.Compose([transforms.Resize((224, 224)), transforms.ToTensor()]) 
    model = torch.load('badresnet18.pt', map_location=torch.device('cpu')) 
    model.eval() 
    image = data_transform(image).unsqueeze(0) # Transform the image 
    out = model(image) # Run the image against the model 
    return out 

if __name__ == "__main__":
    main()
