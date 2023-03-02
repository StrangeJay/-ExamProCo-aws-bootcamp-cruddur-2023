# Week 2 — Distributed Tracing
## HoneyComb 
- I signed up for [HoneyComb](https://ui.honeycomb.io/) 
- I created an environment and stored my api key in a scratchpad
- I pasted it to the terminal and set it as an environment variable using the `export HONEYCOMB_API_KEY="<insert your api key here>"` command. And i saved it using `gp env export HONEYCOMB_API_KEY="<insert API key here>"`  
- I set my honeycomb service name and saved to the environment. 
- I added the OTEL service name, endpoint and headers to my docker-compose.yml file  
> OTEL_SERVICE_NAME: "${HONEYCOMB_SERVICE_NAME}"
  OTEL_EXPORTER_OTLP_ENDPOINT: "https://api.honeycomb.io"
  OTEL_EXPORTER_OTLP_HEADERS: "x-honeycomb-team=${HONEYCOMB_API_KEY}"  

- I changed directory to the **backend-flask** directory
- I added the following commands to my requirements.txt file 
>   opentelemetry-api
    opentelemetry-sdk 
    opentelemetry-exporter-otlp-proto-http 
    opentelemetry-instrumentation-flask 
    opentelemetry-instrumentation-requests  

and ran `pip install -r requirements.txt`   

- 

