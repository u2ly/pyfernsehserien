from typing import List

import json
import re
from bs4 import BeautifulSoup
from datetime import datetime

from .utils import normalize_text

class Parser:
    def __init__(self, html: bytes) -> None:
        html = html.decode("utf-8")
        
        self.soup = BeautifulSoup(html, "html.parser")
        self.beacon = self.get_beacon()
        
        self.is_movie = self.beacon["seite"] == "spielfilm"
        
    def get_beacon(self) -> dict:
        for script in self.soup.find_all("script"):
            if "var fsBeacon2022" in str(script):
                match = re.search(r"var fsBeacon2022=JSON\.parse\(\s*'(.*?)'\s*\);", script.text, re.DOTALL)
                
                if match:
                    return json.loads(match.group(1))
                
        return {}
    
    def get_release_dates(self) -> List[dict]:
        release_dates = []
        
        for element in self.soup.find_all("ea-angabe"):
            title = element.find("ea-angabe-titel").text
            
            if title in ("Originalsprache"): # wtf?
                continue
            
            release_dates.append(
                {
                    "title": title,
                    "date": self._extract_date(element.find("ea-angabe-datum").text),
                    **(
                        {"extra": element.find("ea-angabe-anmerkung").text}
                        if element.find("ea-angabe-anmerkung")
                        else {}
                    ),
                    **(
                        {"channel": element.find("ea-angabe-sender").text}
                        if element.find("ea-angabe-sender")
                        else {}
                    )
                }
            )
            
        return release_dates
    
    def get_countries(self) -> List[str]:
        return [
            country.text
            for country in self.soup.find_all("abbr", itemprop="countryOfOrigin")
        ]

    def get_credits(self) -> List[dict]:
        credits = []
        
        parent_el = self.soup.find("ul", class_="cast-crew-rest")
        if not parent_el:
            parent_el = self.soup.find("ul", class_="cast-crew")
        if not parent_el:
            return []
        
        for item in parent_el.find_all("li"):
            image = item.find("figure", class_="fs-picture").find("meta", itemprop="image")
            
            credits.append(
                {
                    "name": item.find("dt", itemprop="name").text,
                    "role": item.find("dd").text.strip() if item.find("dd").text.strip() else None,
                    "image_url": image.get("content") if image else None,
                    "profile_url": item.find("a").get("href"),
                }
            )
            
        return credits
    
    def get_release_year(self):
        cos = [c for c in self.soup.find_all("abbr", itemprop="countryOfOrigin")][-1]
        parent = cos.parent        
        
        years = re.findall(r'(\b\d{4})-?(\d{4})?\b', str(parent).split(cos.text)[-1])
        
        if self.is_movie:
            return int(years[0][0])
        
        return {
            "year": int(years[0][0]),
            "end": int(years[0][1]) if years[0][1] else None
        }
        
    def get_runtime(self):
        cos = [c for c in self.soup.find_all("abbr", itemprop="countryOfOrigin")][-1]
        parent = cos.parent        

        runtime = re.search(r"\(.*?(\d+)\sMin\.\)", str(parent))
        
        return int(runtime.group(1))
        
    def get_plot(self):
        if self.is_movie:
            plot = self.soup.find("div", class_="episode-output-inhalt").find("p").text
        else:
            plot = self.soup.find("div", itemprop="description").text
            
        return normalize_text(plot)
    
    def get_genres(self):
        return [
            x.text
            for x in self.soup.find("ul", class_="genrepillen").find_all("li")
        ]
        
    
    def _extract_date(self, date: str) -> str:
        date = re.sub(r"[^\d.-]", "", date)
        
        if not date:
            return None
        
        return datetime.strptime(date, "%d.%m.%Y").isoformat().split("T")[0]