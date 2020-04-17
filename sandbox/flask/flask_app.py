#project 11 flask sandbox
#.py route file 

#imports 
import random 
from flask import Flask, render_template
#end imports 

app = Flask(__name__)#instantiate 

#begin routing 
@app.route('/')#root route/index
def homepage():
    #pased variable arithmetic here
    #return/render index - in html index is known as the main or homepage
    return render_template('index.html')
    #end root route 
#can make other routes or pages via 
#@app.route('/fileNameHere')
#def page2():
#   return render_template('fileNameHere.html')
#end code 
