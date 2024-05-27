from .base_module import BaseModule
import pandas as pd
from utils.file_utils import FileUtils
from datetime import datetime

class AnalysisModule(BaseModule):
    def __init__(self) -> None:
        super().__init__()
        self.filepath = 'keyword_search_results.csv'

    def read_data(self) -> pd.DataFrame:
        try:
            data = pd.read_csv(self.filepath)
            self.log(f"Successfully read data from {self.filepath}")
            return data
        except Exception as e:
            self.log(f"Error reading data from {self.filepath}: {e}")
            return pd.DataFrame()

    def save_analysis_to_csv(self, data: pd.DataFrame, filename: str) -> None:
        try:
            data.to_csv(filename, index=False)
            self.log(f"Successfully saved analysis to {filename}")
        except Exception as e:
            self.log(f"Error saving analysis to {filename}: {e}")

    def perform_analysis(self, method: str, count: int = 20) -> str:
        data = self.read_data()

        if method == 'lowest':
            result = self.lowest_number_of_search_results(data, count)
        elif method == 'highest':
            result = self.highest_number_of_search_results(data, count)
        elif method == 'recent':
            result = self.most_recent_keywords(data, count)
        elif method == 'trending':
            result = self.trending_keywords(data)
        elif method == 'popularity':
            result = self.keyword_popularity(data, count)
        else:
            return "Invalid analysis method."

        self.save_analysis_to_csv(result, f'analysis_{method}.csv')
        return f'CSV file updated with {method} analysis.'

    def lowest_number_of_search_results(self, data: pd.DataFrame, count: int) -> pd.DataFrame:
        # Convert 'Search Results' to numeric, ignoring errors for invalid parsing
        data['Search Results'] = pd.to_numeric(data['Search Results'], errors='coerce')
        
        # Drop rows where 'Search Results' is NaN (result of coercing non-numeric values to NaN)
        data = data.dropna(subset=['Search Results'])
        
        # Ensure 'Search Results' is an integer
        data['Search Results'] = data['Search Results'].astype(int)
        
        # Sort by 'Search Results' in ascending order and select the top 'count' keywords
        return data.sort_values(by='Search Results').head(count)

    def highest_number_of_search_results(self, data: pd.DataFrame, count: int) -> pd.DataFrame:
        # Similar approach for highest number of search results
        data['Search Results'] = pd.to_numeric(data['Search Results'], errors='coerce')
        data = data.dropna(subset=['Search Results'])
        data['Search Results'] = data['Search Results'].astype(int)
        return data.sort_values(by='Search Results', ascending=False).head(count)

    def most_recent_keywords(self, data: pd.DataFrame, count: int) -> pd.DataFrame:
        data['Timestamp'] = pd.to_datetime(data['Timestamp'], unit='s')
        return data.sort_values(by='Timestamp', ascending=False).head(count)

    def trending_keywords(self, data: pd.DataFrame) -> pd.DataFrame:
        # Placeholder for trending keywords logic
        pass

    def keyword_popularity(self, data: pd.DataFrame, count: int) -> pd.DataFrame:
        data['Search Results'] = pd.to_numeric(data['Search Results'], errors='coerce')
        data = data.dropna(subset=['Search Results'])
        grouped_data = data.groupby('Keyword').agg({'Search Results': 'mean'}).reset_index()
        sorted_data = grouped_data.sort_values(by='Search Results', ascending=False).head(count)
        return sorted_data

    def get_top_keywords(self) -> str:
        data = pd.read_csv('analysis_lowest.csv')
        return ','.join(data['Keyword'].tolist())
