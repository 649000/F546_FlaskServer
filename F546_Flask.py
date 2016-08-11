from flask import Flask
import requests
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/F546'



@app.route('/')
def hello_world():
    return 'Hello World!'


# Populate Everything
@app.route('/populateTraceroute')
def populateDB():
    r = requests.get('https://api.github.com/events')
    r.json()

    for newResult in r.json():
        # check for existing records
        toBeAdded = MainResult('x')
        db.session.add(toBeAdded)
        db.session.commit()

    return 'Hello World!'


# Populate New

@app.route('/x')
def hello_world2():
    return 'Hello World!!!!'


# Get Erroneous Traceroute
@app.route('/a')
def hello_world3():
    return 'Hello World!'



if __name__ == '__main__':
    app.run(debug=True)



class MainResult(db.Model):
    metadata_key = db.Column(db.String(128), primary_key=True)
    url = db.Column(db.String(128))
    subject_type = db.Column(db.String(50))
    # source = db.Column(db.String)
    # destination = db.Column(db.String)
    # measurement_agent = db.Column(db.String)
    # tool_name = db.Column(db.String)
    # input_source = db.Column(db.String)
    # input_destination = db.Column(db.String)
    # trace_max_ttl = db.Column(db.String)
    # time_interval = db.Column(db.String)
    # ip_transport_protocol = db.Column(db.String)
    # uri = db.Column(db.String)
    #
    # def __init__(self, username, email):
    #     self.username = username
    #     self.email = email
    #
    # def __repr__(self):
    #     return '<User %r>' % self.username


class IndividualTracerouteResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ts = db.Column(db.String(50))
    name = db.Column(db.String(50))


class IndividualTraceroute_SubResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
#     ip = db.Column(db.String)
#     success = db.Column(db.String)
#     error_message = db.Column(db.String)
#     mtu = db.Column(db.String)
#     rtt = db.Column(db.String)
#     ttl = db.Column(db.String)
#     query = db.Column(db.String)
