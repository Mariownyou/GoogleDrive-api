from flask import Flask, request
from drive_api import DriveApi

app = Flask(__name__)
app.debug = True 
drive = DriveApi()

@app.route('/')
def hello_world():
    files = drive.get_all('projects')
    print(files)
    return files[0]

@app.route('/<folder>', methods = ['GET', 'POST'])
def folder(folder):
    if request.method == 'GET':
        files = drive.get_all(folder)
        if len(files) == 0:
            return '<h1>Empty folder</h1>'
        return f'<pre>{files}</pre>'
    if request.method == 'POST':
        img = request.files.get('img')
        json = request.files.get('json')
        img_bytes = img.read()
        json_bytes = json.read()

        img_obj = {
            'file': img_bytes,
            'mimeType': 'image/jpeg'
        }
        json_obj = {
            'file': json_bytes,
            'mimeType': 'application/json'
        }
        drive.create([img_obj, json_obj], folder)
        return 'Post'

@app.route('/file/<id>', methods = ['GET', 'DELETE'])
def get(id):
    if request.method == 'GET':
        files = drive.get(id)
        return files
    if request.method == 'DELETE':
        return 'Delete'

if __name__ == '__main__':
    if app.debug == True:
        app.run()