import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

CSV_FILENAME = "analysis/execution_times.csv"

def mostrar_listado_pruebas():
    """Carga y muestra el listado de pruebas desde el CSV."""
    try:
        df = pd.read_csv(CSV_FILENAME)
        print("\n Listado de entradas de prueba:")
        print(df.to_string(index=False))  # Muestra sin índice
    except Exception as e:
        print(f" Error al leer el archivo CSV: {e}")

def graficar_dispersion():
    """Genera un diagrama de dispersión de tiempos de ejecución."""
    try:
        df = pd.read_csv(CSV_FILENAME)
        x = df["Input Length"]
        y = df["Execution Time (s)"]

        plt.scatter(x, y, label="Datos experimentales", alpha=0.7)
        plt.xlabel("Tamaño de la entrada")
        plt.ylabel("Tiempo de ejecución (s)")
        plt.title("Diagrama de dispersión de tiempos de ejecución")
        plt.legend()
        plt.grid()
        plt.show()

    except Exception as e:
        print(f" Error al leer el CSV para graficar: {e}")

def ajustar_regresion_polinomial():
    """Ajusta una regresión polinomial y grafica la tendencia."""
    try:
        df = pd.read_csv(CSV_FILENAME)
        x = df["Input Length"].values
        y = df["Execution Time (s)"].values

        # Ajustar una regresión polinomial de grado 2
        coef = np.polyfit(x, y, deg=2)
        polinomio = np.poly1d(coef)

        # Generar valores para la curva
        x_fit = np.linspace(min(x), max(x), 100)
        y_fit = polinomio(x_fit)

        # Graficar datos y ajuste
        plt.scatter(x, y, label="Datos experimentales", alpha=0.7)
        plt.plot(x_fit, y_fit, color='red', label="Ajuste polinomial (grado 2)")
        plt.xlabel("Tamaño de la entrada")
        plt.ylabel("Tiempo de ejecución (s)")
        plt.title("Regresión polinomial sobre tiempos de ejecución")
        plt.legend()
        plt.grid()
        plt.show()

        print(f"\n Coeficientes del polinomio ajustado: {coef}")

    except Exception as e:
        print(f" Error en la regresión polinomial: {e}")

if __name__ == "__main__":
    print("\n--- ANÁLISIS EMPÍRICO ---")
    mostrar_listado_pruebas()
    graficar_dispersion()
    ajustar_regresion_polinomial()
