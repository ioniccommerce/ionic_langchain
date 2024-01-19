from ionic import Ionic as IonicSdk

from ionic_langchain.tool import Ionic, Query


def test_ionic_num_results():
    """
    requires server to be running (i.e. not compatible with CI)
    """
    ionic = Ionic(
        sdk=IonicSdk(server_url="http://localhost:8080"),
    )
    results = ionic.query(
        query=Query(
            query="Reindeer Jerky",
            num_results=2,
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
