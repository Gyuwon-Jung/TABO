from flask import Flask, render_template

from convert import convert

app = Flask(__name__)

@app.route('/')
def home():
   return 'This is Example API!'

@app.route('/index')
def index():
    # 원하는 동적인 값 설정
    statement = convert()
    return render_template('template.html', string=statement)

if __name__ == '__main__':
    app.run(debug=True)