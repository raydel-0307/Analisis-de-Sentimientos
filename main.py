import json
import iamodels


def fuctions_execute(config_json_path: str):
    # Leer el archivo de configuración
    with open(config_json_path, 'r', encoding='utf-8') as file:
        config = json.load(file)

    #Ruta del proyecto
    ruta = config["proyect"]
    with open(f"{ruta}/{config_json_path}", 'r', encoding='utf-8') as file:
        config = json.load(file)

    # Usar los valores del archivo JSON
    features = config["features"]
    target = config["target"]
    json_file = config["json_file"]
    output_filename = config["output_filename"]
    filters = config["filters"]
    num_threads = config["num_threads"]

    with open(f"{ruta}/{json_file}", 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Llamar al modelo y mostrar los resultados
    response = iamodels.AnalitysMain(features,target,data,ruta,output_filename,filters,num_threads)

def main():

    config_json_path = "config.json"

    result = fuctions_execute(config_json_path)

if __name__ == "__main__":
    main()
