
from langchain.tools import tool
import json
import os
import requests

from langchain_community.tools.wikidata.tool import WikidataAPIWrapper, WikidataQueryRun

from langchain.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools import DuckDuckGoSearchRun

wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

wikidata = WikidataQueryRun(api_wrapper=WikidataAPIWrapper())

search_tool = DuckDuckGoSearchRun()


class SearchTools():
    @tool("Search the internet")
    def search_internet(query):
        """Useful to search the internet 
        about a a given topic and return relevant results"""
        top_result_to_return = 4
        url = "https://google.serper.dev/search"
        payload = json.dumps({"q": query})
        headers = {
            'X-API-KEY': os.environ['SERPER_API_KEY'],
            'content-type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        results = response.json()['organic']
        string = []
        for result in results[:top_result_to_return]:
            try:
                string.append('\n'.join([
                    f"Title: {result['title']}", f"Link: {result['link']}",
                    f"Snippet: {result['snippet']}", "\n-----------------"
                ]))
            except KeyError:
                next

        return '\n'.join(string)
    

if __name__ == "__main__":
    course_content = CourseContent.course_info
    deatils = course_content.run("how")
    print(course_content.name, course_content.description, course_content.args)