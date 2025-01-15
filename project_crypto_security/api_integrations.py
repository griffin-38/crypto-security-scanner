from dataclasses import dataclass
from typing import Optional, Dict, Any
import aiohttp
import logging
from abc import ABC, abstractmethod
import os
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

@dataclass
class APIConfig:
    """API configuration container"""
    api_key: str
    endpoint: str
    timeout: int = 30
    max_retries: int = 3

class BaseAPIClient(ABC):
    """Abstract base class for API clients"""
    def __init__(self, config: APIConfig):
        self.config = config
        self.headers = {
            'Authorization': f'Bearer {config.api_key}',
            'Content-Type': 'application/json'
        }

    @abstractmethod
    async def validate_token(self, token_address: str) -> Dict[str, Any]:
        """Validate token through specific API"""
        pass

    async def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request with retry logic"""
        for attempt in range(self.config.max_retries):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.request(
                        method=method,
                        url=f"{self.config.endpoint}/{endpoint.lstrip('/')}",
                        headers=self.headers,
                        timeout=self.config.timeout,
                        **kwargs
                    ) as response:
                        response.raise_for_status()
                        return await response.json()
            except Exception as e:
                if attempt == self.config.max_retries - 1:
                    logger.error(f"API request failed after {self.config.max_retries} attempts: {e}")
                    raise
                logger.warning(f"API request attempt {attempt + 1} failed: {e}")
                
class APIManager:
    """Manages all API integrations"""
    def __init__(self):
        # Initialize API clients
        self.apis = self._initialize_apis()

    def _initialize_apis(self) -> Dict[str, BaseAPIClient]:
        """Initialize all API clients"""
        return {
            # Implement actual API client initialization
        }

    async def analyze_token(self, token_address: str) -> Dict[str, Any]:
        """Analyze token using all available APIs"""
        results = {}
        for api_name, api_client in self.apis.items():
            try:
                results[api_name] = await api_client.validate_token(token_address)
            except Exception as e:
                logger.error(f"Error analyzing token with {api_name}: {e}")
                results[api_name] = {'error': str(e)}
        return results
