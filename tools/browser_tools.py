import json
import os
import requests

from crewai import Agent, Task, Crew
from crewai.tools import tool  
from unstructured.partition.html import partition_html
from langchain_ollama import OllamaLLM

class BrowserTools:
    @tool("Scrape website content")
    def scrape_and_summarize_website(self, website: str) -> str:
        """Scrape and summarize a website content."""
        url = f"https://chrome.browserless.io/content?token={os.environ['BROWSERLESS_API_KEY']}"
        payload = json.dumps({"url": website})
        headers = {
            'cache-control': 'no-cache',
            'content-type': 'application/json'
        }

        response = requests.post(url, headers=headers, data=payload)

        elements = partition_html(text=response.text)
        full_content = "\n\n".join([str(el) for el in elements])
        chunks = [full_content[i:i + 8000] for i in range(0, len(full_content), 8000)]

        summaries = []

        for chunk in chunks:
            agent = Agent(
                role='Principal Researcher',
                goal='Do amazing researches and summaries based on the content you are working with',
                backstory='You are a Principal Researcher at a big company, tasked with detailed research.',
                llm=OllamaLLM(model="openhermes", base_url="http://localhost:11434"),
                allow_delegation=False
            )

            task = Task(
                agent=agent,
                description=f'Analyze and summarize the following content:\n\n{chunk}',
                expected_output="A detailed analysis report summarizing product features, appeal, and suggestions."
            )

            crew = Crew(
                agents=[agent],
                tasks=[task],
                verbose=True
            )

            result = crew.kickoff()
            summaries.append(result)

        return '\nScraped Content:\n' + '\n\n'.join(summaries)
