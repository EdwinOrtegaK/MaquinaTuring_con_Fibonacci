import sys
from src.parser import parse_configuration
#from src.turing_machine import TuringMachine

def main():
    # 1. Cargar el archivo de configuración de la máquina
    config_file = "configs/fibonacci.tm"
    try:
        config = parse_configuration(config_file)
    except Exception as e:
        print(f"Error al leer la configuración: {e}")
        sys.exit(1)
    
    # 2. Solicitar al usuario la cadena de entrada
    tape_input = input("Ingrese la cadena de entrada (según la convención definida): ")

    # 3. Crear la instancia de la máquina de Turing con la configuración y la cadena de entrada
    machine = TuringMachine(config, tape_input)

    # 4. Simulación paso a paso de la ejecución de la máquina
    step_count = 0
    while not machine.halted:
        print(f"\nPaso {step_count}:")
        print(f"Estado actual: {machine.current_state}")
        print(f"Cabeza en la posición: {machine.head_position}")
        print(f"Cinta: {machine.get_tape_as_string()}")
        
        # Ejecuta un paso de la máquina
        machine.execute_step()
        step_count += 1

    # 5. Mostrar el resultado final
    print("\nSimulación finalizada.")
    print(f"Estado final: {machine.current_state}")
    print(f"Cinta final: {machine.get_tape_as_string()}")
    print(f"Resultado interpretado: {machine.interpret_result()}")

if __name__ == "__main__":
    main()
