from flask import Flask, render_template, request, redirect, Response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///storage.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Img(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)

db.create_all()

@app.route('/', methods=['GET','POST'])
def index():
    return render_template("index.html")


@app.route('/upload', methods=['GET','POST'])
def upload():
    pic = request.files['pic']

    filename = secure_filename(pic.filename)
    mimetype = pic.mimetype

    img = Img(img=pic.read(), mimetype=mimetype, name=filename)
    db.session.add(img)
    db.session.commit()

    return redirect('/upload/'+str(img.id)+"/"+img.name)

@app.route('/i/<int:id>/<iname>', methods=['GET','POST'])
def img(id, iname):
  img = Img.query.filter_by(id=id,name=iname).first()
  if not img:
    return "Not Found"
  else:
    return Response(img.img, mimetype=img.mimetype)


@app.route('/upload/<int:id>/<iname>', methods=['GET','POST'])
def im(id, iname):
  img = Img.query.filter_by(id=id,name=iname).first()
  if not img:
    return "Not Found"
  else:
    return render_template("uploaded.html", img_url='/i/'+str(id)+'/'+iname)
    print(Response(img.img, mimetype=img.mimetype))
    return Response(img.img, mimetype=img.mimetype)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
