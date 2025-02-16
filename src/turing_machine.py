"""
Módulo turing_machine que contiene la clase TuringMachine para simular una máquina de Turing determinista de una cinta.
"""

class TuringMachine:
    def __init__(self, config, tape_input):
        """
        Inicializa la máquina de Turing usando la configuración y la cadena de entrada.

        Args:
            config (dict): Diccionario con los componentes de la máquina (estados, alfabeto, blank, initial, final, transitions).
            tape_input (str): Cadena de entrada según la convención definida.
        """
        self.states = config["states"]
        self.alphabet = config["alphabet"]
        self.blank = config["blank"]
        self.initial = config["initial"]
        self.final = config["final"]
        self.transitions = config["transitions"]
        
        self.current_state = self.initial
        self.head_position = 0
        
        # La cinta se representa como una lista de caracteres. Si la entrada está vacía, se coloca al menos un símbolo en blanco.
        self.tape = list(tape_input) if tape_input else [self.blank]
        self.halted = False

    def get_symbol(self):
        """
        Retorna el símbolo en la posición actual de la cabeza. Si la cabeza se sale del límite de la cinta,
        la cinta se extiende con el símbolo en blanco.
        """
        if self.head_position < 0:
            # Extiende la cinta a la izquierda
            extension = [self.blank] * (-self.head_position)
            self.tape = extension + self.tape
            self.head_position = 0
        elif self.head_position >= len(self.tape):
            # Extiende la cinta a la derecha
            extension_length = self.head_position - len(self.tape) + 1
            self.tape.extend([self.blank] * extension_length)
        return self.tape[self.head_position]

    def write_symbol(self, symbol):
        """Escribe un símbolo en la posición actual de la cabeza."""
        self.tape[self.head_position] = symbol

    def move_head(self, direction):
        """
        Mueve la cabeza en la dirección indicada.
        Args:
            direction (str): 'L' para izquierda, 'R' para derecha, 'N' para no mover.
        """
        if direction.upper() == 'L':
            self.head_position -= 1
        elif direction.upper() == 'R':
            self.head_position += 1
        # Si es 'N' u otra cosa, no se mueve.

    def execute_step(self):
        """
        Ejecuta un paso de la máquina: lee el símbolo actual, busca la transición correspondiente,
        escribe el símbolo indicado, mueve la cabeza y actualiza el estado.
        Si no se encuentra una transición, se detiene la máquina.
        """
        if self.halted:
            return

        current_symbol = self.get_symbol()
        key = (self.current_state, current_symbol)
        
        if key not in self.transitions:
            # No existe transición definida para esta configuración, se detiene.
            self.halted = True
            return
        
        new_state, write_symbol, direction = self.transitions[key]
        # Escribir el símbolo de salida
        self.write_symbol(write_symbol)
        # Mover la cabeza
        self.move_head(direction)
        # Actualizar el estado
        self.current_state = new_state
        
        # Si se alcanza un estado final, detener la máquina
        if self.current_state in self.final:
            self.halted = True

    def run(self):
        """Ejecuta la máquina de Turing hasta que se detenga."""
        while not self.halted:
            self.execute_step()

    def get_tape_as_string(self):
        """Retorna el contenido de la cinta como una cadena."""
        return ''.join(self.tape)

    def get_configuration(self):
        """
        Retorna una cadena con la configuración actual:
        - Estado actual
        - Posición de la cabeza
        - Contenido de la cinta
        """
        return f"Estado: {self.current_state} | Cabeza en: {self.head_position} | Cinta: {self.get_tape_as_string()}"

    def interpret_result(self):
        """
        Interpreta el resultado de la computación.
        Según la convención, se asume que el resultado (el n-ésimo número de Fibonacci en unaria)
        se encuentra en el registro F(n-1), que es la sección de la cinta posterior al último delimitador '0'.
        
        Retorna:
            int: Número de '1' en la sección final (valor en unaria).
        """
        tape_str = self.get_tape_as_string()
        if '0' in tape_str:
            last_delim_index = tape_str.rfind('0')
            result_section = tape_str[last_delim_index + 1:]
            return result_section.count('1')
        else:
            return None


# Ejemplo de uso
if __name__ == "__main__":
    # Ejemplo de configuración y entrada (para pruebas)
    # Se supone que 'config' fue obtenido mediante el parser desde un archivo .tm
    config_example = {
        "states": ["q0", "q1", "q2", "q3", "q4", "q5", "q6", "q7", "halt"],
        "alphabet": ["1", "0", "B"],
        "blank": "B",
        "initial": "q0",
        "final": ["halt"],
        "transitions": {
            ("q0", "1"): ("q0", "1", "R"),
            ("q0", "B"): ("q1", "0", "R"),
            ("q1", "B"): ("q2", "1", "R"),
            ("q2", "B"): ("q3", "0", "R"),
            ("q3", "B"): ("q4", "1", "R"),
            ("q4", "B"): ("q5", "0", "R"),
            ("q5", "B"): ("halt", "B", "R"),
            ("q5", "1"): ("q6", "1", "R"),
            ("q6", "0"): ("q7", "0", "R"),
            ("q7", "B"): ("q5", "1", "L")
        }
    }
    
    # Entrada de ejemplo (según la convención definida)
    input_tape = "11111"  # Por ejemplo, un contador en unaria
    tm = TuringMachine(config_example, input_tape)
    
    # Simulación paso a paso (mostrando la configuración en cada paso)
    step = 0
    while not tm.halted:
        print(f"Paso {step}: {tm.get_configuration()}")
        tm.execute_step()
        step += 1
    print(f"Paso {step}: {tm.get_configuration()}")
    
    # Interpretar el resultado final
    resultado = tm.interpret_result()
    print(f"Resultado interpretado: {resultado}")
