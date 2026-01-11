import os
import pytest

pytestmark = pytest.mark.integration


@pytest.mark.skipif(
    not os.getenv("DEEPSEEK_API_KEY"),
    reason="Integration test requires DEEPSEEK_API_KEY"
)
def test_real_translation():
    """
    Integration test placeholder.
    Spou?t? se jen ru?n?:
        pytest tests/integration
    """
    assert True
