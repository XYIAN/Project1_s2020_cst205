# @Author   KXD, , ,
# @Title    CST205 | Group Project 1
# @Abstract main python page to load flask templates to preform operations on given api and user data
# @Date     4/6/2020
# @v1.0.0

#begin imports 
#from WTForms import Form, BooleanField, StringField, validators
from flask import Flask, render_template
#end imports 

# create an instance of the Flask class
app = Flask(__name__)

# route() decorator binds a function to a URL
@app.route('/')
def homePage():
    return render_template('index.html')

