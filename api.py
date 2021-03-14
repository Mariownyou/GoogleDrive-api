from flask import Flask, request
from drive_api import DriveApi

app = Flask(__name__)
app.debug = False 
drive = DriveApi()

@app.route('/')
def hello_world():
    files = drive.get_all('projects')
    print(files)
    return files[0]

@app.route('/<folder>', methods = ['GET', 'POST', 'PUT'])
def folder(folder):
    if request.method == 'GET':
        files = drive.get_all(folder)
        if len(files) == 0:
            return '<h1>Empty folder</h1>'
        return f'<pre>{files}</pre>'
    if request.method == 'POST':
        img = request.files.get('image')
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
        files = drive.create([img_obj, json_obj], folder)
        return files

@app.route('/file/<id>', methods = ['GET', 'DELETE', 'PUT'])
def get(id):
    if request.method == 'GET':
        files = drive.get(id)
        return files
    if request.method == 'DELETE':
        return 'Delete'
    if request.method == 'PUT':
        folder_id = id
        img = request.files.get('image')
        json = request.files.get('json')

        img_bytes = img.read() if img else None
        json_bytes = json.read() if json else None
        if json is None and img is not None:
            data = {
                'image': img_bytes
            }
        if json is not None and img is None:
            data = {
                'json': json_bytes
            }
        if json is not None and img is not None:
            data = {
                'image': img_bytes,
                'json': json_bytes
            }

        files = drive.update(data, folder_id)
        return files



if __name__ == '__main__':
    if app.debug == True:
        app.run()