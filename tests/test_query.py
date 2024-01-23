from ionic import Ionic as IonicSdk

from ionic_langchain.tool import Ionic


def test_ionic():
    """
    requires server to be running (i.e. not compatible with CI)
    """
    ionic = Ionic(
        sdk=IonicSdk(server_url="http://localhost:8080"),
    )
    results = ionic.query(
        query_input="Reindeer Jerky",
    )

    assert len(results) == 1
    reindeer_jerky_result = results[0]
    assert (
        reindeer_jerky_result["query"]["query"] == "Reindeer Jerky"
    ), "query should be included in response object"
    assert reindeer_jerky_result["query"]["num_results"] == 5
    assert reindeer_jerky_result["query"]["min_price"] is None
    assert reindeer_jerky_result["query"]["max_price"] is None
    assert "products" in reindeer_jerky_result
    assert (
        len(reindeer_jerky_result["products"]) == 5
    ), "num_results should be respected"


def test_ionic_num_results():
    """
    requires server to be running (i.e. not compatible with CI)
    """
    ionic = Ionic(
        sdk=IonicSdk(server_url="http://localhost:8080"),
    )
    results = ionic.query(
        query_input="Reindeer Jerky, 2",
    )

    assert len(results) == 1
    reindeer_jerky_result = results[0]
    assert (
        reindeer_jerky_result["query"]["query"] == "Reindeer Jerky"
    ), "query should be included in response object"
    assert reindeer_jerky_result["query"]["num_results"] == 2
    assert reindeer_jerky_result["query"]["min_price"] is None
    assert reindeer_jerky_result["query"]["max_price"] is None
    assert "products" in reindeer_jerky_result
    assert (
        len(reindeer_jerky_result["products"]) == 2
    ), "num_results should be respected"


def test_ionic_price_range():
    """
    requires server to be running (i.e. not compatible with CI)
    """
    ionic = Ionic(
        sdk=IonicSdk(server_url="http://localhost:8080"),
    )
    results = ionic.query(query_input="Reindeer Jerky, , 1000, 10000")

    assert len(results) == 1
    reindeer_jerky_result = results[0]
    assert (
        reindeer_jerky_result["query"]["query"] == "Reindeer Jerky"
    ), "query should be included in response object"
    assert reindeer_jerky_result["query"]["num_results"] == 5
    assert reindeer_jerky_result["query"]["min_price"] == 1000
    assert reindeer_jerky_result["query"]["max_price"] == 10000


def test_ionic_max_price():
    """
    requires server to be running (i.e. not compatible with CI)
    """
    ionic = Ionic(
        sdk=IonicSdk(server_url="http://localhost:8080"),
    )
    results = ionic.query(query_input="Reindeer Jerky, , , 10000")

    assert len(results) == 1
    reindeer_jerky_result = results[0]
    assert (
        reindeer_jerky_result["query"]["query"] == "Reindeer Jerky"
    ), "query should be included in response object"
    assert reindeer_jerky_result["query"]["num_results"] == 5
    assert reindeer_jerky_result["query"]["min_price"] is None
    assert reindeer_jerky_result["query"]["max_price"] == 10000


def test_ionic_min_price():
    """
    requires server to be running (i.e. not compatible with CI)
    """
    ionic = Ionic(
        sdk=IonicSdk(server_url="http://localhost:8080"),
    )
    results = ionic.query(query_input="Reindeer Jerky, , 1000")

    assert len(results) == 1
    reindeer_jerky_result = results[0]
    assert (
        reindeer_jerky_result["query"]["query"] == "Reindeer Jerky"
    ), "query should be included in response object"
    assert reindeer_jerky_result["query"]["num_results"] == 5
    assert reindeer_jerky_result["query"]["min_price"] == 1000
    assert reindeer_jerky_result["query"]["max_price"] is None
