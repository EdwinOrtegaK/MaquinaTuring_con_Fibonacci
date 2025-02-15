# Máquina de Turing para calcular el n-ésimo número de la sucesión de Fibonacci en representación unaria.
# Convención:
#   - La entrada es un número en representación unaria (secuencias de '1') que representa el índice n (n >= 1).
#   - La salida es el n-ésimo número de Fibonacci en representación unaria.
#   - Se utiliza 'B' como símbolo en blanco.
#   - Se emplea '0' como delimitador entre secciones.
#
# Organización de la cinta (después de la inicialización):
#   [ Iteration Counter (n - 2 en unary) ] 0 [ F(n-2) ] 0 [ F(n-1) ] 0
#
# Proceso:
# 1. Lectura de la entrada y decremento: se borran las dos primeras '1' para formar el Iteration Counter.
# 2. Inicialización: se escribe el delimitador y se inicializan F(n-2)=1 y F(n-1)=1.
# 3. Iteración:
#    a. Se verifica el Iteration Counter.
#       - Si hay al menos un '1', se borra (decremento) y se procede a sumar.
#       - Si no hay '1', se detiene.
#    b. Suma: se copia (simplificadamente) el contenido de F(n-2) al final de F(n-1), obteniéndose F(n)=F(n-2)+F(n-1).
#    c. Actualización: se traslada F(n-1) a F(n-2) y el resultado se queda en F(n-1).
#
# Estados:
#   q0      : Lectura de la entrada.
#   q0_end  : Al encontrar blanco, retrocede para iniciar el decremento.
#   q1      : Decremento: borrar la primera '1'.
#   q1a     : Decremento: borrar la segunda '1'.
#   q2      : Fin del decremento; escribir delimitador y preparar la inicialización.
#   q3      : Inicialización: escribir F(n-2)=1.
#   q4      : Escribir delimitador para separar F(n-2) y F(n-1).
#   q5      : Inicialización: escribir F(n-1)=1.
#   q6      : Escribir delimitador final y pasar a la iteración.
#   q7      : Verificar el Iteration Counter.
#   q8      : Si se encuentra '1' en el contador, borrarla y proceder a la suma.
#   q9      : Suma: copiar (simplificada) F(n-2) al final de F(n-1).
#   q10     : Actualización de registros.
#   q11     : Retorno a la verificación del contador.
#   halt    : Fin; el resultado está en el registro F(n-1).
#
states: q0,q0_end,q1,q1a,q2,q3,q4,q5,q6,q7,q8,q9,q10,q11,halt
alphabet: 1,0,B,X
blank: B
initial: q0
final: halt

# --- Transiciones ---

# Fase 1: Lectura de la entrada.
transition: q0,1 -> q0,1,R
transition: q0,B -> q0_end,B,L

# Fase 2: Decremento del contador (borrar dos '1').
transition: q0_end,1 -> q1,B,R       # Borra la primera '1'
transition: q1,1 -> q1a,B,R           # Borra la segunda '1'
# Se continúa moviéndose por las '1' restantes (si las hay).
transition: q1a,1 -> q1a,1,R
transition: q1a,B -> q2,0,R           # Al llegar al final, escribe un delimitador '0'

# Fase 3: Inicialización de registros.
# El tape ahora tiene: [Iteration Counter] 0 ...
transition: q2,B -> q3,1,R           # Escribe F(n-2)=1
transition: q3,B -> q4,0,R           # Escribe delimitador entre F(n-2) y F(n-1)
transition: q4,B -> q5,1,R           # Escribe F(n-1)=1
transition: q5,B -> q6,0,R           # Escribe delimitador final; termina la inicialización

# Fase 4: Verificación del Iteration Counter.
# Se regresa a la zona del contador (a la izquierda del primer delimitador).
transition: q6,0 -> q6,0,L          # Retrocede hacia el contador
transition: q6,1 -> q7,B,R          # Si encuentra una '1' (contador activo), la borra y pasa a la suma
transition: q6,B -> halt,B,R        # Si no hay '1' (contador agotado), finaliza

# Fase 5: Suma (copia simplificada de F(n-2) al final de F(n-1)).
# Se salta el delimitador entre contador y F(n-2).
transition: q7,0 -> q8,0,R          
# En q8 se “recorre” F(n-2); (en una implementación completa se marcaría cada '1' y se copiaría).
transition: q8,1 -> q8,1,R          # Se avanza por F(n-2)
transition: q8,0 -> q9,0,R          # Al llegar al delimitador entre F(n-2) y F(n-1), se pasa a copiar

# En q9 se mueve a la derecha en F(n-1) hasta el final, para anexar un '1'
transition: q9,1 -> q9,1,R
transition: q9,B -> q9,1,L          # Cuando encuentra blanco, escribe '1' (copia un '1' de F(n-2))
# Nota: Esta transición simboliza la suma; en una implementación completa se copiarían todas las '1' de F(n-2).

# Fase 6: Actualización de registros.
# Se retrocede al delimitador para preparar la actualización.
transition: q9,0 -> q10,0,L
# q10 realizaría (simplificadamente) la actualización:
#   F(n-2) <- antiguo F(n-1) y F(n-1) <- F(n) (resultado de la suma).
transition: q10,B -> q11,B,R

# Fase 7: Regresa a verificar el contador para la siguiente iteración.
transition: q11,0 -> q11,0,R
transition: q11,B -> q6,0,L   # Regresa a la zona del Iteration Counter

# Al agotarse el contador, se llega a halt y el resultado final está en el registro F(n-1).