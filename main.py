from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
 
# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
 
class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])
 
 
@app.route("/", methods=['GET', 'POST'])
def hello():
    form = ReusableForm(request.form)
 
    print form.errors
    if request.method == 'POST':
        name=request.form['name']
        print name
        lines = name.split('\n')
        updated = []

        for l in lines:
        	n = l.split()
	        for x in n:
	        	if len(x) == 6 and x.isalpha() == False:
	        		x = '*0' + x[4]+x[5]+x[2]+x[3]+x[0]+x[1]
	        		updated.append(x)
 
        if form.validate():
            # Save the comment here.
            flash(updated)
        else:
            flash("Oops! You didn't enter anything.")
 
    return render_template('main.html', form=form)
 
if __name__ == "__main__":
    app.run()