from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, SelectMultipleField, widgets
from flask_sqlalchemy import SQLAlchemy
from functions import ZoneNames

#from flask.ext.heroku import Heroku

# App config.
DEBUG = False
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = ''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#heroku = Heroku(app)
db = SQLAlchemy(app)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = ''


letters = []
updated = []
uinput = ''
zonenames = ZoneNames()


class Counter(db.Model):
    __tablename__ = "count"
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(120))

    def __init__(self, number):
        self.number = number


'''
def get_or_create(model, **kwargs):
    instance = db.session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        db.session.add(instance)
        db.session.commit()
        return instance
'''


def v_count():
    if Counter.query.filter_by(id=1).first():
        update_this = Counter.query.filter_by(id=1).first()
        update_this.number = str(int(update_this.number) + 1)
        db.session.commit()
    else:
        instance = Counter('1')
        db.session.add(instance)
        db.session.commit()
    global cdata
    cdata = Counter.query.filter_by(id=1).first()

    return cdata


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])
    letter = MultiCheckboxField('Label', choices=letters)


@app.route('/', methods=['GET', 'POST'])
def index():
    name = TextField('Name:', validators=[validators.required()])
    letter = MultiCheckboxField('Label', choices=letters)
    form = Form()
    cdata = Counter.query.filter_by(id=1).first()
    return render_template('main.html', name=name, letter=letter, form=form, cdata=cdata.number)


@app.route('/help')
def help():
    return render_template('help.html')


@app.route("/zones", methods=['GET', 'POST'])
def zones():
    name = TextField('Name:', validators=[validators.required()])
    form = Form()
    test = None
    if request.method == 'POST':
        name = request.form['name']
        test = zonenames.convert(name)

    return render_template("zones.html", form=form, name=name, test=test)


@app.route("/input", methods=['GET', 'POST'])
def input():
    form = ReusableForm(request.form)

    letters = None
    alreadyconv = None
    global updated
    updated = []
    letters = []
    words = []
    alreadyconv = []
    zipper = None
    count = None
    blacklist = []
    cdata = Counter.query.filter_by(id=1).first()
    if request.method == 'POST':
        name = request.form['name']
        global uinput
        # v_count()
        uinput = name
        lines = name.split(' ')
        for l in lines:
            n = l.split()
            for x in n:

                # Find likley ID's
                if len(x) == 6 and not x.isalpha() and x.isalnum():
                    x = '*0' + x[4] + x[5] + x[2] + x[3] + x[0] + x[1]
                    if x not in updated and x not in blacklist:
                        updated.append(x)
                    else:
                        blacklist.append(x)
                        updated = [y for y in updated if x != y]

                elif len(x) == 6 and x.isalpha() and x.isalpha():
                    words.append(x)
                    x = '*0' + x[4] + x[5] + x[2] + x[3] + x[0] + x[1]
                    letters.append(x)

                # Find already converted ID's
                elif len(x) == 8 and x[0] == '*':
                    alreadyconv.append(x)

        zipper = zip(letters, words)
        count = len(updated)
    return render_template('main.html', form=form, updated=updated, letters=letters, words=words, alreadyconv=alreadyconv, zipper=zipper, count=count, acount=len(alreadyconv), cdata=cdata.number, blacklist=blacklist)


@app.route("/fix", methods=['GET', 'POST'])
def fix():
    form = ReusableForm(request.form)
    my_letters = None
    final = None
    count = None
    cdata = Counter.query.filter_by(id=1).first()
    if request.method == 'POST':
        my_letters = request.form.getlist("letter")
        conv = [x.encode('UTF8') for x in updated]
        newl = []
        final = []
        # v_count()
        # Create key cloud
        for x in conv:
            newl.append(x)
        for x in my_letters:
            newl.append(x)

        # Iterate original input with key cloud
        lines = uinput.split()
        for x in lines:
            if len(x) == 6:
                x = '*0' + x[4] + x[5] + x[2] + x[3] + x[0] + x[1]
                for y in newl:
                    if x == y:
                        final.append(x)
        print final
        count = len(final)

    return render_template('main.html', form=form,
                           update=updated, my_letters=my_letters, final=final, count=count, cdata=cdata.number)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
