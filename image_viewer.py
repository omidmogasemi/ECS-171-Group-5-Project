# image_viewer.py
import io
import os
import PySimpleGUI as sg
from PIL import Image
file_types = [("JPEG (*.jpg)", "*.jpg"),
              ("All files (*.*)", "*.*")]
def main():
    layout = [
        [sg.Image(key="-IMAGE-")],
        [
            sg.Text("Image File"),
            sg.Input(size=(25, 1), key="-FILE-"),
            sg.FileBrowse(file_types=file_types),
            sg.Button("Load Image"),
            sg.Button("Run Model on loaded Image"),
        ],
    ]
    window = sg.Window("Image Viewer", layout)
    [sg.popup_no_wait('Welcome!')] 
    sg.popup_ok('Welcome to Group 5\'s ECS 171 Project!\n To run our demo, you can upload one of the 5 pre-selected images under the images folder, or upload an image of your own! All major file types are supported.\n Upon seeing your image successfully uploaded, you can then press the "Run" button to have your image classified and see basic statistics relative to our classifications!')  # Shows OK button
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "Load Image":
            filename = values["-FILE-"]
            if os.path.exists(filename):
                image = Image.open(values["-FILE-"])
                image.thumbnail((400, 400))
                bio = io.BytesIO()
                image.save(bio, format="PNG")
                window["-IMAGE-"].update(data=bio.getvalue())
        if event == "Run Model on loaded Image":
            sg.popup_ok("the answer is ", add(2,3))
    window.close()

def add(x,y):
    print(x+y)
    return x+y

if __name__ == "__main__":
    main()
