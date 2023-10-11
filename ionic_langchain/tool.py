# Temp inlining of "SDK"
import requests

from langchain.tools import AIPluginTool, Tool

from ionic_langchain.prompt import TOOL_PROMPT


class Ionic:
    PROD_SERVER = "https://api.ionicapi.com"

    def __init__(self, base_url=None):
        self.base_url = base_url or self.PROD_SERVER

    def query(self, queries: str):
        url = f"{self.base_url}/query"
        
        query_list = [{"query": query} for query in queries.split(", ")]
        
        payload = {"queries": query_list}
        result = requests.post(url, json=payload)

        return result.json()


# TODO StructuredTool or BaseTool
    # https://github.com/langchain-ai/langchain/issues/4197
    # https://python.langchain.com/docs/modules/agents/tools/multi_input_tool


class IonicTool():
    def __init__(self, base_url=None):
        self.ionic = Ionic()

        if base_url:
            self.ionic.base_url = base_url

    def tool(self):
        return Tool(
            func=self.ionic.query,
            name="Ionic Shopping",
            description=TOOL_PROMPT,
            verbose=True
        )
    
    
      

class IonicPluginTool(): 
    def __init__(self, base_url="https://api.ionicapi.com"):
        self.base_url = base_url
  
    def tool(self):
        # tool = AIPluginTool.from_plugin_url("https://www.klarna.com/.well-known/ai-plugin.json")
        tool = AIPluginTool.from_plugin_url(f'{self.base_url}/.well-known/ai-plugin.json')
        print(tool)

        return tool


