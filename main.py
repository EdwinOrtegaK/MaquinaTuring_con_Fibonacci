import sys
import time
import csv
from src.parser import parse_configuration_json
from src.turing_machine import TuringMachine

def main():
    # 1. Cargar el archivo de configuración de la máquina (usamos el híbrido)
    config_file = "configs/fib_hybrid.json"
    try:
        config = parse_configuration_json(config_file)
    except Exception as e:
        print(f"Error al leer la configuración: {e}")
        sys.exit(1)
    
    # 2. Solicitar al usuario la cadena de entrada (en notación unaria)
    tape_input = input("Ingrese la cadena de entrada (según la convención definida): ")

    # 3. Crear la instancia de la máquina de Turing con la configuración y la cadena de entrada
    machine = TuringMachine(config, tape_input)

    # 4. Simulación paso a paso de la ejecución de la máquina
    start_time = time.time()

    step_count = 0
    while not machine.halted:
        print(f"\nPaso {step_count}:")
        print(f"Estado actual: {machine.current_state}")
        print(f"Cabeza en la posición: {machine.head_position}")
        print(f"Cinta: {machine.get_tape_as_string()}")
        
        machine.execute_step()
        step_count += 1

    end_time = time.time()
    execution_time = end_time - start_time 

    # 5. Mostrar el resultado final
    print("\nSimulación finalizada.")
    print(f"Estado final: {machine.current_state}")
    print(f"Cinta final: {machine.get_tape_as_string()}")
    resultado = machine.interpret_result()
    print(f"Resultado interpretado: {resultado}")
    print(f"\nTiempo de ejecución: {execution_time:.6f} segundos")

    # 6. Guardar los tiempos en un archivo CSV
    csv_filename = "analysis/execution_times.csv"
    try:
        with open(csv_filename, mode="a", newline="") as file:
            writer = csv.writer(file)
            # Si el archivo está vacío, escribir encabezados
            if file.tell() == 0:
                writer.writerow(["Input Length", "Execution Time (s)"])
            writer.writerow([len(tape_input), execution_time])
        print(f"Tiempo de ejecución guardado en {csv_filename}")
    except Exception as e:
        print(f"Error al guardar el tiempo de ejecución: {e}")

if __name__ == "__main__":
    main()
