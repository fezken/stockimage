import eel
from modules.keyword_checker import KeywordChecker
from modules.title_scraper import TitleScraper

# Initialize the KeywordChecker and TitleScraper
keyword_checker = KeywordChecker()
title_scraper = TitleScraper()

# Define the Eel-exposed functions
@eel.expose
def check_keywords(keywords: str, category: str = 'both', generative_ai: bool = False) -> str:
    result = keyword_checker.check_keywords(keywords, category, generative_ai)
    return result

@eel.expose
def scrape_titles(keywords: str, pages: str, sort: str = "nb_downloads", category: str = "both", generative_ai: bool = False) -> str:
    result = title_scraper.scrape_titles_to_csv(keywords, pages, sort, category, generative_ai)
    return result

def start_app() -> None:
    eel.init('web')
    eel.start('index.html', size=(800, 600))

if __name__ == "__main__":
    start_app()
