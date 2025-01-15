# tests/test_unit_2.py
import pytest
from crypto_security import CryptoSecurityFilter

@pytest.fixture
def security_filter():
    return CryptoSecurityFilter(
        rugcheck_api_key="test_key",
        rocker_universe_api_key="test_key"
    )

@pytest.mark.asyncio
async def test_analyze_token(security_filter):
    token_data = {
        'address': '0x123test',
        'symbol': 'TEST',
        'volume': 5000,
        'volume_1h': 500,
        'volume_24h': 10000
    }
    
    result = await security_filter.analyze_token(token_data)
    assert result is not None
    assert 'volume_score' in result
    assert 'risk_level' in result

# tests/test_volume_analyzer.py
import pytest
from crypto_security import VolumeAnalyzer

def test_analyze_volume_legitimate():
    analyzer = VolumeAnalyzer()
    volume_data = {
        'total_volume': 5000,
        '1h_volume': 100,
        '24h_volume': 2000,
        'volume_liquidity_ratio': 0.5,
        'volume_spike_ratio': 1.5
    }
    score = analyzer.analyze_volume(volume_data)
    assert score > 0.8

def test_analyze_volume_suspicious():
    analyzer = VolumeAnalyzer()
    volume_data = {
        'total_volume': 100,
        '1h_volume': 0,
        '24h_volume': 0,
        'volume_liquidity_ratio': 0.01,
        'volume_spike_ratio': 5.0
    }
    score = analyzer.analyze_volume(volume_data)
    assert score < 0.5

# tests/test_api_integrations.py
import pytest
from crypto_security import APIManager

@pytest.mark.asyncio
async def test_api_manager():
    api_manager = APIManager()
    result = await api_manager.analyze_token("0x123test")
    assert isinstance(result, dict)
    assert len(result) > 0
