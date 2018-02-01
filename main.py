from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, SelectMultipleField, widgets


# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

letters = []
updated = []
uinput = ''



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
    return render_template('main.html', name=name, letter=letter, form=form)

@app.route('/help')
def help():
    return render_template('help.html')


@app.route("/input", methods=['GET', 'POST'])
def input():
    form = ReusableForm(request.form)

    print form.errors
    letters = None
    alreadyconv = None
    updated = []
    letters = []
    words = []
    alreadyconv = []
    zipper = None
    count = None
    if request.method == 'POST':
        name = request.form['name']
        global uinput
        global updated
        uinput = name
        lines = name.split(' ')


        for l in lines:
            n = l.split()
            for x in n:

                # Find likley ID's
                if len(x) == 6 and not x.isalpha() and x.isalnum():
                    x = '*0' + x[4] + x[5] + x[2] + x[3] + x[0] + x[1]
                    updated.append(x)
                elif len(x) == 6 and x.isalpha() and x.isalpha():
                    words.append(x)
                    x = '*0' + x[4] + x[5] + x[2] + x[3] + x[0] + x[1]
                    letters.append(x)

                # Find already converted ID's
                elif len(x) == 8 and x[0] == '*':
                    alreadyconv.append(x)

        zipper = zip(letters, words)
        count = len(updated)
    return render_template('main.html', form=form, updated=updated, letters=letters, words=words, alreadyconv=alreadyconv, zipper=zipper, count=count, acount=len(alreadyconv))


@app.route("/fix", methods=['GET', 'POST'])
def fix():
    form = ReusableForm(request.form)
    my_letters = None
    final = None
    count = None
    if request.method == 'POST':
        my_letters = request.form.getlist("letter")
        conv = [x.encode('UTF8') for x in updated]
        newl = []
        final = []

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
                           update=updated, my_letters=my_letters, final=final, count=count)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
