#!/usr/bin/python

import os
import uuid
import json
import redis
from flask import Flask

rediscloud_service = json.loads(os.environ['VCAP_SERVICES'])['rediscloud'][0]
credentials = rediscloud_service['credentials']
r = redis.Redis(host=credentials['hostname'], port=credentials['port'], password=credentials['password'])

app = Flask(__name__)
port = int(os.getenv("PORT"))
myuuid = str(uuid.uuid1())
myinstance = str(os.getenv("CF_INSTANCE_INDEX", 0))

@app.route('/')
def main():
    counter = r.incr("yoshi:incr")
    return """
    <html>
    <head>
        <title> VMware Tanzu Application Service </title>
    </head>
    <body>
        <center>
          <FONT size="6" color="black">====== VMware Tanzu Application Service ======</FONT><br>
          <b><FONT size="7" color="black">Simple Web Application with Redis</FONT></b><br>
          <FONT size="5" color="black">Running on Pivotal Web Service</FONT><br>
          <br>
          <h1> App Instance : <font color="blue"> {}<br>
          <FONT size="4" color="blue">UUID : {}</FONT><br>
          <h1> Access Counter : <font color="blue"> {}<br>
        </center>
    </body>
    </html>
    """.format(myinstance, myuuid, counter, )
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port)
