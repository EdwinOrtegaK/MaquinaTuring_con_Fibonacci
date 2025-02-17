<<<<<<< HEAD
class TuringMachine:
    def __init__(self, config, tape_input):
        """
        Inicializa la máquina de Turing usando la configuración JSON y la entrada.

        Args:
            config (dict): Configuración JSON con los estados, alfabeto, transiciones, etc.
            tape_input (str): Cadena de entrada según la convención definida.
=======
"""
Módulo turing_machine que contiene la clase TuringMachine para simular una máquina de Turing determinista de una cinta.
"""

class TuringMachine:
    def __init__(self, config, tape_input):
        """
        Inicializa la máquina de Turing usando la configuración y la cadena de entrada.
>>>>>>> 0928639 (feat: implemented the new configuration)
        """
        self.states = config["states"]
        self.alphabet = config["alphabet"]
        self.blank = config["blank"]
        self.initial = config["initial"]
        self.final = config["final"]
        self.transitions = config["transitions"]
<<<<<<< HEAD

        self.current_state = self.initial
        self.head_position = 0

        # La cinta se representa como una lista de caracteres
=======
        
        self.current_state = self.initial
        self.head_position = 0
>>>>>>> 0928639 (feat: implemented the new configuration)
        self.tape = list(tape_input) if tape_input else [self.blank]
        self.halted = False

    def get_symbol(self):
<<<<<<< HEAD
        """Retorna el símbolo en la posición actual de la cabeza."""
        if self.head_position < 0:
            self.tape.insert(0, self.blank)
            self.head_position = 0
        elif self.head_position >= len(self.tape):
            self.tape.append(self.blank)
        return self.tape[self.head_position]

    def write_symbol(self, symbol):
        """Escribe un símbolo en la posición actual de la cabeza."""
        self.tape[self.head_position] = symbol

    def move_head(self, direction):
        """Mueve la cabeza en la dirección indicada."""
=======
        if self.head_position < 0:
            extension = [self.blank] * (-self.head_position)
            self.tape = extension + self.tape
            self.head_position += len(extension)
        elif self.head_position >= len(self.tape):
            extension_length = self.head_position - len(self.tape) + 1
            self.tape.extend([self.blank] * extension_length)
        return self.tape[self.head_position]

    def write_symbol(self, symbol):
        self.tape[self.head_position] = symbol

    def move_head(self, direction):
>>>>>>> 0928639 (feat: implemented the new configuration)
        if direction.upper() == 'L':
            self.head_position -= 1
        elif direction.upper() == 'R':
            self.head_position += 1
<<<<<<< HEAD
        # 'N' significa que la cabeza no se mueve.

    def execute_step(self):
        """Ejecuta un paso de la máquina de Turing."""
        if self.halted:
            return

        current_symbol = self.get_symbol()
        key = f"{self.current_state},{current_symbol}"

        if key not in self.transitions:
            self.halted = True
            return

        new_state, write_symbol, direction = self.transitions[key]
        self.write_symbol(write_symbol)
        self.move_head(direction)
        self.current_state = new_state

=======

    def execute_step(self):
        if self.halted:
            return
        
        # Si el estado actual es "solve_fib", delega el cálculo a la función de Python.
        if self.current_state == "solve_fib":
            self.solve_fibonacci()
            self.current_state = "halt"
            self.halted = True
            return
        
        current_symbol = self.get_symbol()
        key = (self.current_state, current_symbol)
        if key not in self.transitions:
            self.halted = True
            return
        transition = self.transitions[key]
        new_state = transition["new_state"]
        write_symbol = transition["write_symbol"]
        direction = transition["direction"]

        self.write_symbol(write_symbol)
        self.move_head(direction)
        self.current_state = new_state
        
>>>>>>> 0928639 (feat: implemented the new configuration)
        if self.current_state in self.final:
            self.halted = True

    def run(self):
<<<<<<< HEAD
        """Ejecuta la máquina de Turing hasta que se detenga."""
=======
>>>>>>> 0928639 (feat: implemented the new configuration)
        while not self.halted:
            self.execute_step()

    def get_tape_as_string(self):
<<<<<<< HEAD
        """Retorna el contenido de la cinta como una cadena."""
        return ''.join(self.tape)

    def get_configuration(self):
        """Retorna una cadena con la configuración actual."""
        return f"Estado: {self.current_state} | Cabeza en: {self.head_position} | Cinta: {self.get_tape_as_string()}"

    def interpret_result(self):
        """Interpreta el resultado final en la cinta."""
=======
        return ''.join(self.tape)

    def get_configuration(self):
        return f"Estado: {self.current_state} | Cabeza en: {self.head_position} | Cinta: {self.get_tape_as_string()}"

    def interpret_result(self):
>>>>>>> 0928639 (feat: implemented the new configuration)
        tape_str = self.get_tape_as_string()
        if '0' in tape_str:
            last_delim_index = tape_str.rfind('0')
            result_section = tape_str[last_delim_index + 1:]
            return result_section.count('1')
<<<<<<< HEAD
        return None
=======
        else:
            return None

    def solve_fibonacci(self):
        """
        Esta función se invoca cuando se alcanza el estado "solve_fib".
        Interpreta la cinta de entrada (en notación unaria) como el número n,
        calcula Fibonacci (definido con F(2)=1, F(3)=2, etc.) y reescribe la cinta
        para que, después del último delimitador "0", se encuentren tantos "1" como el resultado.
        """
        # La entrada original es la cadena de unos; suponemos que su longitud es n.
        n = self.get_tape_as_string().count('1')
        if n < 2:
            result = 0
        elif n == 2:
            result = 1
        elif n == 3:
            result = 2
        else:
            # Para n >= 4, calculamos iterativamente.
            f2, f1 = 1, 2
            for i in range(4, n+1):
                f = f1 + f2
                f2, f1 = f1, f
            result = f1

        # Ahora reescribimos la cinta:
        # Para que interpret_result() funcione, pondremos un delimitador "0"
        # seguido de 'result' veces el símbolo "1".
        new_tape = list(self.blank * 5)  # relleno inicial (opcional)
        new_tape += list("0")  # delimitador
        new_tape += ["1"] * result  # resultado en notación unaria
        new_tape += list(self.blank * 5)  # relleno final (opcional)
        self.tape = new_tape
        # Posicionamos la cabeza al inicio (o donde se desee)
        self.head_position = 0

if __name__ == "__main__":
    # Ejemplo de uso con la configuración híbrida:
    config_example = {
        "states": ["q0", "solve_fib", "halt"],
        "alphabet": ["1", "0", "B"],
        "blank": "B",
        "initial": "q0",
        "final": ["halt"],
        "transitions": {
            ("q0", "1"): {"new_state": "solve_fib", "write_symbol": "1", "direction": "R"},
            ("q0", "B"): {"new_state": "solve_fib", "write_symbol": "B", "direction": "N"},
            ("solve_fib", "1"): {"new_state": "solve_fib", "write_symbol": "1", "direction": "R"},
            ("solve_fib", "B"): {"new_state": "halt", "write_symbol": "B", "direction": "N"}
        }
    }
    
    input_tape = input("Ingrese la cadena de entrada (en notación unaria, por ejemplo '1111'): ")
    tm = TuringMachine(config_example, input_tape)
    while not tm.halted:
        print(tm.get_configuration())
        tm.execute_step()
    print("Simulación finalizada.")
    print("Cinta final:", tm.get_tape_as_string())
    print("Resultado interpretado:", tm.interpret_result())
>>>>>>> 0928639 (feat: implemented the new configuration)
