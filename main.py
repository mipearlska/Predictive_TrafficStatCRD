import schedule
import time
import os
from configs import configs
import requests
import csv
import rolling_update
from kubernetes import client, config

def get_metric():
    #q = 'rate(nginx_ingress_nginx_http_requests_total{app="nginx-ingress", class="nginx"}[15s])'
    #q = 'sum(rate(nginx_ingress_nginx_http_requests_total{app="nginx-ingress", class="nginx"}[15s]))'
    q = 'locust_users{instance="192.168.26.42:9646", job="generator1"}'
    test = []
    f = open('./dataset/request.csv', 'a', newline='')
    with f:
        writer = csv.writer(f)
        response = requests.get('{0}/api/v1/query'.format(configs.PROMETHEUS_URL), params={'query': q})
        if bool(response.json()['data']['result']):
            results = response.json()['data']['result'][0]['value'][1]
            results = float(results)
            results = round(results, 3)
            test.append(results)
        if bool(test):
            print("collected Rps/Users = {}".format(test[0]))
            writer.writerow(test)

def get_stable_concurrency():
    q = 'autoscaler_stable_request_concurrency{namespace_name="default", service_name="deploy-a"}'
    test = []
    response = requests.get('{0}/api/v1/query'.format(configs.PROMETHEUS_URL), params={'query': q})
    if bool(response.json()['data']['result']):
        results = response.json()['data']['result'][0]['value'][1]
        results = float(results)
        results = round(results, 3)
        print("Average Stable Window request count = {}".format(results))

def get_panic_concurrency():
    q = 'autoscaler_panic_request_concurrency{namespace_name="default", service_name="deploy-a"}'
    test = []
    response = requests.get('{0}/api/v1/query'.format(configs.PROMETHEUS_URL), params={'query': q})
    if bool(response.json()['data']['result']):
        results = response.json()['data']['result'][0]['value'][1]
        results = float(results)
        results = round(results, 3)
        print("Average Panic Window request count = {}".format(results))

def get_panic_mode():
    q = 'autoscaler_panic_mode{namespace_name="default", service_name="deploy-a"}'
    test = []
    response = requests.get('{0}/api/v1/query'.format(configs.PROMETHEUS_URL), params={'query': q})
    if bool(response.json()['data']['result']):
        results = response.json()['data']['result'][0]['value'][1]
        results = float(results)
        results = round(results, 3)
        print("Panic Mode = {}".format(results))

def get_actual_pod():
    q = 'autoscaler_actual_pods{namespace_name="default", service_name="deploy-a"}'
    test = []
    response = requests.get('{0}/api/v1/query'.format(configs.PROMETHEUS_URL), params={'query': q})
    if bool(response.json()['data']['result']):
        results = response.json()['data']['result'][0]['value'][1]
        results = float(results)
        results = round(results, 3)
        print("Actual Pods = {}".format(results))

def get_desired_pod():
    q = 'autoscaler_desired_pods{namespace_name="default", service_name="deploy-a"}'
    test = []
    response = requests.get('{0}/api/v1/query'.format(configs.PROMETHEUS_URL), params={'query': q})
    if bool(response.json()['data']['result']):
        results = response.json()['data']['result'][0]['value'][1]
        results = float(results)
        results = round(results, 3)
        print("Desired Pods = {}".format(results))

def get_activator_concurrency():
    q = 'activator_request_concurrency{namespace_name="default", service_name="deploy-a"}'
    test = []
    response = requests.get('{0}/api/v1/query'.format(configs.PROMETHEUS_URL), params={'query': q})
    if bool(response.json()['data']['result']):
        results = response.json()['data']['result'][0]['value'][1]
        results = float(results)
        results = round(results, 3)
        print("Activator Concurrency = {}".format(results))


def predict(api):
    get_metric()
    # get_stable_concurrency()
    # get_panic_concurrency()
    # get_panic_mode()
    # get_actual_pod()
    # get_desired_pod()
    predicted_traffic = str(rolling_update.predict_traffic())

    TrafficStat_resource = {
		"apiVersion": "hybridscaling.knativescaling.dcn.ssu.ac.kr/v1",
		"kind": "TrafficStat",
		"metadata": {"name": "deploy-a-trafficstat-test"},
		"spec": {
			"servicename": "deploy-a",
			"scalinginputtraffic": predicted_traffic
		}
	}
    
    list = api.list_namespaced_custom_object(
        group="hybridscaling.knativescaling.dcn.ssu.ac.kr",
		version="v1",
		namespace="default",
		plural="trafficstats" 
	)

    if len(list['items']) == 0:
        flag = False
    else:
        flag = False
        for item in list['items']:
            if "deploy-a" in item['metadata']['name']:
                flag = True

    if flag != True: 
  
        api.create_namespaced_custom_object(
			group="hybridscaling.knativescaling.dcn.ssu.ac.kr",
			version="v1",
			namespace="default",
			plural="trafficstats",
			body=TrafficStat_resource,
		)
        print("Resource created")
	
    else:

        api.patch_namespaced_custom_object(
        group="hybridscaling.knativescaling.dcn.ssu.ac.kr",
        version="v1",
        name="deploy-a-trafficstat-test",
        namespace="default",
        plural="trafficstats",
        body=TrafficStat_resource,
    )

if __name__ == '__main__':
    os.system("cp /root/Hybrid-Scaler/hybrid_scaler/dataset/request.bak /root/Hybrid-Scaler/hybrid_scaler/dataset/request.csv")
    config.load_kube_config()

    api = client.CustomObjectsApi()

    schedule.every().minute.at(":00").do(lambda: predict(api))
    #schedule.every().minute.at(":30").do(predict)
    while True:
        schedule.run_pending()
        time.sleep(1)

