from kubernetes import client, config
from pprint import pprint

def main():
	config.load_kube_config()

	api = client.CustomObjectsApi()

	TrafficStat_resource = {
		"apiVersion": "hybridscaling.knativescaling.dcn.ssu.ac.kr/v1",
		"kind": "TrafficStat",
		"metadata": {"name": "deploy-a-trafficstat-test"},
		"spec": {
			"servicename": "deploy-a",
			"scalinginputtraffic": "100"
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

if __name__ == "__main__":
    main()
