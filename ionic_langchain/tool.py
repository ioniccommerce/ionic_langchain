import dataclasses
from typing import Any, Optional, Annotated, Sequence, List

from ionic import Ionic as IonicSDK
from ionic.models.components import QueryAPIRequest, Query as SDKQuery
from ionic.models.operations import QuerySecurity, QueryResponse
from langchain_core.tools import Tool
from pydantic import BaseModel, StringConstraints

from ionic_langchain.prompt import TOOL_PROMPT

QueryString = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


class Query(BaseModel):
    """
    :param queries: one or more queries separated by commas
    :param num_results: how many results should be returned.
    :param min_price: minimum price of products in recommendation.  Some results may be slightly lower than specified.
    :param max_price: maximum price of products in recommendation.  Some results may be slightly higher than specified.
    """

    query: QueryString
    num_results: Optional[int] = None
    min_price: Optional[int] = None
    max_price: Optional[int] = None


class QueryInput(BaseModel):
    queries: List[Query]


class Ionic:
    _sdk: IonicSDK

    def __init__(self, sdk: Optional[IonicSDK] = None):
        """
        :param sdk: Provide your own SDK if you need to customize something; otherwise, a default instance will be used.
        """
        if sdk is None:
            self._sdk = IonicSDK()
        else:
            self._sdk = sdk

    def query(
        self,
        query_input: QueryInput,
    ) -> Sequence[dict[str, Any]]:
        if len(query_input.queries) == 0:
            raise ValueError("query_input must not be empty")
        """
        :param query_input:  see QueryInput
        :return:
        """
        request = QueryAPIRequest(
            queries=[
                SDKQuery(
                    query=query.query,
                    num_results=query.num_results,
                    min_price=query.min_price,
                    max_price=query.max_price,
                )
                for query in query_input.queries
            ],
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

    def __init__(self):
        self._ionic = Ionic()

    def tool(self) -> Tool:
        """
        - https://github.com/langchain-ai/langchain/issues/4197
        - https://python.langchain.com/docs/modules/agents/tools/multi_input_tool
        """
        return Tool.from_function(
            func=self._ionic.query,
            name="Ionic Shopping",
            description=TOOL_PROMPT,
            verbose=True,
        )
