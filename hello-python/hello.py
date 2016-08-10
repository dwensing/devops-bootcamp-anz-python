import os
import uuid
from flask import Flask

#redis stuff
import os
import urlparse
import redis
import json

rediscloud_service = json.loads(os.environ['VCAP_SERVICES'])['rediscloud'][0]
credentials = rediscloud_service['credentials']
r = redis.Redis(host=credentials['hostname'], port=credentials['port'], password=credentials['password'])

app = Flask(__name__)
my_uuid = str(uuid.uuid1())
BLUE = "#0099FF"
GREEN = "#33CC33"

COLOR = BLUE
counter = 0 

#set global counter
r.set("counter",1)

@app.route('/')
def hello():

    r.incr("counter")
    if r.get("counter") %2 == 0:
        COLOR = GREEN
    else:
        COLOR = BLUE

    return """
    <html>
    <body bgcolor="{}">

    <center><h1><font color="pink">Hi, I'm GUID:<br/>
    {}</br>
    
    <br>
    
    Page Hit Count {}

    </center>
    <br>

    </body>
    </html>
    """.format(COLOR,my_uuid,counter)

if __name__ == "__main__":
	app.run(debug=True,host='0.0.0.0', port=int(os.getenv('PORT', '5000')))
