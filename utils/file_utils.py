# utils/file_utils.py
import csv
from typing import List, Tuple

class FileUtils:
    @staticmethod
    def save_to_file(filename: str, content: str) -> None:
        with open(filename, 'a') as file:
            file.write(content + '\n')

    @staticmethod
    def save_results_to_csv(results: List[Tuple], headers: List[str], filename: str) -> None:
        with open(filename, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Write header if the file is empty
            if file.tell() == 0:
                writer.writerow(headers)
            writer.writerows(results)
