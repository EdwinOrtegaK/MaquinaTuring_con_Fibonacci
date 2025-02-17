class TuringMachine:
    def __init__(self, config, tape_input):
        """
        Inicializa la máquina de Turing usando la configuración JSON y la entrada.

        Args:
            config (dict): Configuración JSON con los estados, alfabeto, transiciones, etc.
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

        # La cinta se representa como una lista de caracteres
        self.tape = list(tape_input) if tape_input else [self.blank]
        self.halted = False

    def get_symbol(self):
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
        if direction.upper() == 'L':
            self.head_position -= 1
        elif direction.upper() == 'R':
            self.head_position += 1
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
        """Retorna una cadena con la configuración actual."""
        return f"Estado: {self.current_state} | Cabeza en: {self.head_position} | Cinta: {self.get_tape_as_string()}"

    def interpret_result(self):
        """Interpreta el resultado final en la cinta."""
        tape_str = self.get_tape_as_string()
        if '0' in tape_str:
            last_delim_index = tape_str.rfind('0')
            result_section = tape_str[last_delim_index + 1:]
            return result_section.count('1')
        return None
