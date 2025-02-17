import json

def parse_configuration_json(file_path):
    """
    Parsea el archivo de configuración en formato JSON y retorna un diccionario con los componentes de la máquina de Turing.
    
    El archivo JSON debe tener la siguiente estructura:
    {
      "states": ["q0", "q1", ...],
      "alphabet": ["1", "0", "B"],
      "blank": "B",
      "initial": "q0",
      "final": ["halt"],
      "transitions": {
          "q0,1": {"new_state": "q1", "write_symbol": "B", "direction": "R"},
          "q0,B": {"new_state": "qBase", "write_symbol": "B", "direction": "N"},
          ...
      }
    }
    
    Returns:
        dict: Diccionario con la configuración de la máquina de Turing.
    """
    with open(file_path, "r") as f:
        config = json.load(f)
    
    # Convertir las claves de las transiciones de cadena a tuplas.
    transitions = {}
    for key_str, value in config.get("transitions", {}).items():
        parts = key_str.split(",")
        if len(parts) != 2:
            raise ValueError(f"Clave de transición inválida: {key_str}")
        key = (parts[0].strip(), parts[1].strip())
        transitions[key] = value
    config["transitions"] = transitions

    return config

if __name__ == "__main__":
    config_path = "configs/fibonacci.json"
    config = parse_configuration_json(config_path)
    print("Configuración parseada:")
    for key, value in config.items():
        print(f"{key}: {value}")