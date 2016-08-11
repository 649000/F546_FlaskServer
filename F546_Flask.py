from flask import Flask
import requests
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/F546'
host = "http://hpc-perfsonar.usc.edu/esmond/perfsonar/archive/"




class MainResult(db.Model):
    # This is used to set the table name, mainly for foreign key.
    __tablename__ = "mainresult"

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
    individualResults = db.relationship('IndividualTracerouteResult_Value', backref='mainresult', lazy='dynamic',
                                        cascade="all, delete-orphan")

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

class IndividualTracerouteResult_Value(db.Model):
    __tablename__ = "individualtracerouteresult_value"

    metadata_key = db.Column(db.String(128), db.ForeignKey('mainresult.metadata_key'), primary_key=True)
    ts = db.Column(db.String(50), primary_key=True)

    ip = db.Column(db.String(50), primary_key=True)
    success = db.Column(db.String(30), primary_key=True)
    error_message = db.Column(db.String(30), primary_key=True)
    # mtu = db.Column(db.String(30), primary_key=True)
    rtt = db.Column(db.String(30), primary_key=True)
    ttl = db.Column(db.String(30), primary_key=True)
    query = db.Column(db.String(30), primary_key=True)
    orderNumber = db.Column(db.Integer, primary_key=True)

    def __init__(self, metadata_key, ts, ip, success, error_message, rtt, ttl, query, orderNumber):
        # MTU is not added as it's always null
        self.metadata_key = metadata_key
        self.ts = ts
        self.ip = ip
        self.success = success
        self.error_message = error_message
        # self.mtu = mtu
        self.rtt = rtt
        self.ttl = ttl
        self.query = query
        self.orderNumber = orderNumber

class IPAddress_Location(db.Model):
    __tablename__ = "IPAddress_Location"
    ip = db.Column(db.String(30), primary_key=True)
    city = db.Column(db.String(30))
    country = db.Column(db.String(30))


@app.route('/')
def hello_world():
    return 'Hello World!'




# Populate Everything
@app.route('/populateTraceroute')
def populateDB():
    mainParams = {'format': 'json', 'event-type': 'packet-trace', 'time-range': '86400'}
    response = requests.get(host, params=mainParams).json()

    # Consider dropping all data and redownload everything
    # Because we do do not know how often traceroute data are taken,
    # its difficult to determine if the data kept in DB is still valid.

    # To Delete Everything:
    # db.session.query(IndividualTracerouteResult_Value).delete()
    # db.session.query(MainResult).delete()
    # db.session.commit()


    for newResult in response:
        # Following keys may not be present
        # trace-max-ttl
        # ip-packet-size

        if MainResult.query.get(newResult['metadata-key']) is None:
            toBeAdded = MainResult(newResult['metadata-key'], newResult['url'], newResult['subject-type'],
                                   newResult['source'], newResult['destination'], newResult['measurement-agent'],
                                   newResult['tool-name'], newResult['input-source'], newResult['input-destination'],
                                   newResult['time-interval'], newResult['ip-transport-protocol'], newResult['uri'])
            db.session.add(toBeAdded)
            db.session.commit()

            for event in newResult['event-types']:
                if event['event-type'] == "packet-trace":
                    subParams = {'format': 'json', 'time-range': '86400'}
                    subHost = newResult['url'] + event['event-type'] + "/base"
                    subResponse = requests.get(subHost, params=subParams).json()
                    for subResult in subResponse:

                        for index, value in enumerate(subResult['val']):
                            print value['ip']
                            valuesToAdd = IndividualTracerouteResult_Value(newResult['metadata-key'], subResult['ts'],
                                                                           str(value['ip']),
                                                                           str(value['success']),
                                                                           str(value['error_message']),
                                                                           str(value['rtt']), str(value['ttl']),
                                                                           str(value['query']), index + 1)

                            db.session.add(valuesToAdd)
                            db.session.commit()






        else:
            insertedResult = MainResult.query.filter_by(metadata_key=newResult['metadata-key']).first()

            insertedResult.url = newResult['url']
            insertedResult.subject_type = newResult['subject-type']
            insertedResult.source = newResult['source']
            insertedResult.destination = newResult['destination']
            insertedResult.measurement_agent = newResult['measurement-agent']
            insertedResult.tool_name = newResult['tool-name']
            insertedResult.input_source = newResult['input-source']
            insertedResult.input_destination = newResult['input-destination']
            insertedResult.time_interval = newResult['time-interval']
            insertedResult.ip_transport_protocol = newResult['ip-transport-protocol']
            insertedResult.uri = newResult['uri']
            db.session.commit()

    return 'Hello World!'

# Get Erroneous Traceroute
@app.route('/getErroneousTracerouteRtt')
def erroneousTracerouteRTT():



    IndividualTracerouteResult_Value.query.filter_by(metadata_key='03d49625b00643058a40eb8672e94f4e').first()
    print MainResult.query.get("03d49625b00643058a40eb8672e94f4e")

    return 'Hello World!'



# Populate New

@app.route('/x')
def hello_world2():
    return 'Hello World!!!!'




if __name__ == '__main__':
    app.run(debug=True)
