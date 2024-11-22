import json
import os
import pytest
import main

# Leer el archivo config.json para obtener el número de proyecto
with open('config.json', 'r', encoding='utf-8') as file:
    config_data = json.load(file)
    project = config_data.get('proyect')

config_file = f"{project}/config.json"

config_structure = {
    'json_file': str,
    'features': str,
    'target': str,
    'model': list,
    'output_filename': str,
    'filters': list
}

def get_output_structure(config_file):
    with open(config_file, 'r', encoding='utf-8') as file:
        config = json.load(file)
    output_structure = {config['target']: str}
    return output_structure

output_structure = get_output_structure(config_file)

# Prueba para verificar si el archivo de configuración existe y tiene la estructura correcta
def test_config_json():
    assert os.path.exists(config_file), f"El archivo de configuración {config_file} no existe"
    
    with open(config_file, 'r', encoding='utf-8') as file:
        config = json.load(file)
    
    for key, value_type in config_structure.items():
        assert key in config, f"Clave '{key}' no encontrada en {config_file}"
        assert isinstance(config[key], value_type), f"Clave '{key}' debería ser de tipo {value_type.__name__} en {config_file}"
    
    assert config['model'], "El modelo no debería estar vacío"
    assert len(config['model']) > 0, "El modelo no debería estar vacío"

# Prueba para verificar si el archivo JSON especificado en la configuración existe y tiene la estructura correcta
def test_json_file_content():
    with open(config_file, 'r', encoding='utf-8') as file:
        config = json.load(file)
    
    json_file_path = f"{project}/{config['json_file']}"
    assert os.path.exists(json_file_path), f"El archivo {config['json_file']} especificado en {config_file} no existe"
    
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    
    # Verificar que la clave 'features' exista en todos los elementos del archivo JSON
    for item in data:
        assert config['features'] in item, f"Clave '{config['features']}' no encontrada en el elemento de datos en {json_file_path}"
    
    # Verificar los filtros si existen
    if config['filters']:
        first_filter = config['filters'][0]
        for key in first_filter.keys():
            # Verificar que la clave del primer filtro exista en todos los elementos del archivo JSON
            for item in data:
                assert key in item, f"Clave '{key}' del primer filtro no encontrada en el elemento de datos en {json_file_path}"
            
            # Verificar que el valor del primer filtro exista al menos una vez en los elementos del archivo JSON
            value_exists = any(item[key] == first_filter[key] for item in data)
            assert value_exists, f"Valor '{first_filter[key]}' del primer filtro no encontrado en ningún elemento de datos en {json_file_path}"
        
        # Verificar que el segundo filtro tenga la clave 'questions' y que su valor exista como clave en todos los elementos del archivo JSON
        second_filter = config['filters'][1]
        assert 'questions' in second_filter, "El segundo filtro debe tener la clave 'questions'"
        question_key = second_filter['questions']
        for item in data:
            assert question_key in item, f"Clave '{question_key}' del segundo filtro no encontrada en el elemento de datos en {json_file_path}"


#Prueba para verificar si la salida del algoritmo es JSON válido y tiene la estructura correcta
def test_algorithm_output():
    main.fuctions_execute("config.json")
    
    with open(config_file, 'r', encoding='utf-8') as file:
        config = json.load(file)
        
    output_file = f"{project}/{config['output_filename']}"
    assert os.path.exists(output_file), f"El archivo de salida {output_file} no existe"
    
    with open(output_file, 'r', encoding='utf-8') as file:
        result = json.load(file)
    
    assert isinstance(result, list), "La salida debería ser una lista"
    assert len(result) > 0, "Las recomendaciones no deberían estar vacías"
    
    for recommendation in result:
        for key, value_type in output_structure.items():
            assert key in recommendation, f"Clave '{key}' no encontrada en la recomendación"
            assert isinstance(recommendation[key], value_type), f"Clave '{key}' debería ser de tipo {value_type.__name__}"



if __name__ == "__main__":
    pytest.main()