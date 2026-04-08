from elasticsearch import Elasticsearch
import warnings
warnings.filterwarnings("ignore")

# Elasticsearch服务器的URL
url = 'https://127.0.0.1:9200'

# Elasticsearch的用户名和密码
username = 'elastic'
password = 'elastic'

# 创建Elasticsearch连接
es = Elasticsearch(
    [url],
    http_auth=(username, password),
    verify_certs=False  # 如果您使用的是自签名证书，请将其设置为True；对于生产环境，推荐使用受信任的证书
)

# modify your index_settings
index_settings = {
  "settings": {
        "number_of_shards": 3,
        "number_of_replicas": 1
    },
  "mappings": {
    "properties": {
      "id": {
        "type": "keyword"
      },
      "sourceName": {
        "type": "keyword"
      },
      "sourceId": {
        "type": "keyword"
      },
      "status": {
        "type": "keyword"
      },
      "closedRoadName": {
        "type": "text"
      },
      "eventType": {
        "type": "keyword"
      },
      "eventDueTo": {
        "type": "keyword"
      },
      "ImpactDirection": {
        "type": "keyword"
      },
      "ImpactType": {
        "type": "keyword"
      },
      "numberLanesImpacted": {
        "type": "keyword"
      },
      "speedLimitOnSite": {
        "type": "integer"
      },
      "durationstart": {
        "type": "date",
        "format": "yyyy-MM-dd'T'HH:mm:ss"
      },
      "durationend": {
        "type": "date",
        "format": "yyyy-MM-dd'T'HH:mm:ss"
      },
      "lastUpdated": {
        "type": "date",
        "format": "yyyy-MM-dd HH:mm:ss"
      }
    }
  }
}


# create index
index_name = "robservations"
es.indices.create(index=index_name, body=index_settings)
index_list = es.cat.indices(format="json")
info = [index for index in index_list if index["index"] == "robservations"]
print(info)
# get mapping of index
mapping = es.indices.get_mapping(index=index_name)
print(mapping)
