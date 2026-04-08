# SUDO Regional Population upload to es Guide

## Description
The files in this repository are used to upload the data from local file downloaded at SUDO platform to ElasticSearch. The function's purpose is to format the JSON data into correct format and keep the necessary items and finally index it into Elasticsearch.

## Processing Steps
1. **Prepare to run**: Change the json_file_path to the actual path to the json file in the folder. Make sure you have downloaded the elasticsearch8 package

   ```
   json_file_path = "Actual path of json file"

   ```
2. **Connect to 9200**: Make sure you connect to port 9200

```bash
kubectl port-forward service/elasticsearch-master -n elastic 9200:9200

```

3. **Create index before you run**: 

```bash
curl -X PUT "https://127.0.0.1:9200/population" -H 'Content-Type: application/json' -d'
{
  "settings": {
    "number_of_shards": 3,
    "number_of_replicas": 1
  },
  "mappings": {
    "properties": {
      "persons_num": {
        "type": "integer",
        "null_value": 0
      },
      "percentage_person_aged_0_14": {
        "type": "float",
        "null_value": 0
      },
      "percentage_person_aged_15_64": {
        "type": "integer",
        "null_value": 0
      },
      "percentage_person_aged_65_plus": {
        "type": "integer",
        "null_value": 0
      },
      "feature_name": {
        "type": "keyword"
      }
    }
  }
}' --insecure --user elastic:elastic


```

4. **Run function locally**: Create an HTTP trigger for the function:

```bash
python3 ./sudo.py

```


