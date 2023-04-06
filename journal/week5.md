# Week 5 — DynamoDB and Serverless Caching

###### Install boto3
- I added `boto3` to my requirements.txt file and i ran my "pip install -r requirements.txt"

- I docker-composed up to start up my containers

- I arranged my bin folder and put all scripts in their respective folders. 

- I went to my setup file to make changes that reflect the new names, and i did the same with all the scripts. 

- I created a new directory called **ddb** in the **bin** directory. And i created 3 files for my script named **schema-load**, **seed**, and **drop** and i put my code in the them. 

- I added the lines of code below into my **/bin/ddb/schema-load** file 
```
#!/usr/bin/env python3

import boto3
import sys

attrs = {
  'endpoint_url': 'http://localhost:8000'
}

if len(sys.argv) == 2:
  if "prod" in sys.argv[1]:
    attrs = {}

dynamodb = boto3.client('dynamodb', **attrs)
table_name = 'cruddur-messages'

# define the schema for the table
table_schema = {
  'AttributeDefinitions': [
    {
      'AttributeName': 'message_group_uuid',
      'AttributeType': 'S'
    },{
      'AttributeName': 'pk',
      'AttributeType': 'S'
    },{
      'AttributeName': 'sk',
      'AttributeType': 'S'
    }
  ],
  'KeySchema': [{
      'AttributeName': 'pk',
      'KeyType': 'HASH'
    },{
      'AttributeName': 'sk',
      'KeyType': 'RANGE'
    }
  ],
  'BillingMode': 'PROVISIONED',
  'ProvisionedThroughput': {
      'ReadCapacityUnits': 5,
      'WriteCapacityUnits': 5
  },
  'GlobalSecondaryIndexes':[{
    'IndexName':'message-group-sk-index',
    'KeySchema':[{
      'AttributeName': 'message_group_uuid',
      'KeyType': 'HASH'
    },{
      'AttributeName': 'sk',
      'KeyType': 'RANGE'
    }],
    'Projection': {
      'ProjectionType': 'ALL'
    },
    'ProvisionedThroughput': {
      'ReadCapacityUnits': 5,
      'WriteCapacityUnits': 5
    },
  }]
}

# create the table
response = dynamodb.create_table(
    TableName=table_name,
    **table_schema
)

# print the response
print(response)
```

- I uncommented my DynamoDB line of code, to enable my container run. 

- I ran my `./bin/ddb/schema-load` command and i got back data. 


- I created a new file in my **/bin/ddb/** directory called **list-tables** and put the code below into it. 
```
#! /usr/bin/bash

if [ "$1" = "prod" ]; then
  ENDPOINT_URL=""
else
  ENDPOINT_URL="--endpoint-url=http://localhost:8000"
fi

aws dynamodb list-tables  $ENDPOINT_URL \
  --query TableNames \
  --output table
```

- I ran my `./bin/ddb/list-tables` and it showed my cruddur table




