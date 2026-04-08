# Backend

## Overview
This folder contains the backend components of the project, responsible for data ingestion, processing, and analytics.

The system is built using a **serverless architecture on Kubernetes (Fission)**, where each module handles a specific data pipeline or analytical task.

---

## Structure

- **aussocialquery/** – Queries and processes Mastodon (social media) data  
- **Kafka/** – Streaming and message queue configurations  
- **lineinfo/** – Train line data processing  
- **mastodonquery/** – Social media data retrieval  
- **mharvester/** – Data harvesting services  
- **pedcount/** – Pedestrian data processing  
- **pedcountget/** – Pedestrian data retrieval  
- **sharveprocein/** – Data processing utilities  
- **socialharvester/** – Social media data ingestion  
- **specs/** – YAML deployment specifications (Fission functions, triggers)  
- **SUDO/** – Population data processing (Spatial Urban Data Observatory)  
- **sudoinfo/** – Population data retrieval  
- **traffic/** – Traffic data ingestion and processing  
- **trafficstatistic/** – Traffic analytics  
- **traininfo/** – Train service data processing  

---

## Key Features

- Event-driven data processing using **Kafka**
- Serverless function execution with **Fission**
- Modular design with each component handling a specific dataset
- Scalable deployment on **Kubernetes**

---

## Notes

- Each module corresponds to a specific **data source or analytical scenario**
- Deployment configurations are defined in the `specs/` folder
- Backend services are designed to be **independent and extensible**