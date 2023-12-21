import dataclasses
from typing import Any, Optional

from ionic import Ionic as IonicSDK
from ionic.models.components import QueryAPIRequest, Query
from ionic.models.operations import QuerySecurity, QueryResponse
from langchain.tools import Tool

from ionic_langchain.prompt import TOOL_PROMPT


class Ionic:
    _sdk: IonicSDK

    def __init__(self, sdk: Optional[IonicSDK] = None):
        if sdk:
            self._sdk = sdk
        else:
            self._sdk = IonicSDK()

    def query(self, queries: str) -> list[dict[str, Any]]:
        """
        FIXME: handle non-200 responses
        TODO: better typing in response
        """
        request = QueryAPIRequest(
            queries=[Query(query=query) for query in queries.split(", ")],
        )
        response: QueryResponse = self._sdk.query(
            request=request,
            security=QuerySecurity(),
        )

        return [dataclasses.asdict(r) for r in response.query_api_response.results]


# TODO StructuredTool or BaseTool
# https://github.com/langchain-ai/langchain/issues/4197
# https://python.langchain.com/docs/modules/agents/tools/multi_input_tool


class IonicTool:
    _ionic: Ionic

    def __init__(self, ionic: Optional[Ionic] = None):
        if ionic:
            self._ionic = ionic
        else:
            self._ionic = Ionic()

    def tool(self) -> Tool:
        return Tool(
            func=self._ionic.query,
            name="Ionic Shopping",
            description=TOOL_PROMPT,
            verbose=True,
        )
