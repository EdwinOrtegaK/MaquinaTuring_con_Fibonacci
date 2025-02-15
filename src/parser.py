"""
Módulo parser para leer y procesar el archivo de configuración de la Máquina de Turing.
"""

def parse_configuration(file_path):
    """
    Parsea el archivo de configuración y retorna un diccionario con los componentes de la Máquina de Turing.

    El formato esperado del archivo es:
    
        # Comentarios con #
        states: q0,q1,q2,halt
        alphabet: 0,1,B
        blank: B
        initial: q0
        final: halt
        transition: q0,0 -> q1,1,R
        transition: q1,1 -> q2,0,L
        ...

    Args:
        file_path (str): Ruta del archivo de configuración (.tm).

    Returns:
        dict: Diccionario con la configuración, que contiene:
            - "states": lista de estados
            - "alphabet": lista de símbolos del alfabeto
            - "blank": símbolo en blanco de la cinta
            - "initial": estado inicial
            - "final": lista de estados de aceptación/rechazo
            - "transitions": diccionario con las transiciones, donde la clave es (estado_actual, símbolo_leído)
                             y el valor es (nuevo_estado, símbolo_escrito, dirección).
    """
    config = {
        "states": [],
        "alphabet": [],
        "blank": None,
        "initial": None,
        "final": [],
        "transitions": {}
    }
    
    try:
        with open(file_path, "r") as f:
            for line in f:
                # Remover espacios en blanco
                line = line.strip()
                # Eliminar comentarios inline: tomar solo la parte antes del '#'
                if '#' in line:
                    line = line.split('#', 1)[0].strip()
                # Si la línea queda vacía, continuar
                if not line:
                    continue

                # Procesar cada clave según su prefijo
                if line.startswith("states:"):
                    states_line = line[len("states:"):].strip()
                    config["states"] = [s.strip() for s in states_line.split(",") if s.strip()]
                elif line.startswith("alphabet:"):
                    alph_line = line[len("alphabet:"):].strip()
                    config["alphabet"] = [s.strip() for s in alph_line.split(",") if s.strip()]
                elif line.startswith("blank:"):
                    config["blank"] = line[len("blank:"):].strip()
                elif line.startswith("initial:"):
                    config["initial"] = line[len("initial:"):].strip()
                elif line.startswith("final:"):
                    final_line = line[len("final:"):].strip()
                    config["final"] = [s.strip() for s in final_line.split(",") if s.strip()]
                elif line.startswith("transition:"):
                    # Se espera el formato: transition: estado_actual,símbolo_leído -> nuevo_estado,símbolo_escrito,dirección
                    transition_line = line[len("transition:"):].strip()
                    if "->" not in transition_line:
                        raise ValueError(f"Formato de transición inválido: {line}")
                    
                    left, right = transition_line.split("->", 1)
                    left = left.strip()
                    right = right.strip()
                    
                    try:
                        current_state, read_symbol = [s.strip() for s in left.split(",")]
                    except Exception:
                        raise ValueError(f"Formato de transición (lado izquierdo) inválido: {left}")
                    
                    try:
                        new_state, write_symbol, movement = [s.strip() for s in right.split(",")]
                    except Exception:
                        raise ValueError(f"Formato de transición (lado derecho) inválido: {right}")
                    
                    # Almacenar la transición en el diccionario
                    config["transitions"][(current_state, read_symbol)] = (new_state, write_symbol, movement)
                else:
                    # Ignorar líneas con formato desconocido
                    continue

    except FileNotFoundError:
        raise FileNotFoundError(f"No se encontró el archivo de configuración: {file_path}")
    except Exception as e:
        raise Exception(f"Error al parsear el archivo de configuración: {e}")

    return config

# Ejemplo de uso (puede ser removido o comentado en producción):
if __name__ == "__main__":
    config_path = "configs/fibonacci.tm"
    config = parse_configuration(config_path)
    print("Configuración parseada:")
    for key, value in config.items():
        print(f"{key}: {value}")
