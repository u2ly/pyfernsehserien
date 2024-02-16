import re

from .exceptions import *
from .parser import Parser
from .session import Session


class Fernsehserien:
    def __init__(self) -> None:
        self.session = Session()

    def search(self, query: str) -> dict:
        response = self.session.post(
            url="https://www.fernsehserien.de/fastsearch",
            json={"suchwort": query},
            headers={"X-Csrf-Token": self._get_csrf_token()},
        ).json()

        items = []

        for item in response["items"]:
            country, year = item["l"].split(" ")

            items.append(
                {
                    "title": item["t"],
                    "slug": item["s"],
                    "type": self._map_type(item["a"]),
                    "origin": country.lower(),
                    "release_year": {
                        "year": int(year.split("-")[0][:-1]),
                        "end": (
                            int(year.split("-")[1])
                            if len(year.split("-")) == 2
                            else None
                        ),
                    },
                    "channel": item["c"],
                    "color_theme": item["f"],
                    "poster": item["b"],
                }
            )

        return {
            "has_more": response["mehr"],
            "total_count": response["count"],
            "items": items,
        }

    def get(self, slug: str) -> dict:
        html = self.session.get(
            f"https://www.fernsehserien.de/{slug}",
        )

        if html.status_code == 404:
            raise TitleNotFound(f"Title with slug '{slug}' not found")

        parser = Parser(html.content)

        type_ = self._map_type(parser.beacon["seite"])

        return {
            "id": int(parser.beacon["id"]),
            "slug": parser.beacon["href"],
            "title": parser.soup.find("meta", property="og:title").get("content"),
            "type": type_,
            "genres": parser.get_genres(),
            "original_language": parser.soup.find("meta", itemprop="inLanguage").get("content"),
            "overview": parser.get_plot(),
            "release_year": parser.get_release_year(),
            **(
                {
                    "number_of_seasons": int(parser.soup.find("span", itemprop="numberOfSeasons").text) if parser.soup.find("span", itemprop="numberOfSeasons") else None,
                    "number_of_episodes": int(parser.soup.find("span", itemprop="numberOfEpisodes").text) if parser.soup.find("span", itemprop="numberOfEpisodes") else None,
                }
                if not parser.is_movie
                else {
                    "runtime": 0,
                }
            ),
            "release_dates": parser.get_release_dates(),
            "origin_countries": parser.get_countries(),
            "credits": parser.get_credits(),
        }

    # Helper methods

    def _get_csrf_token(self) -> str:
        r = self.session.get(
            # Dummy request, chose the login page because it should be small.
            # This also sets cookies if not already set.
            "https://www.fernsehserien.de/meins/login"
        ).text

        csrf = re.search(r'var csrfToken="([^"]+)"', r)

        if csrf:
            return csrf.group(1)

        raise Exception("Could not find CSRF token")

    @staticmethod
    def _map_type(type: str) -> str:
        MAP = {"sg": "show", "sm": "movie", "serie-infos": "show", "spielfilm": "movie"}

        return MAP.get(type, type)