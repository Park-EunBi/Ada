'''
Flask web server main file
Edited by EunBi Park
8 Nov 2022
'''

from flask import Flask, render_template
import sys
sys.path.append('..')
from mydatabase.violation_database import result

app = Flask(__name__)

'''
description :
- Link to indes page
'''
@app.route('/')
def hello():
    return render_template('index.html')

'''
description :
- Link to violation page
'''
@app.route('/violation')
def test():
    return render_template('violation.html', tables=[result.to_html()], titles=[''])

'''
description :
- Link to img page
'''
@app.route('/img')
def img():
    return render_template('violation_img.html', image="https://ada-scooter.s3.ap-northeast-2.amazonaws.com/4-2022-11-07+05-03-51.jpg")

'''
description :
- Link to graph page
'''
@app.route('/graph')
def graph():
    return render_template('graph.html')

if __name__ == '__main__':
    app.run(host="127.0.0.1", port='80')