class GeneralScraperException(Exception):
    """General exception for the scraper, could have multiple reasons"""

class TitleNotFound(Exception):
    """Title was not found on the website"""