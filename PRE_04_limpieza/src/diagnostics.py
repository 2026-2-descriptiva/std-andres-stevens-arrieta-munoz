import pandas as pd

OUTPUT_FILE = "PRE_04_limpieza/submission/ventas.csv"


def main():
    df = pd.read_csv(OUTPUT_FILE)
    series = df["weight"]

    # Ayuda a ver si hay fechas duplicadas, pero no es necesario para el resultado final
    # series = series.str.replace(r"\d", "d", regex=True)
    # series = series.drop_duplicates()


    series = series.sort_values()
    series = series.drop_duplicates()

    print(series)
    print(len(series))


if __name__ == "__main__":
    main()