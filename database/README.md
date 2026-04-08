# Database

## Overview
This folder contains Elasticsearch configurations, including index mappings and query definitions used in the data pipeline.

---

## Structure

- **mappings/**  
  Defines Elasticsearch index structures for different datasets  

- **queries/**  
  Predefined queries used for data retrieval and analytics  

- **train_service_count/**  
  Dataset-specific configurations and queries for train usage analysis  

---

## Purpose

- Enable **efficient indexing and fast querying** of large-scale data  
- Support analytics across multiple domains (transport, population, traffic, etc.)  
- Provide reusable query templates for backend services  

---

## Notes

- Elasticsearch is used as the primary **data storage and analytics engine**  
- Index design is optimised for **real-time querying and aggregation**