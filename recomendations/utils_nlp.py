from pathlib import Path


def get_stopwords():
    stopwords = set()
    path = Path(__file__).resolve().parent / '..' / 'resources' / 'stopwords' / 'stopwords.txt'
    with path.open() as f:
        for line in f:
            if line != '':
                stopwords.add(line.strip().lower())
    return stopwords
