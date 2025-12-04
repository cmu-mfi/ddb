# Publish-Subscribe Broker
MQTT is a lightweight Pub/Sub protocol widely used for IoT, robots, sensors, and low-power devices.

MQTT implements a topic-based publish/subscribe messaging pattern.

**Publish**
A client sends a PUBLISH packet to the broker containing:
Topic name
Message payload (binary or text)
QoS level (0, 1, or 2)
Retain flag (store as last-known-good message)
User properties (MQTT 5)
The broker receives the message and determines which subscribers should receive it.

**Subscribe**
A client sends a SUBSCRIBE packet specifying:
Topic filter
Requested QoS level

The MQTT broker is the central server responsible for:
  Managing client connections (TCP, typically over port 1883 or 8883 for TLS)
  Receiving PUBLISH packets from clients
  Routing messages based on topic matching
  Delivering messages to subscribed clients
  
CMU MFI is currently using EMQX open source MQTT broker for its implementation.
EMQX Broker Link for Windows: https://www.emqx.com/en/downloads/broker/v5.3.2

![ddb](../files/pubsub.png)
