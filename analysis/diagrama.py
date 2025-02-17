import matplotlib.pyplot as plt
import networkx as nx
import json

# Cargar el archivo JSON de configuración de la máquina de Turing
with open("configs/fibonacci.json", "r") as file:
    turing_machine_config = json.load(file)

# Extraer estados y transiciones
states = turing_machine_config["states"]
transitions = turing_machine_config["transitions"]

# Crear un grafo dirigido
G = nx.DiGraph()

# Agregar nodos (estados)
for state in states:
    G.add_node(state)

# Agregar aristas (transiciones) con etiquetas
for key, value in transitions.items():
    try:
        current_state, read_symbol = key.split(",")
        next_state, write_symbol, move_direction = value
        edge_label = f"{read_symbol}/{write_symbol},{move_direction}"
        G.add_edge(current_state, next_state, label=edge_label)
    except Exception as e:
        print(f"Error procesando transición {key}: {e}")

# Dibujar el grafo con una mejor distribución de nodos
plt.figure(figsize=(18, 14))
pos = nx.spring_layout(G, seed=42)  # Alternativa para mejorar la organización de nodos
nx.draw(G, pos, with_labels=True, node_color="lightblue", edge_color="gray", node_size=4000, font_size=12)
edge_labels = nx.get_edge_attributes(G, "label")
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)

# Guardar la imagen
plt.savefig("analysis/turing_machine_fibonacci_diagram.png", dpi=300, bbox_inches="tight")

# Mostrar el diagrama generado
plt.show()

print("Diagrama generado y guardado como 'turing_machine_fibonacci_diagram.png'.")
