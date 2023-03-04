# Week 2 — Distributed Tracing
## HoneyComb 
- I signed up for [HoneyComb](https://ui.honeycomb.io/) 
![honey comb env creation](https://user-images.githubusercontent.com/105195327/222523875-d53b1674-8ffd-47c5-be95-1ac2ad172383.png)

- I created an environment and stored my api key in a scratchpad 
![HC create env](https://user-images.githubusercontent.com/105195327/222524020-79f963fe-b7d7-491c-b847-0319fdd2f5f3.png)  

![HC api key](https://user-images.githubusercontent.com/105195327/222524060-aaaa66f0-813b-442c-a186-f0cbfb5d1943.png)  

- I pasted it to the terminal and set it as an environment variable using the `export HONEYCOMB_API_KEY="<insert your api key here>"` command. 
And i saved it using `gp env export HONEYCOMB_API_KEY="<insert API key here>"`  
- I set my honeycomb service name and saved to the environment. 
- I added the OTEL service name, endpoint and headers to my docker-compose.yml file  
``` 
  OTEL_SERVICE_NAME: "${HONEYCOMB_SERVICE_NAME}"  
  OTEL_EXPORTER_OTLP_ENDPOINT: "https://api.honeycomb.io"  
  OTEL_EXPORTER_OTLP_HEADERS: "x-honeycomb-team=${HONEYCOMB_API_KEY}"    
```  
  
![OTEL env ](https://user-images.githubusercontent.com/105195327/222524148-2f3816d0-2976-476a-8e58-661d2f012422.png)  

- I changed directory to the **backend-flask** directory
- I went to honeycombs python instruction section, copied the installation commands there and added them to my requirements.txt file 
![honeycomb pip install](https://user-images.githubusercontent.com/105195327/222602728-dad95858-7ad9-40bd-8a5c-8c4430bec3e3.png)  

```   
    opentelemetry-api
    opentelemetry-sdk 
    opentelemetry-exporter-otlp-proto-http 
    opentelemetry-instrumentation-flask 
    opentelemetry-instrumentation-requests  
```    

and ran `pip install -r requirements.txt`   

- I copied the import statements from initialize section and pasted it in my **app.py** file.  


``` 
    from opentelemetry import trace  
    from opentelemetry.instrumentation.flask import FlaskInstrumentor
    from opentelemetry.instrumentation.requests import RequestsInstrumentor
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
```    
![app py initialise import](https://user-images.githubusercontent.com/105195327/222602981-ee91dcbf-e80b-43ae-a49e-a4fd9351f645.png)  

- I copied the trace provider section to my app.py file 

``` 
    # Initialize tracing and an exporter that can send data to Honeycomb
    provider = TracerProvider()  
    processor = BatchSpanProcessor(OTLPSpanExporter())  
    provider.add_span_processor(processor)  
    trace.set_tracer_provider(provider)  
    tracer = trace.get_tracer(__name__)  
```    

- I copied and pasted the part to initialise automatic instrumentations with flask, removing the already existing `app = Flask(__name__)` line.  
``` 
    FlaskInstrumentor().instrument_app(app)  
    RequestsInstrumentor().instrument() 
```    

![complete Honeycomb ish](https://user-images.githubusercontent.com/105195327/222603107-1c3d352c-4d33-44e3-8896-7eac31f80216.png)  


- I changed directory to my **frontend-react-js** directory, and i ran `npm i`.   
- I set my ports on the gitpod.yml file, so i don't have to keep unlocking them everytime.  
- I went back to my production directory, right clicked on my docker-compose file, and did a docker-compose up. 
![Docker compose up  HC](https://user-images.githubusercontent.com/105195327/222603276-d5804af9-de1d-4a0b-98ef-326f70ffe2a4.png)  

![docker running perfectly](https://user-images.githubusercontent.com/105195327/222603295-9315611e-b1f9-44af-8aca-b4724d36079c.png)  

- The containers are running. And the backend and frontend are up.
![backend working](https://user-images.githubusercontent.com/105195327/222603329-b636674c-9127-4fca-9987-f576d80e4781.png)  

![frontend working](https://user-images.githubusercontent.com/105195327/222603355-c267bee0-dbf1-4b10-b8ab-f886b4000e10.png)  


- I went to honeycomb and checked for data, and there was data in the dataset.  
![honeycomb data set](https://user-images.githubusercontent.com/105195327/222603517-99e74ac5-158a-49c6-af97-aa5fc7f2d8e0.png)  

![honeycomb data feed](https://user-images.githubusercontent.com/105195327/222603551-3dbb07e7-5649-4efd-beae-0bfe1d0d311c.png)  

- I ran a trace for specific api calls to see more details  
![Screenshot 2023-03-03 012357](https://user-images.githubusercontent.com/105195327/222603723-fcd025d5-71e7-4354-ab04-57a31cb81e2c.png)

 
---

### Hardcoding a SPAN 
- I checked the [honeycomb docs](https://docs.honeycomb.io/getting-data-in/opentelemetry/python/) for the required command to aquire a tracer for my **home activities**  
- I copied the command 
```
from opentelemetry import trace` 
tracer = trace.get_tracer("home.activities")` 
with tracer.start_as_current_span("home-activities-mock-data"):
```
to my **home_activities.py** file.  

![add tracer](https://user-images.githubusercontent.com/105195327/222827129-b25cc64f-ff18-4427-8a0d-d689efc2ae75.png)  

- I went to my frontend directory, did my `npm i`
- I docker comosed up, went to the web pages to check them out, then i went to honeycomb to see if the extra span would show up for 'Home activities'  
![extra span](https://user-images.githubusercontent.com/105195327/222829679-643f51cc-6588-4d0b-a849-3f6860a6281d.png)  

![full view extra span](https://user-images.githubusercontent.com/105195327/222829970-9c8a0f96-93b2-442d-a430-6f614be5652b.png)

### Adding Attributes to the span 
- I went back to the honeycombs python docs, copied the necesasary command for adding attributes, and i added it to my **home_activities.py** file.  
```
span = trace.get_current_span()
span.set_attribute("user.id", user.id())
``` 
- I edited it with the necessary information i'd use to identify what i wanted.  
```
span.set_attribute("app.now", now.isofformat()) 
span.set_attribute("app.result_length", len(results))
``` 
![span attribute](https://user-images.githubusercontent.com/105195327/222830886-a0a15ef9-6afd-4bbf-b8de-3fa636c5fa8c.png)  

- I refreshed the web pages and revisited my honeycome query page  
![attributed query run](https://user-images.githubusercontent.com/105195327/222830988-ba69e30b-3d51-4bc5-bc3e-a710c9466c9e.png)  

![app  attributed query](https://user-images.githubusercontent.com/105195327/222831013-ec83c399-cc38-4126-a814-2c05969d8e25.png)

---
## X-Ray
### Instrument AWS X-Ray for Flask 
- I updated my **gitpod.yml** file, so i don't have to `npm i` everytime.  
![react gipod yml update](https://user-images.githubusercontent.com/105195327/222869264-c2f77d03-ff47-4903-b71e-fc088c87aaad.png)  

- I went to check the [AWS SDK for python](https://github.com/aws/aws-xray-sdk-python) instructions.  
- I changed directory to my **backend-flask** directory
- I added the `aws-xray-sdk` command to my requirements.txt file and ran `pip install -r requirements.txt` to install dependencies.  

### Add to app.py 
- i added the commands below to my app.py file 
```
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

xray_url = os.getenv("AWS_XRAY_URL")
xray_recorder.configure(service='backend-flask', dynamic_naming=xray_url)
XRayMiddleware(app, xray_recorder)
```

![xray fix in app-py](https://user-images.githubusercontent.com/105195327/222869374-73b06a3a-3246-46a7-88a1-9fb45e623337.png)  

### Setup AWS X-RAY Resources 
- I created an **xray.json** file in my **aws/json** folder.  
- I inputted the commands below in the file json file.  

```
{
  "SamplingRule": {
      "RuleName": "Cruddur",
      "ResourceARN": "*",
      "Priority": 9000,
      "FixedRate": 0.1,
      "ReservoirSize": 5,
      "ServiceName": "backend-flask",
      "ServiceType": "*",
      "Host": "*",
      "HTTPMethod": "*",
      "URLPath": "*",
      "Version": 1
  }
}
```

### Create an xray group
- I ran the command below, in my terminal.  
```
FLASK_ADDRESS="https://4567-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}"
aws xray create-group \
   --group-name "Cruddur" \
   --filter-expression "service(\"backend-flask\")"
``` 

![xray group](https://user-images.githubusercontent.com/105195327/222870575-f2cba06b-443c-4859-9bcb-9e9e10eb0e1f.png)  


### Create a sampling rule 
- I ran the following command in my terminal and it returned json 

```
aws xray create-sampling-rule --cli-input-json file://aws/json/xray.json
```
![xray json returned](https://user-images.githubusercontent.com/105195327/222869484-941fc617-6c99-442a-932d-7f6fe5c7a8b1.png)  

- Confirm on the AWS console that the xray sampling rule has been created  
![crudder rule](https://user-images.githubusercontent.com/105195327/222870544-9e740ec9-32e3-4d3d-89ee-1ec6efae883e.png)  

### Install the X-RAY Daemon 
- [Github AWS X-RAY Daemon]( wget https://s3.us-east-2.amazonaws.com/aws-xray-assets.us-east-2/xray-daemon/aws-xray-daemon-3.x.deb
 sudo dpkg -i **.deb)  

- [X-RAY Docker Compose example](https://github.com/marjamis/xray/blob/master/docker-compose.yml)  

```
wget https://s3.us-east-2.amazonaws.com/aws-xray-assets.us-east-2/xray-daemon/aws-xray-daemon-3.x.deb
sudo dpkg -i **.deb
```

### Add Deamon Service to Docker Compose
- I added the following commands to my **docker-compose.yml** file.  

```
  xray-daemon:
    image: "amazon/aws-xray-daemon"
    environment:
      AWS_ACCESS_KEY_ID: "${AWS_ACCESS_KEY_ID}"
      AWS_SECRET_ACCESS_KEY: "${AWS_SECRET_ACCESS_KEY}"
      AWS_REGION: "us-east-1"
    command:
      - "xray -o -b xray-daemon:2000"
    ports:
      - 2000:2000/udp
```
![xray in dockercompose](https://user-images.githubusercontent.com/105195327/222869576-6e2ed7ab-7b5e-4633-a543-562b31303019.png)  

- I add these two environment variables to the **backend-flask** section of my `docker-compose.yml` file.  
```
      AWS_XRAY_URL: "*4567-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}*"
      AWS_XRAY_DAEMON_ADDRESS: "xray-daemon:2000"
```

![xray in backend docker compose](https://user-images.githubusercontent.com/105195327/222869613-ca13ee8d-5837-4ebc-ade0-5fa9e0e50fb4.png)  

- I composed up to see if it'll work 
- I got an error while running docker-compose up, the xray port wasn't being served.  
- I checked my docker-compose file and noticed i placed my xray dependencies in the wrong place and so i fixed that and tried running it again and the containers where created 
![xray fix in app-py](https://user-images.githubusercontent.com/105195327/222869668-22649999-c6ae-4805-8355-a23f514e4a4e.png)  

- I visited the frontend and backend web pages, then checked the xray container logs to make sure there's communication.  
![xray successfully sent data](https://user-images.githubusercontent.com/105195327/222869774-de9f15f0-bffc-42ec-b911-82c9e98488e5.png)  

- I went to xray in the AWS management console to see the traces  
![xray traces in aws console](https://user-images.githubusercontent.com/105195327/222869820-a034654b-f304-41d5-9bc5-eceb63fbac97.png)  

- I ran my query, clicked into the information and went through everything. 
![xray traces in console2](https://user-images.githubusercontent.com/105195327/222869827-189fa714-a67a-4a0f-8984-5cce9f352c7e.png)  

![xray traces in console3](https://user-images.githubusercontent.com/105195327/222869842-2c8aeedc-8044-4020-918b-0852611e4b65.png)  

### Check service data for the last 10 minutes 
```
EPOCH=$(date +%s)
aws xray get-service-graph --start-time $(($EPOCH-600)) --end-time $EPOCH
```
---

## Cloudwatch logs
- I added `watchtower` to my requirements.txt file, changed directory to my backend flask and ran `pip install -r requirements.txt`   

- I added the following to my app.py  
```
import watchtower
import logging
from time import strftime 
```

![cloudwatch logs app](https://user-images.githubusercontent.com/105195327/222869900-3c5b3580-07b0-435f-a9ca-0b8265c27731.png)  

```
# Configuring Logger to Use CloudWatch  
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
cw_handler = watchtower.CloudWatchLogHandler(log_group='cruddur')
LOGGER.addHandler(console_handler)
LOGGER.addHandler(cw_handler)
```
![conf logger to use cloudwatch logs](https://user-images.githubusercontent.com/105195327/222870251-168a6766-44a5-45f4-a316-f4a33fe28395.png)   

```
@app.after_request
def after_request(response):
    timestamp = strftime('[%Y-%b-%d %H:%M]')
    LOGGER.error('%s %s %s %s %s %s', timestamp, request.remote_addr, request.method, request.scheme, request.full_path, response.status)
    return response
``` 

![conf logger error](https://user-images.githubusercontent.com/105195327/222870340-134efa6d-a915-4db8-9f7c-39c67246f304.png)  

- i added `LOGGER.info("HomeActivities)` to my **home_activities.py** file and `LOGGER.info("test log")` to my **app.py** file.  
![logger info activities](https://user-images.githubusercontent.com/105195327/222869954-291ff88d-a53e-4ca4-ae4f-f283eb612c5d.png)  

- I set my region, and access keys env var in backend-flask 
![region and access keys](https://user-images.githubusercontent.com/105195327/222870012-54fb502e-c0da-4b07-81fc-e9b1813fdfce.png)  

- I saved all changes and did a docker compose up.  
- I got an error while trying to access the activities/home endpoint, i made fixes to the app.py and home_activities. py file, and it worked.  
![Changes in logger app dot py](https://user-images.githubusercontent.com/105195327/222870118-9a0e8fc7-8783-4e80-a659-24efba77e0c3.png)   

- I went to cloudtrain in the aws console to check it out  
![cloudwatch logs created in console](https://user-images.githubusercontent.com/105195327/222870613-75371573-443a-45c8-b20b-4a2e2b6d4570.png)  

![cloudwatch logs created in console2](https://user-images.githubusercontent.com/105195327/222870627-655f4c36-b7eb-4a90-92fb-39836c292bde.png)  

![cloudwatch logs created in console3](https://user-images.githubusercontent.com/105195327/222870636-cee47571-1a94-4b7e-8c61-ce6e86fbe866.png)  

- I disabled after confirming, and i turned off all cloudwatch and xray commands to save on spend... 
![save on spend](https://user-images.githubusercontent.com/105195327/222870655-70695c54-46c0-4b0d-96e3-9cb2fc3e269f.png)  

---
## Rollbar 
-  I added `blinker` and `rollbar` to my **requirements.txt** file.  
- I changed directory to my **backend-flask** directory and i ran `pip install -r requirements.txt` 
- I went to rollbar, i copied my access token and saved it as an env var in my workspace.  
- I confirmed with `env | grep ROLLBAR` and i got my value.  
- I added the following commands gotten from [rollbar](https://app.rollbar.com/a/jaybills369) to my app.py file.  

```
import os
import rollbar
import rollbar.contrib.flask
from flask import got_request_exception
```



```
rollbar_access_token = os.getenv('ROLLBAR_ACCESS_TOKEN')
@app.before_first_request
def init_rollbar():
    """init rollbar module"""
    rollbar.init(
        # access token
        rollbar_access_token,
        # environment name
        'production',
        # server root directory, makes tracebacks prettier
        root=os.path.dirname(os.path.realpath(__file__)),
        # flask already sets up logging
        allow_logging_basic_config=False)

    # send exceptions from `app` to rollbar, using flask's signal system.
    got_request_exception.connect(rollbar.contrib.flask.report_exception, app)
```

- I added a test endpoint 

```
@app.route('/rollbar/test')
def rollbar_test():
    rollbar.report_message('Hello World!', 'warning')
    return "Hello World!"
``` 

- I did a docker compose up. 

