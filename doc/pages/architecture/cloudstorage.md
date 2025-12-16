## Cloud Storage

This diagram illustrates the different storage types used in our architecture.

- **Cloud File Storage**  
  Currently implemented as a partitioned drive, this storage is used for unstructured data such as images and videos.

- **Key-Value Storage**  
  Used to store JSON files containing text-based and semi-structured data.

- **Data Historian**  
  We currently use Aveva PI to store time-series data, such as spindle speed and other machine signals.

- **Metadata Store**  
  This is the core of our data retrieval strategy. It stores the mappings that link related data across systems, enabling efficient queries.    For example, retrieving all data for a given trial that includes video capture alongside machine data.

The **connectors** are primarily custom software components developed by MFI, with one connector per storage system. Each connector subscribes to relevant topics streamed through the MQTT broker and organizes the data into the database. The exception is the **Data Historian**, where Aveva PI uses its own native connector.

  
![ddb](../../files/cloudstorage.png)
