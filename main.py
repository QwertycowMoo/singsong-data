from flask import Flask
from flask import request
from flask import make_response
from werkzeug.utils import secure_filename
from flask_cors import CORS
from firebase_admin import credentials, initialize_app, storage

creds = credentials.Certificate("./singsong-key.json")
initialize_app(creds,  {'storageBucket': 'singsong-data'})

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/postAudio", methods=['POST'])
def postAudio():
    # TODO: Convert from OGG to WAV, preferably in here to not have to do it after getting the data from Cloud Storage
    # Use FFMpeg - need to download to this computer
    # try:
        filename = request.args.get("filename")
        filename = secure_filename(filename) + ".ogg"
        file = request.files["file"]

        # file.save(filename)
        bucket = storage.bucket()
        destination = bucket.blob("audiofiles/" + filename)
        destination.upload_from_file(file)
        return "saved " + filename + " to storage"
    # except:
    #     return 500, "Server Error"

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)