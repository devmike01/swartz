import requests


class BulkReferencer:
    api: str = "https://www.mybib.com/api/autocite/search?q={}&sourceId=webpage"

    def find_reference(self, ref_url: str):
        response = requests.get(self.api.format(ref_url.strip()))
        if response.status_code == 200:
            response = response.json()
        else:
            response = {
                "error": "{}. \nReason: {}".format(ref_url, str(response.reason))
            }
        return response

    def find_references(self, i: int, ref_urls: list, results: list):
        if i < len(ref_urls):
            url: str = ref_urls[i]
            result = self.find_reference(url)
            if result.get('error') is None:
                results.append(result)
                self.find_references(i + 1, ref_urls, results)
            else:
                print("SWARTZ_NEW_ERROR: err_at_{}".format(result.get('error')))
                self.find_references(i+1, ref_urls, results)
        return results

    def extract_data(self, ref_urls: list):
        result = self.find_references(0, ref_urls, [])
        return result
