import temperature
import humidity
import uv
import moisture

def get_output_num(variable_name):
    if variable_name == "temperature":
        return "output_1"
    if variable_name == "humidity":
        return "output_2"
    if variable_name == "moisture":
        return "output_3"
    if variable_name == "uv":
        return "output_4"


    



