from __future__ import annotations

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

        query, num_results, min_price, max_price = self.gen_query_request(query_input)
        request = QueryAPIRequest(
            query=SDKQuery(
                query=query,
                num_results=num_results,
                min_price=min_price,
                max_price=max_price,
            )
        )
        response: QueryResponse = self._sdk.query(
            request=request,
            security=QuerySecurity(),
        )

        return [
            dataclasses.asdict(result) for result in response.query_api_response.results
        ]

    def _parse_number(self, value: str) -> int | None:
        return int(value) if value and int(value) >= 0 else None

    def gen_query_request(
        self, query_input: str
    ) -> tuple[str, int | None, int | None, int | None]:
        if not query_input:
            raise ValueError("query must not be empty")

        split_query = query_input.split(",")
        len4_query = split_query + [None] * (4 - len(split_query))  # pad with None

        (
            query,
            num_results,
            min_price,
            max_price,
            *rest,
        ) = [  # *rest ignores extra values
            item.strip() if item is not None else None for item in len4_query
        ]
        if not query:
            raise ValueError("query must not be empty")

        return (
            str(query),
            self._parse_number(num_results),
            self._parse_number(min_price),
            self._parse_number(max_price),
        )


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
