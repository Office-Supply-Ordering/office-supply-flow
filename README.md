## Python Worker 
This folder holds all the code for the Python version of the Camunda 8 Worker. As client implementation we have used the pyzeebe dependency. You can find the GitHub repository right [here](https://github.com/camunda-community-hub/pyzeebe).

## Preparation
Install Python: https://python.org

### Install dependencies
The `requirements.txt` contains all dependencies necessary:
```shell
> pip install -r src/requirements.txt
```

### Export zeebe client credentials
You need to configure properties for Camunda Platform 8 in your environment. All necessary information can be retrieved from the Camunda 8 console (Cluster API view) right away. Remember to first of all create a client credential in order to make this possible. You then need to use the `Download credentials` function. The resulting txt-file contains a few export statements like this:

```shell
export CAMUNDA_CLUSTER_REGION='xxx-x'
export ZEEBE_ADDRESS='yyyyyyyy.xxx-x.zeebe.camunda.io:443'
export ZEEBE_CLIENT_ID='zzzzzzzzz'
export ZEEBE_CLIENT_SECRET='***********'
export ZEEBE_AUTHORIZATION_SERVER_URL='https://login.cloud.camunda.io/oauth/token'
```

*Execute these exports on your console*, for getting your credentials set in your local environment. `PythonWorker.py` will use those credentials from your environment automatically.

## Usage

- Open the process model in Camunda Cloud and start a new process instance.

- Run PythonWorker
  - Execute on console:
    ```shell
    > python src/PythonWorker.py
    ```

- Once the process is started and the python client is running, you get an output on the console for each task.

## Process Model

A running example of the process is available in the ‘Process Model’ directory of our GitHub repository. This directory also includes our BPMN model, along with all forms and DMN diagrams as well as screen recordings of the automation in Camunda in action.
