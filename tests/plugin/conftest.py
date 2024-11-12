from pathlib import Path

import plugin_python_template
import pytest
from stencila_plugin.testing import HttpHarness, StdioHarness

@pytest.mark.skip(reason="no way of currently testing this")
@pytest.fixture()
def plugin_path():
    """Provide the path to the plugin."""
    path = Path(plugin_python_template.__file__).parent / "plugin.py"
    assert path.exists()
    return path

@pytest.mark.skip(reason="no way of currently testing this")
@pytest.fixture()
async def stdio_harness(plugin_path: Path):
    async with StdioHarness(plugin_path) as harness:
        yield harness

@pytest.mark.skip(reason="no way of currently testing this")
@pytest.fixture()
async def http_harness(plugin_path: Path):
    async with HttpHarness(plugin_path) as harness:
        yield harness

@pytest.mark.skip(reason="no way of currently testing this")
@pytest.fixture(params=["stdio_harness", "http_harness"])
def harness(request):  # noqa: ANN001
    """Roll up both harnesses together."""
    return request.getfixturevalue(request.param)
