import dataclasses
from typing import Any, Optional, Sequence

from ionic import Ionic as IonicSDK
from ionic.models.components import Query as SDKQuery, QueryAPIRequest
from ionic.models.operations import QueryResponse, QuerySecurity
from langchain_core.tools import Tool

from ionic_langchain.prompt import TOOL_PROMPT

class Ionic:
    _sdk: IonicSDK

    def __init__(self, sdk: Optional[IonicSDK] = None):
        if sdk:
            self._sdk = sdk
        else:
            self._sdk = IonicSDK()

    def query(
        self,
        query_input: str,
    ) -> Sequence[dict[str, Any]]:
        if not query_input:
            raise ValueError("query must not be empty")
        """
        :param query_input:  see QueryInput
        :return:
        """
        split_query = query_input.split(",")
        query = split_query + [None] * (4 - len(split_query))
        query = [item.strip() if item is not None else None for item in query]
        print("query", query)
        request = QueryAPIRequest(
            query=SDKQuery(
                query=str(query[0]),
                num_results=int(query[1]) if query[1] not in [None, ''] else None,
                min_price=int(query[2]) if query[2] not in [None, ''] else None,
                max_price=int(query[3]) if query[3] not in [None, ''] else None,
            )
        )
        response: QueryResponse = self._sdk.query(
            request=request,
            security=QuerySecurity(),
        )

        return [
            dataclasses.asdict(result) for result in response.query_api_response.results
        ]


class IonicTool:
    _ionic: Ionic

    def __init__(self, ionic: Optional[Ionic] = None):
        if ionic:
            self._ionic = ionic
        else:
            self._ionic = Ionic()

    def tool(self) -> Tool:
        """
        - https://github.com/langchain-ai/langchain/issues/4197
        - https://python.langchain.com/docs/modules/agents/tools/multi_input_tool
        """
        return Tool.from_function(
            func=self._ionic.query,
            name="Ionic Commerce Shopping Tool",
            description=TOOL_PROMPT,
            verbose=True,
        )
