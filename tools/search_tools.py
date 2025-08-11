from crewai.tools import tool
import json
import os
import requests

class SearchTools:

    @tool("Search internet")
    def search_internet(self, query: str) -> str:
        """Useful to search the internet about a given topic and return relevant results."""
        return self._search(query)

    @tool("Search Instagram")
    def search_instagram(self, query: str) -> str:
        """Useful to search for Instagram posts about a given topic and return relevant results."""
        instagram_query = f"site:instagram.com {query}"
        return self._search(instagram_query)

    @staticmethod
    def _search(query: str, n_results: int = 5) -> str:
        url = "https://google.serper.dev/search"
        payload = json.dumps({"q": query})
        headers = {
            'X-API-KEY': os.environ['SERPER_API_KEY'],
            'content-type': 'application/json'
        }

        response = requests.post(url, headers=headers, data=payload)
        results = response.json().get('organic', [])
        output = []

        for result in results[:n_results]:
            try:
                output.append('\n'.join([
                    f"Title: {result['title']}",
                    f"Link: {result['link']}",
                    f"Snippet: {result['snippet']}",
                    "-----------------"
                ]))
            except KeyError:
                continue

        return '\n'.join(output)
