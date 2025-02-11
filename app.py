from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
app = Flask(__name__)
with app.app_context():
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
    app.config['SECRET_KEY']='thisisasecretkey'
    db = SQLAlchemy(app)


class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    photo = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(200), nullable=False)


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route('/works')
def works():
    user_chose = request.args.get('category')
    if user_chose:
        images = Photo.query.filter_by(category=user_chose).all()
    else:
        images = Photo.query.all()
    return render_template('works.html', images=images)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/blog")
def blog():
    return render_template("blog.html")


@app.route("/contact", methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        print(name)
        email = request.form['email']
        print(email)
        message = request.form['message']
        print(message)
    else:
        return render_template("contact.html")


app.config['UPLOAD_FOLDER'] = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'jfif'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/photo", methods=['POST', 'GET'])
def add_page():
    if request.method == 'POST':
        category = request.form['category']
        photo = request.files.get('photo')

        photo_path = None
        print(photo)
        if photo and allowed_file(photo.filename):
            print('Успешный вход!')
            filename = secure_filename(photo.filename)
            photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            try:
                photo.save(photo_path)
            except Exception as e:
                flash(f'Ошибка при сохранении файла: {str(e)}')
                return redirect('/photo')
        else:
            flash('Не подходящий формат файла!')
            return redirect('/photo')

        if photo_path and category:
            try:
                print('Успешный вход 2')
                photo_path = photo_path.replace("\\", "/")
                new_post = Photo(photo=photo_path, category=category)
                db.session.add(new_post)
                db.session.commit()
                print('Фото успешно загружено!')
            except Exception as e:
                print(f'Ошибка при добавлении записи в базу данных: {str(e)}')
                db.session.rollback()
        else:
            flash('Ошибка: фото или категория не указаны.')

        return redirect('/index')
    else:
        return render_template("photo.html")



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")