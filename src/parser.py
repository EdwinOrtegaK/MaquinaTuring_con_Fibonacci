import json

def parse_configuration(file_path):
    """
    Carga la configuración de la Máquina de Turing desde un archivo JSON.

    Args:
        file_path (str): Ruta del archivo JSON con la configuración.

    Returns:
        dict: Diccionario con la configuración de la Máquina de Turing.
    """
    try:
        with open(file_path, "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"No se encontró el archivo: {file_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Error en el formato JSON del archivo {file_path}")
    
    return config

# Ejemplo de uso
if __name__ == "__main__":
    config_path = "configs/fibonacci.json"
    config = parse_configuration(config_path)
    print("Configuración cargada correctamente:")
    print(json.dumps(config, indent=4))
