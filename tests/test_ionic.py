import sys

import pytest
from ionic import Ionic as IonicSdk
from ionic.models.errors import HTTPValidationError

from ionic_langchain.tool import Ionic, Query, QueryInput


def test_ionic_num_results():
    """
    requires server to be running (i.e. not compatible with CI)
    """
    ionic = Ionic(
        sdk=IonicSdk(server_url="http://localhost:8080"),
    )
    results = ionic.query(
        query_input=QueryInput(
            queries=[
                Query(
                    query="Reindeer Jerky",
                    num_results=2,
                )
            ]
        )
    )

    assert len(results) == 1
    reindeer_jerky_result = results[0]
    assert (
        reindeer_jerky_result["query"]["query"] == "Reindeer Jerky"
    ), "query should be included in response object"
    assert reindeer_jerky_result["query"]["num_results"] == 2
    assert reindeer_jerky_result["query"]["max_price"] is None
    assert reindeer_jerky_result["query"]["min_price"] is None
    assert "products" in reindeer_jerky_result
    assert (
        len(reindeer_jerky_result["products"]) == 2
    ), "num_results should be respected"


def test_ionic_bad_input():
    """
    requires server to be running
    """
    ionic = Ionic(
        sdk=IonicSdk(
            server_url="http://localhost:8080",
        ),
    )

    with pytest.raises(HTTPValidationError) as exc_info:
        ionic.query(
            query_input=QueryInput(
                queries=[
                    Query(
                        query="Reindeer Jerky",
                        max_price=-1,
                        min_price=-1,
                        num_results=sys.maxsize,
                    )
                ]
            )
        )

    problems = [det.loc[-1] for det in exc_info.value.detail]
    assert len(problems) == 3, "all problems are included in error"
    assert sorted(problems) == ["max_price", "min_price", "num_results"]
