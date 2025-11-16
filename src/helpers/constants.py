import json
import os

BASE_PATH = os.path.abspath(os.getcwd())
CONFIG_FOLDER_PATH = os.path.join(BASE_PATH, "configuration")
CONFIGURATION_FILE_PATH = os.path.join(CONFIG_FOLDER_PATH, "student_config.json")
RESULTS_FOLDER = os.path.join(BASE_PATH, "results")
INPUT_FOLDER = os.path.join(BASE_PATH, "input")
# input_file = "cnffile.cnf"
# input_file = "binpacking.txt"
#input_file = "data_kSAT_VS.cnf"
input_file = "data_2SAT_VS.cnf"
#input_file = "data_check1_VS.cnf"
INPUT_FILE = os.path.join(INPUT_FOLDER, input_file)


def parse_config(config_path):
    if not os.path.exists(config_path):
        raise Exception("Please make sure the configuration file exists!!!")
    with open(config_path, mode="r", encoding="utf-8") as conf_buffer:
        data = json.load(conf_buffer)
    data = data["Project Configuration"]
    selection = data["Selection"]
    sub_problem = data["Sub Problem"]
    return selection, sub_problem
