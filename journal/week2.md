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





