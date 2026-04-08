# Sharveprocein Function Deployment Guide

## Description
The files in this repository are used to deploy the Sharveprocein Function in a cluster. The function's purpose is to retrieve location and status information of Bluetooth detection sites from [VicRoads Data Exchange](https://data-exchange.vicroads.vic.gov.au/), format the obtained data, remove redundant information, and finally index it into Elasticsearch.

## Deployment Steps
1. **Package Creation**: Package the files `Sharveprocein.py`, `requirements.txt`, and `build.sh` into a `.zip` file.
   
   ```bash
   (
        cd fission/functions/sharveprocein
        zip -r sharveprocein.zip .
        mv sharveprocein.zip ../
    )

   ```
2. **Create Package**: Execute the following command in the terminal to create a package:

```bash
fission package create --spec --sourcearchive ./sharveprocein.zip --env python --name sharveprocein --buildcmd './build.sh'

```

3. **Create function**: Use the created package to create the function:

```bash
fission function create --spec --name sharveprocein --pkg sharveprocein --env python --entrypoint "Sharveprocein.main" --configmap shared-data

```

4. **Create HTTP Trigger**: Create an HTTP trigger for the function:

```bash
fission route create --spec --url /sharveprocein --function sharveprocein --name sharveprocein --createingress

```

5. **Apply Specifications**: Apply the specifications to the cluster:

```bash
fission spec apply --specdir fission/specs --wait

```

## test
To test the route and trigger, use the following command:
```bash
curl "http://127.0.0.1:9090/sharveprocein" | jq '.'

```
This will generate the **URL: "http://127.0.0.1:9090/sharveprocein"**.


