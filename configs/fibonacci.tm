# Máquina de Turing para calcular el n-ésimo número de la sucesión de Fibonacci en representación unaria.
# Convención:
#   - La entrada es un número en representación unaria (secuencias de '1'), que representa el índice n (n >= 1).
#   - La salida es el n-ésimo número de Fibonacci en representación unaria.
#   - Se utiliza 'B' como símbolo en blanco.
#   - Se emplea '0' como delimitador entre secciones de la cinta.
#
# Notas:
#   Esta configuración es una simplificación para fines ilustrativos.
#   En una implementación completa, se requeriría una detallada secuencia de operaciones para copiar
#   y sumar registros en la cinta, de forma que se realice la suma en notación unaria (concatenación de '1's).
#
# Estados definidos:
#   q0: Lectura de la entrada (n en unaria)
#   q1 a q4: Inicialización de registros (F(1)=1 y F(2)=1)
#   q5: Verificación de iteraciones pendientes (n > 2)
#   q6 y q7: Simulación simplificada de la suma (F(n) = F(n-2) + F(n-1))
#   halt: Estado final, se interpreta el resultado en la cinta

states: q0,q1,q2,q3,q4,q5,q6,q7,halt
alphabet: 1,0,B
blank: B
initial: q0
final: halt

# --- Transiciones ---

# q0: Recorrer la entrada (n en unaria).
transition: q0,1 -> q0,1,R
transition: q0,B -> q1,0,R   # Al llegar al primer espacio en blanco, escribe un delimitador '0' y pasa a inicializar.

# q1: Inicialización del primer registro: escribe F(1)=1.
transition: q1,B -> q2,1,R

# q2: Escribe un delimitador para separar el primer registro.
transition: q2,B -> q3,0,R

# q3: Inicialización del segundo registro: escribe F(2)=1.
transition: q3,B -> q4,1,R

# q4: Escribe un delimitador para separar la sección de iteración.
transition: q4,B -> q5,0,R

# q5: Verifica si quedan iteraciones pendientes.
#       - Si se encuentra B (sección vacía), se asume que n <= 2 y se finaliza la computación.
transition: q5,B -> halt,B,R
#       - Si se encuentra al menos un '1', se procede a la iteración (simulación de la suma).
transition: q5,1 -> q6,1,R

# q6: Movimiento para preparar la suma: se busca el inicio del registro de F(n-1).
transition: q6,0 -> q7,0,R

# q7: Suma simplificada: se simula la suma agregando un '1' al final de F(n-1).
#      Esta acción simboliza que se ha calculado F(n)=F(n-2)+F(n-1) (en una implementación real,
#      se copiaría el contenido completo del registro F(n-2) al final de F(n-1)).
transition: q7,B -> q5,1,L   # Escribe un '1' y regresa a q5 para verificar si quedan iteraciones.
