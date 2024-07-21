from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
with app.app_context():
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
    app.config['SECRET_KEY']='thisisasecretkey'
    db = SQLAlchemy(app)


class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    photo = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(200), nullable=False)


@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/works")
def works():
    return render_template("works.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/blog")
def blog():
    return render_template("blog.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


app.config['UPLOAD_FOLDER'] = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

@app.route("/photo", methods=['POST', 'GET'])
def add_page():
    if request.method == 'POST':
        category = request.form['category']
        photo = request.files.get('photo')  # Используем get() чтобы избежать KeyError

        photo_path = None
        if photo and allowed_file(photo.filename):
            filename = secure_filename(photo.filename)
            photo_path = filename  # Сохраняем только имя файла в базе данных
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        elif photo:
            flash('Не подходящий формат файла!')

        try:
            new_post = Photo(photo=photo_path, category=category)
            db.session.add(new_post)
            db.session.commit()
        except:
            flash('Ошибка при добавлении статьи в БД')

        return redirect('/')
    else:
        return render_template("photo.html")


if __name__ == "__main__":
    app.run(debug=True)