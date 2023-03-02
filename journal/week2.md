# Week 2 — Distributed Tracing
## HoneyComb 
- I signed up for [HoneyComb](https://ui.honeycomb.io/) 
![honey comb env creation](https://user-images.githubusercontent.com/105195327/222523875-d53b1674-8ffd-47c5-be95-1ac2ad172383.png)

- I created an environment and stored my api key in a scratchpad 
![HC create env](https://user-images.githubusercontent.com/105195327/222524020-79f963fe-b7d7-491c-b847-0319fdd2f5f3.png)  

![HC api key](https://user-images.githubusercontent.com/105195327/222524060-aaaa66f0-813b-442c-a186-f0cbfb5d1943.png)  

- I pasted it to the terminal and set it as an environment variable using the `export HONEYCOMB_API_KEY="<insert your api key here>"` command. And i saved it using `gp env export HONEYCOMB_API_KEY="<insert API key here>"`  
- I set my honeycomb service name and saved to the environment. 
- I added the OTEL service name, endpoint and headers to my docker-compose.yml file  
> OTEL_SERVICE_NAME: "${HONEYCOMB_SERVICE_NAME}"
  OTEL_EXPORTER_OTLP_ENDPOINT: "https://api.honeycomb.io"
  OTEL_EXPORTER_OTLP_HEADERS: "x-honeycomb-team=${HONEYCOMB_API_KEY}"  
  
![OTEL env ](https://user-images.githubusercontent.com/105195327/222524148-2f3816d0-2976-476a-8e58-661d2f012422.png)  

- I changed directory to the **backend-flask** directory
- I went to honeycombs python instruction section, copied the installation commands there and added them to my requirements.txt file 
>   opentelemetry-api
    opentelemetry-sdk 
    opentelemetry-exporter-otlp-proto-http 
    opentelemetry-instrumentation-flask 
    opentelemetry-instrumentation-requests  

and ran `pip install -r requirements.txt`   

- I copied the import statements from initialize section and pasted it in my **app.py** file.  

>   from opentelemetry import trace
    from opentelemetry.instrumentation.flask import FlaskInstrumentor
    from opentelemetry.instrumentation.requests import RequestsInstrumentor
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor


- I copied the trace provider section to my app.py file 

>   # Initialize tracing and an exporter that can send data to Honeycomb
    provider = TracerProvider()
    processor = BatchSpanProcessor(OTLPSpanExporter())
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)
    tracer = trace.get_tracer(__name__) 

- I copied and pasted the part to initialise automatic instrumentations with flask, removing the already existing `app = Flask(__name__)` line.  
>   FlaskInstrumentor().instrument_app(app)
    RequestsInstrumentor().instrument()  

-     