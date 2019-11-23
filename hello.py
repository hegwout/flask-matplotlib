# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template
from flask import Response
from flask_mail import Message
from flask_mail import Mail

import click 
import pymysql.cursors 
import numpy as np
import matplotlib.pyplot as plt
import io
import os
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

app = Flask(__name__)
mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": os.environ['EMAIL_USER'] , 
    "MAIL_PASSWORD": os.environ['EMAIL_PASSWORD'], 
} 
app.config.update(mail_settings)
mail = Mail(app)

@app.route('/') 
def html(name=None):  
    res = db_query(30,'desc')   
    return render_template('email.html',  result=res)

@app.cli.command("sendmail")
def sendmail(): 
    res = db_query(30,'desc') 
    resAsc = db_query(7,'asc')  
    fig = create_figure_res(resAsc) 
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)  
    fig.savefig('my_plot.png',dpi = 200) 
    day = res[0]['day'].strftime('%Y-%m-%d')
    count = res[0]['count'] 
    msg = Message("Recent users: {}:{} times".format(day,count),
                  sender="no-reply@yourdomain.com",
                  recipients=["recipient@yourdomain.com"])
    html = render_template('email.html', result=res)
    msg.body = html
    msg.html = html
    #mail.send(msg)
    with app.open_resource("my_plot.png") as fp:  
        msg.attach("my_plot.png","image/png",fp.read(),headers=[['Content-ID', '<my_plot.png>'],])  
        mail.send(msg)  
    return html
 
def create_figure_res(res): 
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = [x['day'].strftime('%m-%d') for x in res]
    ys = [x['count'] for x in res]
    axis.plot(xs, ys)
    axis.set_xlabel('Day')
    axis.set_ylabel('Count')
    fig.set_size_inches(8, 4) 
    return fig 

class Database:
    def __init__(self):
        host = os.environ['DB_DEFAULT_URL']
        user = os.environ['DB_DEFAULT_USERNAME']
        password = os.environ['DB_DEFAULT_PASSWORD']
        db = os.environ['DB_DEFAULT_NAME']
        self.con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.
                                   DictCursor)
        self.cur = self.con.cursor()
    def list(self,num = 30, direction = 'desc'):
        sql = '''SELECT DATE(last_login) as `day`,count(1) as `count`
                FROM  fos_user 
                WHERE last_login >  (NOW() - INTERVAL {} DAY)
                GROUP BY DATE(last_login)
                ORDER BY `day` {}
                LIMIT {};  
                '''.format(num,direction,num)
        self.cur.execute(sql)
        result = self.cur.fetchall()
        return result

def db_query(num,direction):
    db = Database()
    emps = db.list(num,direction)
    return emps

def fig_to_base64(fig):
    img = io.BytesIO()
    fig.savefig(img, format='png',
                bbox_inches='tight')
    img.seek(0)

    return base64.b64encode(img.getvalue())


if __name__ == '__main__': 
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)    