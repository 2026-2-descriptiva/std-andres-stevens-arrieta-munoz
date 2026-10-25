def pregunta_01():
    """
    Las frases de este laboratorio no están en una tabla, sino en miles de
    archivos de texto organizados en carpetas. Dentro de `data/` hay dos
    carpetas, `train/` y `test/`, y cada una contiene las carpetas
    `negative/`, `neutral/` y `positive/`. Cada archivo `.txt` contiene una
    frase, y la carpeta donde se encuentra indica su sentimiento.

    Su tarea es construir un dataset para cada división y guardarlo en:

    - `submission/train_dataset.csv`
    - `submission/test_dataset.csv`

    Cada archivo debe tener dos columnas: `phrase`, con el texto de la frase,
    y `target`, con el nombre de la carpeta de sentimiento (`negative`,
    `neutral` o `positive`). Recorra las carpetas y los archivos en orden
    alfabético, de modo que el resultado sea siempre el mismo. No guarde el
    índice de Pandas en el CSV.

    Ejemplo del formato de cada archivo:

        phrase,target
        "The real estate company posted a net loss ...",negative
        ...
        "Cardona slowed her vehicle , turned around ...",neutral
        ...
    """

    import re
    from pathlib import Path
    import pandas as pd

    DATA_DIRECTORY = Path(__file__).resolve().parent.parent / "data"
    TRAIN_DIRECTORY = DATA_DIRECTORY / "train"
    TEST_DIRECTORY = DATA_DIRECTORY / "test"
    SUBMISSION_DIRECTORY = Path(__file__).resolve().parent.parent / "submission"

    def build_dataset(directory: Path) -> pd.DataFrame:
        data = []
        for sentiment_dir in sorted(directory.iterdir()):
            if sentiment_dir.is_dir():
                sentiment = sentiment_dir.name
                for file_path in sorted(sentiment_dir.glob("*.txt")):
                    phrase = file_path.read_text(encoding="utf-8").strip()
                    data.append({"phrase": phrase, "target": sentiment})
        return pd.DataFrame(data)

    train_dataset = build_dataset(TRAIN_DIRECTORY)
    test_dataset = build_dataset(TEST_DIRECTORY)

    train_dataset.to_csv(SUBMISSION_DIRECTORY / "train_dataset.csv", index=False)
    test_dataset.to_csv(SUBMISSION_DIRECTORY / "test_dataset.csv", index=False) 


if __name__ == "__main__":
    pregunta_01()

