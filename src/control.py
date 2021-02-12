def pin_handling(variable_name):
    if variable_name == "temperature" or variable_name == "humidity":
        pin = 17
        return pin
    if variable_name == "uv":
        pin = 16
        return pin
    if variable_name == "moisture":
        pin = 5
        return pin


def get_output_num(variable_name):
    if variable_name == "temperature":
        return "output_1"
    if variable_name == "humidity":
        return "output_2"
    if variable_name == "moisture":
        return "output_3"
    if variable_name == "uv":
        return "output_4"


    



