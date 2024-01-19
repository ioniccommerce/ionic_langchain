import dataclasses
from typing import Annotated, Any, Optional, Sequence

from ionic import Ionic as IonicSDK
from ionic.models.components import Query as SDKQuery, QueryAPIRequest
from ionic.models.operations import QueryResponse, QuerySecurity
from langchain_core.tools import Tool
from pydantic import BaseModel, StringConstraints

from ionic_langchain.prompt import TOOL_PROMPT

QueryString = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


class Query(BaseModel):
    """
    :param query: query string for product or product category with attributes.
    :param num_results: how many results should be returned.
    :param min_price: minimum price of products in recommendation.  Some results may be slightly lower than specified.
    :param max_price: maximum price of products in recommendation.  Some results may be slightly higher than specified.
    """

    query: QueryString
    num_results: Optional[int] = None
    min_price: Optional[int] = None
    max_price: Optional[int] = None


class Ionic:
    _sdk: IonicSDK

    def __init__(self, sdk: Optional[IonicSDK] = None):
        if sdk:
            self._sdk = sdk
        else:
            self._sdk = IonicSDK()

    def query(
        self,
        query: Query,
    ) -> Sequence[dict[str, Any]]:
        if not query:
            raise ValueError("query must not be empty")
        """
        :param query:  Query object
        :return:
        """
        request = QueryAPIRequest(
            query=SDKQuery(
                query=str(query.query),
                num_results=query.num_results,
                min_price=query.min_price,
                max_price=query.max_price,
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
