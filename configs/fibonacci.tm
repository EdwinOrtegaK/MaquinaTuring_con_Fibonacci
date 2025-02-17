# Máquina de Turing para calcular el n-ésimo número de Fibonacci en notación unaria.
# Convención:
#   - Entrada: n en unaria (ej. "111" = 3).
#   - Salida: F(n) en unaria.
#   - Símbolo en blanco: B.
#   - Delimitador: 0.
#
# Organización de la cinta tras inicialización (para n>=3):
#   [Contador = n-2 en 1’s] 0 [F(n–2)=1] 0 [F(n–1)=1] 0
#
# Proceso:
# Fase 1: Lectura y decremento de la entrada.
#   q0: Recorre la entrada.
#   q0_end: Al encontrar B, retrocede hasta encontrar un 1.
#           • Si lee B, se mueve a la izquierda (q0_end,B -> q0_end,B,L).
#           • Si lee 1, la borra y pasa a q1 (q0_end,1 -> q1,B,R).
#   q1: Se encarga de borrar la segunda 1.
#           • Si en q1 se lee B, se mueve a la izquierda (q1,B -> q1,B,L).
#           • Si se lee 1, la borra y pasa a q1a (q1,1 -> q1a,B,R).
#   q1a: Avanza por el contador.
#           • q1a,1 -> q1a,1,R
#           • q1a,B -> q2,0,R   (al llegar al final, escribe el primer delimitador 0)
#
# q_base: Caso base para n<=2. En ese caso, se escribe directamente el resultado (1) y se finaliza.
#
# Fase 2: Inicialización de registros (para n>=3).
#   q2: Escribe F(n–2)=1.
#   q3: Escribe el delimitador entre F(n–2) y F(n–1).
#   q4: Escribe F(n–1)=1.
#   q5: Escribe el delimitador final.
#
# Fase 3: Iteración (mientras el contador tenga al menos un '1').
#  3.1: Verificación y decremento del contador.
#       q6: Retrocede desde el final hacia el contador.
#           • q6,0 -> q6,0,L
#           • q6,1 -> q7,B,R    (borra una 1 y pasa a copiar)
#           • q6,B -> halt,B,R  (si el contador está vacío, finaliza)
#
#  3.2: Copia (Suma): Copiar TODOS los '1' de F(n–2) a la zona final de F(n–1).
#       q7: Se posiciona justo después del primer delimitador (inicio de F(n–2)).
#       q8: En F(n–2), busca un '1' sin marcar.
#            • q8,1 -> q9,X,R   (marca el '1' y pasa a copiar)
#            • q8,X -> q8,X,R   (salta los ya marcados)
#            • q8,0 -> q13,0,R  (si encuentra 0, ya no hay 1 sin marcar; pasa a desmarcar)
#       q9: Avanza en F(n–2) hasta el delimitador que separa F(n–2) y F(n–1).
#            • q9,1 -> q9,1,R
#            • q9,X -> q9,X,R
#            • q9,0 -> q10,0,R
#       q10: En F(n–1), avanza hasta el delimitador final.
#             • q10,1 -> q10,1,R
#             • q10,0 -> q11,0,R
#             • q10,B -> q11,B,L  (si encuentra B, transita a q11)
#       q11: Al encontrar el delimitador final en F(n–1), lo reemplaza por 1 (anexando la copia) y retrocede.
#             • q11,0 -> q11,1,L
#             • q11,1 -> q11,1,L
#             • q11,X -> q11,X,L
#             • q11,0 -> q12,0,L
#       q12: Retrocede hasta volver a la zona de F(n–2) para buscar el siguiente '1' sin marcar.
#             • q12,1 -> q12,1,L
#             • q12,X -> q12,X,L
#             • q12,B -> q8,B,R   (al alcanzar un B en la zona de F(n–2), regresa a q8)
#
#  3.3: Desmarcado:
#       q13: Convierte todas las X de F(n–2) en 1 y pasa a q14.
#             • q13,X -> q13,1,R
#             • q13,0 -> q14,0,R
#
#  3.4: Actualización de registros (simplificada):
#       q14: Borra el contenido de F(n–2) (simulando que se descarta) para que la antigua F(n–1)
#            sirva de nueva F(n–2).
#             • q14,1 -> q14,B,R
#             • q14,0 -> q15,0,R
#       q15: Reestructura la cinta (simplificado) y reposiciona la cabeza en la zona del contador para la siguiente iteración.
#             • q15,B -> q15,0,L
#             • q15,0 -> q15,0,L
#             • q15,B -> q6,B,R
#
# Fase 4: Finalización.
#   Cuando el contador esté vacío, la máquina transita a halt.
#
# Auto-transición en halt (para evitar estados indefinidos):
#   halt, B -> halt, B, N

