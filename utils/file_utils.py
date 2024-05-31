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

    @staticmethod
    def calculate_aspect_ratio(width: int, height: int) -> str:
        common_aspect_ratios = {
            "16:9": 16 / 9,
            "9:16": 9 / 16,
            "4:3": 4 / 3,
            "3:4": 3 / 4,
            "3:2": 3 / 2,
            "2:3": 2 / 3,
            "1:1": 1 / 1
        }

        def gcd(a: int, b: int) -> int:
            while b:
                a, b = b, a % b
            return a

        def closest_aspect_ratio(width: int, height: int) -> str:
            ratio = width / height
            closest = min(common_aspect_ratios, key=lambda x: abs(common_aspect_ratios[x] - ratio))
            return closest

        # Simplify the width and height by their greatest common divisor
        common_divisor = gcd(width, height)
        width //= common_divisor
        height //= common_divisor

        # Find the closest common aspect ratio
        return closest_aspect_ratio(width, height)
