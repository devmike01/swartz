# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import requests
import os


class BulkReferencer:
    api: str = "https://www.mybib.com/api/autocite/search?q={}&sourceId=webpage"

    def find_reference(self, ref_url: str):
        response = requests.get(self.api.format(ref_url.strip()))
        return response.json()

    def find_references(self, i: int, ref_urls: list, results: list):
        if i < len(ref_urls):
            url: str = ref_urls[i]
            results.append(self.find_reference(url))
            self.find_references(i + 1, ref_urls, results)
        return results

    def extract_data(self, ref_urls: list):
        result = self.find_references(0, ref_urls, [])
        return result
