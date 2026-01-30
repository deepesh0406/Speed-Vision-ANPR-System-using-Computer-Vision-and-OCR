from flask import Flask, render_template, send_from_directory, url_for
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
from threading import Thread
import os, time, secrets, schedule

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(24)
app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'

def cleanup_uploads():
    if not os.path.exists(app.config['UPLOADED_PHOTOS_DEST']):
        print(f"{app.config['UPLOADED_PHOTOS_DEST']} does not exist. Skipping cleanup.")
        return
    
    for file_name in os.listdir(app.config['UPLOADED_PHOTOS_DEST']):
        file_path = os.path.join(app.config['UPLOADED_PHOTOS_DEST'], file_name)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted: {file_path}")
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")

def run_scheduler():
    schedule.every(30).minute.do(cleanup_uploads)

    while True:
        schedule.run_pending()
        time.sleep(1)


scheduler_thread = Thread(target=run_scheduler)
scheduler_thread.daemon = True 

scheduler_thread.start()

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

class UploadForm(FlaskForm):
    photo = FileField(
        validators=[
            FileAllowed(photos, 'Only images are allowed'),
            FileRequired('File field should not be empty')
        ]
    )
    submit = SubmitField('Upload')


@app.route('/uploads/<filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'], filename)


@app.route('/', methods=['GET', 'POST'])
def upload_image():
    form = UploadForm()
    file_url = None
    
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        file_url = url_for('get_file', filename=filename)
       
    return render_template('index.html', form=form, file_url=file_url)



if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOADED_PHOTOS_DEST']):
        os.makedirs(app.config['UPLOADED_PHOTOS_DEST'])
    
    app.run(debug=True)





