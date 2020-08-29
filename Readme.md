
## KAFKA BENCHMARK 

This script is useful to benchmark the kafka deployed on kubernetes environment provided that is has an endpoint exposed (cluster ip)

## Prerequisites 
-  pip install -U -r requirements.txt

## Contents

```
- Config.properties : The endpoint and topic details are configured here.
- InputData.txt : The messages to be sent to the topic is added here. Each line is one separate message.
- Producer.py : The script that executes kubectl command and sends the messages from the InputData.txt to the topic from config.properties.
```
