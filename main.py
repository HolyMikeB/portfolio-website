from flask import Flask, render_template, url_for, redirect
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL

app = Flask(__name__)
app.config['SECRET_KEY'] = 'X&;h"a/-AP\9+mV.Zw?#'
Bootstrap(app)

# Connect to DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projects.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()
db = SQLAlchemy(app)

db.create_all()


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=False)
    link = db.Column(db.String(250), unique=False)
    image = db.Column(db.String(250), unique=True, nullable=False)
    alt_text = db.Column(db.String(250), unique=False, nullable=False)


class CreateProjectForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    link = StringField('Link', validators=[DataRequired(), URL()])
    image = StringField('Image', validators=[DataRequired()])
    alt_text = StringField('Alt Text', validators=[DataRequired()])
    submit = SubmitField(label='Submit')


# new_project = Project(
#     title='Morse Code Translator',
#     link="https://github.com/HolyMikeB/morse-code-translator/blob/master/main.py",
#     image='https://2.bp.blogspot.com/_9w-e2Ulder8/S8k8bblJ-xI/AAAAAAAAAY0/cYkqH4aDBGU/s1600/morsecodeNumbers.jpg',
#     alt_text='morse code'
# )
# db.session.add(new_project)
# db.session.commit()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/projects')
def projects():
    projects = Project.query.all()
    return render_template('projects.html', all_projects=projects)


@app.route('/add-project', methods=['GET', "POST"])
def add_new_project():
    form = CreateProjectForm()
    if form.validate_on_submit():
        new_project = Project(
            title=form.title.data,
            link=form.link.data,
            image=form.image.data,
            alt_text=form.alt_text.data
        )
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('new-project.html', form=form)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
