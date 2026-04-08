# sudoinfo Function Deployment Guide

## Description
The files in this repository are used to deploy the sudoinfo Function in a cluster. The function's purpose is to retrieve all information about different age groups in suburbs in Victoria. This function retrieve data from elasticsearch.

## Deployment Steps
1. **Package Creation**: Package the files `sudoinfo.py`, `requirements.txt`, and `build.sh` into a `.zip` file.

   ```bash
   (
        cd fission/functions/sudoinfo
        zip -r sudoinfo.zip .
        mv sudoinfo.zip ../
    )

   ```
2. **Create Package**: Execute the following command in the terminal to create a package:

```bash
fission package create --spec --sourcearchive ./sudoinfo.zip --env python --name sudoinfo --buildcmd './build.sh'

```

3. **Create function**: Use the created package to create the function:

```bash
fission function create --spec --name sudoinfo --pkg sudoinfo --env python --entrypoint "sudoinfo.main" --configmap shared-data

```

4. **Create HTTP Trigger**: Create an HTTP trigger for the function:

```bash
fission route create --spec --url /population --function sudoinfo --name population --createingress

```

5. **Apply Specifications**: Apply the specifications to the cluster:

```bash
fission spec apply --specdir fission/specs --wait

```

## test
To test the route and trigger, use the following command:
```bash
curl "http://127.0.0.1:9090/population" | jq '.'

```
This will generate the **URL: "http://127.0.0.1:9090/population"**.


