---
layout: default
title: Data Generators
parent: Architecture
nav_order: 1
---

# Data Generators
This diagram shows one of our connected machines, a HAAS 5-axis equipped with an MTConnect module. An edge device sits on the network alongside the machine and hosts our data adapter. The data adapter collects MTConnect data from the machine and converts it into an MQTT payload to publish to our MQTT Broker.

![ddb](../files/data_generators.png)


```{toctree}
:hidden:
:maxdepth: 1
architecture_data_generators
architecture_data_adapters
