# Bi-LSTM Traffic Prediction application, output prediction result as a Kubernetes CRD
for synthetic dataset (part of fifawc98 dataset with similar pattern) used in 
- https://doi.org/10.1016/j.future.2023.11.010

## Requirements for running
- Install TrafficStat CRD from https://github.com/mipearlska/knative_hybrid_scaling
- Install requirements (Python >= 3.6.9)
```
sudo apt install python3-dev python3-venv libffi-dev gcc libssl-dev git
```
```
python3 -m venv $HOME/Predictive_TrafficStatCRD
```
```
source $HOME/Predictive_TrafficStatCRD/bin/activate
```
```
pip install -U pip
```
```
pip install -r requirements.txt
```
- Locust Traffic Generator (https://locust.io/)
```
pip3 install locust
```
- Locust exporter for Prometheus
```
sudo docker run -d --net=host containersol/locust_exporter
```
- When deploying Prometheus, add Locust config in values.yaml of Prometheus:
job_name = Locust's job parameter in Prometheus query below
target = "<Host URL that run Locust>:9696"
```
prometheus:
  prometheusSpec:
    additionalScrapeConfigs:
      - job_name: "generator1"
        scrape_interval: 2s
        static_configs:
        - targets: ["192.168.26.20:9646"]
```
- Modify a correct Prometheus URL,port in configs/configs.py
```
PROMETHEUS_URL = "http://192.168.26.42:32000"
```
- Modify a correct Prometheus Locust query link in get_metric() function of main.py file:
```
locust_users{instance="192.168.26.42:9646", job="generator1"}
```
- (Optional) Modify when (which second) to make a prediction in __main__ function of main.py file:
```
schedule.every().minute.at(":55").do(lambda: predict(api))
```
## Running
- Generate Traffic to service by running locust traffic profile (Given sample profile change traffic amount every 1 minute)
```
locust -f locustservicetraffic.py
```
- Run Traffic Prediction service
```
python main.py
```
