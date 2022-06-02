# Introduction 
Welcome to the repository for Group 5's ECS 171 assignment. This repository contains a Flask server capable of running and demonstrating our model. 

To use it, simply follow the Setup instructions below. Once your application is running, you can upload any image of a skin lesion to have it classified. There are 5 sample images for your use located in the `test_images` folder. Any images you upload will subsequently be placed into the `uploaded_images` folder for Flask's processing. 

## Setup 
1. To install the necessary packages uses in `server.py`, run the following command in the root directory of this project: `conda create --name <env> --file requirements.txt`, where `<env>` is your desired name of the environment. 
2. Run `conda activate <env>` to activate this environment. 
3. Run `export FLASK_APP=server` to set the environment variable `FLASK_APP` to `server.py`. 
4. Run `flask run` to start the server. 
5. Navigate to `http://127.0.0.1:5000/` in your browser. 
