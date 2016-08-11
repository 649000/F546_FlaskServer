from flask import Flask
import requests
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/F546'


class MainResult(db.Model):
    metadata_key = db.Column(db.String(128), primary_key=True)
    url = db.Column(db.String(128))
    subject_type = db.Column(db.String(50))
    source = db.Column(db.String(50))
    destination = db.Column(db.String(50))
    measurement_agent = db.Column(db.String(50))
    tool_name = db.Column(db.String(50))
    input_source = db.Column(db.String(50))
    input_destination = db.Column(db.String(50))
    time_interval = db.Column(db.String(50))
    ip_transport_protocol = db.Column(db.String(50))
    uri = db.Column(db.String(128))

    def __init__(self, metadata_key, url, subject_type, source, destination, measurement_agent, tool_name, input_source,
                 input_destination, time_interval, ip_transport_protocol, uri):
        self.metadata_key = metadata_key
        self.url = url
        self.subject_type = subject_type
        self.source = source
        self.destination = destination
        self.measurement_agent = measurement_agent
        self.tool_name = tool_name
        self.input_source = input_source
        self.input_destination = input_destination
        self.time_interval = time_interval
        self.ip_transport_protocol = ip_transport_protocol
        self.uri = uri


host = "http://hpc-perfsonar.usc.edu/esmond/perfsonar/archive/";


@app.route('/')
def hello_world():
    return 'Hello World!'


# Populate Everything
@app.route('/populateTraceroute')
def populateDB():
    mainParams = {'format': 'json', 'event-type': 'packet-trace', 'time-range': '86000'}
    response = requests.get(host, params=mainParams).json()

    #

    for newResult in response:
        print newResult['url']
        # Following keys may not be present
        # trace-max-ttl
        # ip-packet-size

        toBeAdded = MainResult(newResult['metadata-key'], newResult['url'], newResult['subject-type'],
                               newResult['source'], newResult['destination'], newResult['measurement-agent'],
                               newResult['tool-name'], newResult['input-source'], newResult['input-destination'],
                               newResult['time-interval'], newResult['ip-transport-protocol'], newResult['uri'])
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




    # url = db.Column(db.String(128))
    # subject_type = db.Column(db.String(50))
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

# ip = db.Column(db.String)
#     success = db.Column(db.String)
#     error_message = db.Column(db.String)
#     mtu = db.Column(db.String)
#     rtt = db.Column(db.String)
#     ttl = db.Column(db.String)
#     query = db.Column(db.String)
