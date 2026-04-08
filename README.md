## Cloud and Cloud Computing - Group 25
# Cloud-Driven Insights: Enhancing Urban Planning and Transportation in Victoria
## Overview
This project leverages cloud computing to develop an in-depth correlation study of urban transportation in Victoria, focusing on five key scenarios: pedestrian distribution, regional population density, usage per station, traffic congestion, and social media activity. The project utilizes the Melbourne Research Cloud (MRC) and integrates various technologies and tools to collect, process, analyze, and visualize data.

## Software Stack Installation and Required Pre-configuration
The detailed pre-requirements, client configuration, Kubernetes architecture design, and deplyments of Fission, ElasticSearch, Kibana, Kafka, and other usage can be referred to the linke below:
https://gitlab.unimelb.edu.au/feit-comp90024/comp90024/-/tree/master

Detialed list of functions and triggers can be found in the Appendix in the report under the folder Docs.

## Technology Stack
1. Back-end: Kubernetes, Helm, Fission, Elasticsearch, Kafka
2. Front-end: Jupyter Notebook, Folium, Seaborn, Matplotlib, ipywidgets
3. Data Processing: Pandas, NumPy, JSON, re

## Table of Contents for Project Repository
1. Backend: Source code for the application backend (harvesters, analytics, YAML specifications,  etc.)
2. Frontend: Source code for the client part of the application (Jupyter notebooks) including individual development and final combined version.
3. Test: Source code for backend automated tests
4. Data: Examples of SUDO data and pedestrian counting system sensor locations.
5. Docs: Final report for this project.
6. Database: Elasticsearch type mappings and queries.

## Data Sources
1. Spatial Urban Data Observatory (SUDO): https://sudo.eresearch.unimelb.edu.au/
2. Mastodon: https://mastodon.au and https://aus.social
3. Melbourne Data - the City of Melbourne’s Open Data Platform: https://data.melbourne.vic.gov.au/explore/dataset/pedestrian-counting-system-monthly-counts-per-hour
4. Train Service Passenger Counts Dataset: https://www.data.vic.gov.au/train-service-passenger-counts
5. Real-time Traffic Congestion: https://data-exchange.vicroads.vic.gov.au/

## Scenarios and Analysis
The project focuses on analyzing five scenarios:
1. SUDO: Regional population data analysis.
2. Mastodon: Sentiment analysis influenced by traffic conditions, weather, and air quality.
3. Pedestrian Counts: Analysis of pedestrian activity.
4. Train Service Passenger Counts: Trends and volume of passenger flow.
5. Real-time Congestion: Visualization of traffic congestion data.

## Other Branches
Other branches are for each team member to store their codes and results from the initial design on local machines, testing on local machines with ElasticSearch, straightforward deployements on K8s, and final YAML spec deployment on Fission.

## Team Members
1. Yechen Deng (647915)
2. Binghong Xing (1221767)
3. Chenxi Yao (1439064)
4. Mingyang Yao (1435451)
5. Ziying Zhang (1424322)

## Acknowledgements
We extend our sincere thanks to Professor Richard Sinnott, Mr. Luca Morandini, and Mr. Yao Pan for their invaluable guidance and supervision throughout this project.