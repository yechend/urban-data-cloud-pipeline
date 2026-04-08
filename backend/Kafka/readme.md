# Project Overview

This directory contains various functions and files for data acquisition, distribution, processing, and indexing.

## Function Descriptions

### Data Harvesting

Functions tagged with `harvest` are used to acquire data.

### Data Distribution

The `Enqueue` function is responsible for receiving and distributing data.

### Kafka Topics

The `Topic` folder contains all topic files involved in the Kafka queue.

### Data Processing

Functions tagged with `processor` are responsible for retrieving, processing, and forwarding data from the queue.

### Data Indexing

Functions tagged with `observations` are responsible for indexing data into Elasticsearch (ES).
