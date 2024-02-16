# pyfernsehserien

Python package for scraping data from fernsehserien.de. It currently supports only searching and retrieving title information. I haven't implemented additional features since they aren't needed for my purposes. Feel free to contribute to or fork this project. Also, note that I didn't put much effort into testing, so don't expect much.

## Installation

You can install pyfernsehserien via pip:

```bash
pip install pyfernsehserien
```

## Usage

Here's a basic example demonstrating how to use this package:

```python
from pyfernsehserien import Fernsehserien

# Initialize Fernsehserien object
fs = Fernsehserien()

# Search for movies/series
results = fs.search("Rick and Morty")["items"]

# Get detailed information about the first result
info = fs.get(results[0]["slug"])

print(info)
```

The output will look something like this:

```json
{
    "id": 24036,
    "slug": "/rick-and-morty",
    "title": "Rick and Morty",
    "type": "show",
    "genres": [
        "Comedy",
        "Science-Fiction",
        "Zeichentrick"
    ],
    "original_language": "en",
    "overview": "Im Mittelpunkt der Serie stehen der Teenager Morty und seine Familie. Morty wird von den üblichen Highschool-Problemen geplagt. Sein Großvater Rick ist ein genialer Wissenschaftler mit Alkoholproblem, der ihn immer wieder zu riskanten Abenteuern anstiftet, bei denen es auch schon mal zum Kontakt mit Aliens kommt. Vater Jeff sieht Rick als negativen Einfluss für seinen Sohn. Zur Familie zählen außerdem die dominante Mutter Beth und Mortys ältere Schwester Summer. (Text: MB)",
    "release_year": {
        "year": 2013,
        "end": null
    },
    "number_of_seasons": 7,
    "number_of_episodes": 71,
    "release_dates": [
        {
            "title": "Deutsche TV-Premiere",
            "date": "2014-11-29",
            "channel": "TNT Serie"
        },
        {
            "title": "Free-TV-Premiere",
            "date": "2016-09-06",
            "channel": "Rocket Beans TV"
        },
        {
            "title": "Original-TV-Premiere",
            "date": "2013-12-02",
            "channel": "adult swim"
        }
    ],
    "origin_countries": [
        "USA"
    ],
    "credits": [
        {
            "name": "Kari Wahlgren",
            "role": null,
            "image_url": "https://bilder.fernsehserien.de/gfx/person_1000/k/kari-wahlgren.jpg",
            "profile_url": "/kari-wahlgren/filmografie"
        },
        ...
    ]
}
```

## License

This project is licensed under the terms of [GNU General Public License, Version 3.0](LICENSE).