states: q0,q0_end,q1,q1a,q_base,q2,q3,q4,q5,q6,q7,q8,q9,q10,q11,q12,q13,q14,q15,halt
alphabet: 1,0,B,X
blank: B
initial: q0
final: halt

# --- Fase 1: Lectura y decremento de la entrada ---
transition: q0,1 -> q0,1,R
transition: q0,B -> q0_end,B,L

# En q0_end: Si encuentra B, sigue retrocediendo; si encuentra 1, borra y pasa a q1.
transition: q0_end,B -> q0_end,B,L
transition: q0_end,1 -> q1,B,R

# q1: Se espera borrar la segunda 1. Si encuentra B, retrocede; si encuentra 1, borra y pasa a q1a.
transition: q1,B -> q1,B,L
transition: q1,1 -> q1a,B,R

# q1a: Avanza por el contador.
transition: q1a,1 -> q1a,1,R
transition: q1a,B -> q2,0,R   # Al llegar al final del contador, escribe el primer delimitador '0'

# --- q_base: Caso base para n<=2 (no se iterará) ---
transition: q_base,B -> halt,B,N

# --- Fase 2: Inicialización de registros (para n>=3) ---
transition: q2,B -> q3,1,R           # Escribe F(n–2)=1
transition: q3,B -> q4,0,R           # Escribe el delimitador entre F(n–2) y F(n–1)
transition: q4,B -> q5,1,R           # Escribe F(n–1)=1
transition: q5,B -> q_move,B,L   # Termina inicialización y mueve la cabeza a la izquierda
transition: q_move,1 -> q_move,1,L  
transition: q_move,0 -> q6,0,R    # Cuando encuentra el delimitador, pasa a q6 (verificación del contador)
transition: q_move,B -> q_move,B,L

# --- Fase 3.1: Verificación y decremento del contador ---
transition: q6,0 -> q6,0,L           # Retrocede sobre el delimitador final
transition: q6,1 -> q7,B,R           # Si encuentra '1' en el contador, la borra y pasa a q7
transition: q6,B -> halt,B,R         # Si el contador está vacío, finaliza

# --- Fase 3.2: Copia (Suma): Copiar TODOS los '1' de F(n–2) a F(n–1) ---
# q7: Posicionarse justo después del primer delimitador (inicio de F(n–2))
transition: q7,0 -> q8,0,R

# q8: En F(n–2), buscar un '1' sin marcar.
transition: q8,X -> q8,X,R           # Salta los ya marcados.
transition: q8,0 -> q_check,0,L  # En lugar de avanzar, primero verifica en q_check.
transition: q8,1 -> q9,X,R           # Si encuentra 1, lo marca y continúa la copia

# q_check: Verifica si en la sección F(n–2) quedan '1' sin marcar.
transition: q_check,1 -> q8,1,R        # Si aún hay 1 sin marcar, regresa a q8.
transition: q_check,X -> q_check,X,L   # Sigue retrocediendo si encuentra X.
transition: q_check,0 -> q13,0,R       # Solo avanza a q13 si no quedan 1 sin marcar.

# q9: Desde F(n–2), avanza hasta el delimitador que separa F(n–2) y F(n–1).
transition: q9,1 -> q9,1,R
transition: q9,X -> q9,X,R
transition: q9,0 -> q10,0,R

# q10: En F(n–1), avanza hasta el delimitador final.
transition: q10,1 -> q10,1,R
transition: q10,0 -> q11,0,R
transition: q10,B -> q11,B,L         # Si encuentra B (espacio en blanco), transita a q11

# q11: Al encontrar el delimitador final en F(n–1), lo reemplaza por 1 (anexando la copia) y retrocede.
transition: q11,0 -> q11,1,L
transition: q11,1 -> q11,1,L
transition: q11,X -> q11,X,L
transition: q11,0 -> q12,0,L

# q12: Retrocede hasta volver a la zona de F(n–2) para buscar el siguiente '1' sin marcar.
transition: q12,1 -> q12,1,L
transition: q12,X -> q12,X,L
transition: q12,B -> q8,B,R         # Al alcanzar el borde (B) de F(n–2), regresa a q8.

# --- Fase 3.3: Desmarcado ---
# q13: Convierte todas las X en 1 en F(n–2) y pasa a la actualización.
transition: q13,X -> q13,1,R
transition: q13,0 -> q14,0,R

# --- Fase 3.4: Actualización de registros (simplificada) ---
# q14: Borra el contenido de F(n–2) (simulando que se descarta) para que la antigua F(n–1) sirva de nueva F(n–2).
transition: q14,1 -> q14,B,R
transition: q14,0 -> q15,0,R

# q15: Reestructura la cinta (simplificado) y reposiciona la cabeza en la zona del contador para la siguiente iteración.
transition: q15,0 -> q15,0,L
transition: q15,B -> q0,B,R

# --- Auto-transición para halt (evitar estados indefinidos) ---
transition: halt,B -> halt,B,N
