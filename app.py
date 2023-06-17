from io import BytesIO
from flask import Flask, redirect ,send_file,render_template, request, flash, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = '********hidden********'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Upload(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    filename = db.Column(db.String(25))
    data = db.Column(db.LargeBinary)

@app.route('/', methods = ['POST', 'GET'])
def main():
    if request.method == 'POST':
        file = request.files['file']
        upload = Upload(filename = file.filename, data= file.read())
        db.session.add(upload)
        db.session.commit()
        flash (f"Sucessfully uploaded {file.filename}")
        return redirect(url_for('main'))
    return render_template('index.html')

@app.route('/download/<upload_id>')
def download(upload_id):
    upload = Upload.query.filter_by(id=upload_id).first()
    return send_file(BytesIO(upload.data), as_attachment=True, download_name= upload.filename)
    return redirect(url_for('main'))

@app.errorhandler(404)
def not_found(e):
    return redirect(url_for('main'))

app.app_context().push()

if __name__ == '__main__':
    app.run(debug=True)