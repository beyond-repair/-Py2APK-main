"""Legacy ONNX Android integration test — skipped without model + onnx extra."""
import pytest

pytestmark = pytest.mark.skip(
    reason="Claim-0: requires ONNX model asset and py2apk[onnx]; see tests/ for SDK-free suite"
)


def test_placeholder():
    assert True
