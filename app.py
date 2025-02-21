from flask import Flask, render_template, g, request
import sqlite3
import config



from datetime import datetime
app = Flask(__name__)

def connect_db():
    sql = sqlite3.connect(config.DATABASE_PATH)
    sql.row_factory=sqlite3.Row
    return sql
def get_db():
    if not hasattr(g, 'sqlite3_db'):
       g.sqlite_db=connect_db()
    return g.sqlite_db
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite3'):
        g.sqlite_db.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    db = get_db()
    if request.method == 'POST':
       date = request.form['date']
       dt = datetime.strptime(date, '%Y-%m-%d')
       database_date = datetime.strftime(dt, '%Y%m%d')
       db.execute('insert into log_date(entry_date) values(?)', [database_date])
       db.commit()
    cur = db.execute('select entry_date from log_date order by entry_date desc')
    results = cur.fetchall()
    header_date = []
    for i in results:
       single_date = {}
       d = datetime.strptime(str(i['entry_date']), '%Y%m%d')
       single_date['entry_date'] = datetime.strftime(d, '%B %d %Y')
       header_date.append(single_date)


    return render_template('home.html', header_date=header_date)
@app.route('/view')
def view():
    return render_template('day.html')
@app.route('/food', methods=['GET', 'POST'])
def food():
    db = get_db()
    if request.method=='POST':
        name=request.form['food-name']
        protein=int(request.form['proteins'])
        carbohydrates=int(request.form['carbohydrates'])
        fats=int(request.form['fats'])
        calories=protein*4 + carbohydrates * 4 + fats *9
         
        db = get_db()
        db.execute('insert into food(name, protein, carbohydrates, fat, calories) values(?,?,?,?,?)',\
                   [name, protein, carbohydrates, fats, calories])
        db.commit()
    cur = db.execute('select name, protein, carbohydrates, fat, calories from food')
    results = cur.fetchall()

    return render_template('add_food.html', results=results)
if __name__ == '__main__':
    app.run(debug=True)
