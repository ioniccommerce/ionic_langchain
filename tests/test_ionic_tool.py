import pytest

from ionic_langchain.tool import IonicTool


def test_ionic_tool_is_valid():
    """
    sanity check to ensure tool is valid
    """
    try:
        IonicTool().tool()
    except Exception:
        pytest.fail("unexpected exception %s initializing IonicTool#tool")