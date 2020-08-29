import subprocess
import random
import configparser
import time

#Import the endpoint and topic from config.properties
configParser = configparser.RawConfigParser()
configFilePath = r'config.properties'
configParser.read(configFilePath)
endpoint = configParser.get('kafka-config', 'endpoint')
topic = configParser.get('kafka-config', 'topic')

producer_timings = {}
msg_size = 100
length=0
msg_payload = ('TestMessage' * 100).encode()[:msg_size]

#Add a random integer to podname so that it is unique each time the script is run
podName = 'kafka-producer'+str(random.randint(600,700))

#Calculate the number of messages
with open(r'InputData.txt') as values:
    for i in values:
        length = length+1
print("<=========Starting Benchmark=========>")
print("Total number of messages = {}\nSize of each message = {} Bytes".format(length,len(msg_payload)))

#Function to calculate the throughput
def calculate_throughput(timing, n_messages=length, msg_size=msg_size):
    print("Processed {0} messsages in {1:.2f} seconds".format(n_messages, timing ))
    print("{0:.2f} MB/s".format((msg_size * n_messages) / timing / (1024*1024)))
    print("{0:.2f} Msgs/s".format(n_messages / timing))

#Start the time before execution
producer_start = time.time() 

#Executes the kubectl command via cmd and sends each line of text in InputData.txt as a message to the topic
with open(r'InputData.txt') as values:
    subprocess.run(['kubectl', 'run', podName ,
            '-i', '--image=strimzi/kafka:0.19.0-kafka-2.4.0',
            '--rm=true', '--restart=Never',
            '--', 'bin/kafka-console-producer.sh',
            '--broker-list', endpoint,
            '--topic', topic],
        stdin=values,
        check=True, text=True)   

#Calculate the total time taken        
producer_end = time.time() - producer_start

producer_timings['strimzi_producer'] = producer_end
calculate_throughput(producer_timings['strimzi_producer'])
