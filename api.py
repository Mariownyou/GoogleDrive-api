from flask import Flask
from app import DriveApi

app = Flask(__name__)
drive = DriveApi()

@app.route('/')
def hello_world():
    files = drive.get_all('projects')
    print(files)
    return files[0]

@app.route('/api/<folder>')
def folder(folder):
    files = drive.get_all(folder)
    if len(files) == 0:
        return '<h1>Empty folder</h1>'
    return f'<pre>{files}</pre>'

if __name__ == '__main__':
    app.run()