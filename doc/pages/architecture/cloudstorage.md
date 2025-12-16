## Cloud Storage

This diagram illustrates the different storage types used in our architecture.

- **Cloud File Storage**  
  Currently implemented as a partitioned drive, this storage is used for unstructured data such as images and videos.

- **Key-Value Storage**  
  Used to store JSON files containing text-based and semi-structured data.

- **Data Historian**  
  We currently use Aveva PI to store time-series data, such as spindle speed and other machine signals.

- **Metadata Store**  
  This is the core of our data retrieval strategy. It stores the mappings that link related data across systems, enabling efficient queries—    for example, retrieving all data for a given trial that includes video capture alongside machine data. 
  
![ddb](../../files/cloudstorage.png)
