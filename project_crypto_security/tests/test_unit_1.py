# tests/test_unit_1.py
import pytest
from unittest.mock import patch, Mock
from dataclasses import asdict
from datetime import datetime
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from crypto_security import (
    VolumeAnalyzer,
    RugCheckAPI,
    CryptoSecurityFilter,
    ContractRisk,
    ContractAnalysis
)

class TestVolumeAnalyzer:
    def test_analyze_volume_perfect_score(self):
        volume_data = {
            'total_volume': 2000,
            '1h_volume': 100,
            '24h_volume': 500,
            'volume_liquidity_ratio': 0.2,
            'volume_spike_ratio': 1.5
        }
        score = VolumeAnalyzer.analyze_volume(volume_data)
        assert score == 1.0

    def test_analyze_volume_zero_score(self):
        volume_data = {
            'total_volume': 0,
            '1h_volume': 0,
            '24h_volume': 0,
            'volume_liquidity_ratio': 0,
            'volume_spike_ratio': 3.0
        }
        score = VolumeAnalyzer.analyze_volume(volume_data)
        assert score == 0.0

    def test_analyze_volume_missing_data(self):
        volume_data = {}
        score = VolumeAnalyzer.analyze_volume(volume_data)
        assert score == 0.0

    def test_analyze_volume_partial_score(self):
        volume_data = {
            'total_volume': 2000,  # Pass
            '1h_volume': 0,        # Fail
            '24h_volume': 500,     # Pass
            'volume_liquidity_ratio': 0.2,  # Pass
            'volume_spike_ratio': 3.0       # Fail
        }
        score = VolumeAnalyzer.analyze_volume(volume_data)
        assert score == 0.6  # 3 out of 5 checks pass

class TestRugCheckAPI:
    def test_check_contract_success(self):
        api = RugCheckAPI()
        analysis = api.check_contract("0xValidAddress")
        
        assert isinstance(analysis, ContractAnalysis)
        assert analysis.token_address == "0xValidAddress"
        assert analysis.risk_level == ContractRisk.LOW_RISK
        assert analysis.is_verified is True
        assert analysis.is_honeypot is False

    @patch('logging.Logger.error')
    def test_check_contract_exception_handling(self, mock_logger):
        api = RugCheckAPI()
        with patch.object(api, 'base_url', side_effect=Exception("API error")):
            analysis = api.check_contract("0xInvalidAddress")
            
            assert analysis.token_address == "0xInvalidAddress"
            assert analysis.risk_level == ContractRisk.HIGH_RISK
            mock_logger.assert_called_once()

class TestCryptoSecurityFilter:
    @pytest.fixture
    def security_filter(self):
        return CryptoSecurityFilter(
            rugcheck_api_key="test_key",
            rocker_universe_api_key="test_key"
        )

    def test_perform_comprehensive_analysis_low_volume_score(self, security_filter):
        token_data = {
            'address': '0x123token_address',
            'symbol': 'TEST',
            'volume': 100,
            'volume_1h': 0,
            'volume_24h': 0,
            'volume_liquidity_ratio': 0.05,
            'volume_spike': 3
        }
        result = security_filter.perform_comprehensive_analysis(token_data)
        assert result is None

    def test_perform_comprehensive_analysis_success(self, security_filter):
        token_data = {
            'address': '0x123token_address',
            'symbol': 'TEST',
            'volume': 5000,
            'volume_1h': 500,
            'volume_24h': 10000,
            'volume_liquidity_ratio': 0.2,
            'volume_spike': 1.5,
            'developer_address': '0x456dev_address'
        }
        result = security_filter.perform_comprehensive_analysis(token_data)
        
        assert result is not None
        assert result['symbol'] == 'TEST'
        assert result['volume_legitimacy_score'] == 1.0
        assert result['contract_risk_level'] == 'LOW_RISK'

    def test_filter_tokens(self, security_filter):
        tokens_data = [
            {
                'address': '0x123token_address',
                'symbol': 'GOOD',
                'volume': 5000,
                'volume_1h': 500,
                'volume_24h': 10000,
                'volume_liquidity_ratio': 0.2,
                'volume_spike': 1.5
            },
            {
                'address': '0x456token_address',
                'symbol': 'BAD',
                'volume': 100,
                'volume_1h': 0,
                'volume_24h': 0,
                'volume_liquidity_ratio': 0.05,
                'volume_spike': 3
            }
        ]
        
        verified_tokens = security_filter.filter_tokens(tokens_data)
        
        assert len(verified_tokens) == 1
        assert verified_tokens[0]['symbol'] == 'GOOD'

    @patch('logging.Logger.error')
    def test_perform_comprehensive_analysis_exception(self, mock_logger, security_filter):
        token_data = None  # Invalid data to trigger exception
        result = security_filter.perform_comprehensive_analysis(token_data)
        
        assert result is None
        mock_logger.assert_called_once()

def test_main():
    with patch('crypto_security.CryptoSecurityFilter') as MockFilter:
        instance = MockFilter.return_value
        instance.filter_tokens.return_value = [
            {
                'symbol': 'TEST',
                'contract_risk_level': 'LOW_RISK'
            }
        ]
        
        # Test main function doesn't raise exceptions
        try:
            main()
            assert True
        except Exception:
            assert False, "main() raised an exception"
        finally:
            pass

        