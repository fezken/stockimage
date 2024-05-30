import eel
from modules.keyword_checker import KeywordChecker
from modules.title_scraper import TitleScraper
from modules.analysis_module import AnalysisModule

# Initialize the modules
keyword_checker = KeywordChecker()
title_scraper = TitleScraper()
analysis_module = AnalysisModule()

@eel.expose
def check_keywords(keywords: str, category: str = 'both', generative_ai: bool = False) -> str:
    result = keyword_checker.check_keywords(keywords, category, generative_ai)
    return result

@eel.expose
def scrape_titles(keywords: str, pages: str, sort: str = "nb_downloads", category: str = "both", generative_ai: bool = False) -> str:
    result = title_scraper.scrape_titles_to_csv(keywords, pages, sort, category, generative_ai)
    return result

@eel.expose
def scrape_titles_by_creator(creator_ids: str, pages: str) -> str:
    result = title_scraper.scrape_titles_by_creator_to_csv(creator_ids, pages)
    return result

@eel.expose
def perform_analysis(method: str, count: int = 20) -> str:
    result = analysis_module.perform_analysis(method, count)
    return result

@eel.expose
def automate_process(keywords: str, category: str = 'both', generative_ai: bool = False) -> str:
    keyword_checker.check_keywords(keywords, category, generative_ai)
    analysis_module.perform_analysis('lowest')
    top_keywords = analysis_module.get_top_keywords()
    result = title_scraper.scrape_titles_to_csv(top_keywords, '1-3', 'nb_downloads', category, generative_ai)
    return result

def start_app() -> None:
    eel.init('web')
    eel.start('index.html', size=(800, 600))

if __name__ == "__main__":
    start_app()
