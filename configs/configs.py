EPOCHS = 100
BATCH_SIZE = 128
NUM_UNITS = 100
VALIDATION_SPLIT = 0.2
N_STEPS_IN = 7
N_STEPS_OUT = 1
MODEL_PATH = "./model/demo-model.h5"
PERFORMANCE_MODEL_PATH = "./model/performance_model.pkl"
SCALER_PATH = "./scaler/demo-scaler.pkl"
#TRAIN_DATA_PATH = "./dataset/recurrent_fault.csv"
COLLECTED_DATA_PATH = "./dataset/request.csv"
PROMETHEUS_URL = "http://192.168.26.42:32000"
THRESHOLD = 20
APP_LABEL = "deploy-a"
DEPLOYMENT_NAME = "deploy-a"
BURST = 50
COUNT = 1
