# crypto_security/blacklist_manager.py

import yaml
import logging
from typing import Set, Dict
from pathlib import Path

logger = logging.getLogger(__name__)

class BlacklistManager:
    """Manages blacklists for suspicious tokens and developers"""
    
    def __init__(self, blacklist_file: str = 'blacklists.yaml'):
        """
        Initialize the BlacklistManager
        
        Args:
            blacklist_file (str): Path to the YAML file storing blacklists
        """
        self.blacklist_file = blacklist_file
        self.blacklists = self._load_blacklists()
    
    def _load_blacklists(self) -> Dict[str, Set[str]]:
        """
        Load existing blacklists from file
        
        Returns:
            Dict[str, Set[str]]: Dictionary containing different types of blacklists
        """
        try:
            with open(self.blacklist_file, 'r') as f:
                data = yaml.safe_load(f) or {}
                return {
                    'tokens': set(data.get('tokens', [])),
                    'developers': set(data.get('developers', [])),
                    'contracts': set(data.get('contracts', [])),
                    'domains': set(data.get('domains', []))
                }
        except FileNotFoundError:
            logger.info(f"Blacklist file {self.blacklist_file} not found. Creating new blacklists.")
            return {
                'tokens': set(),
                'developers': set(),
                'contracts': set(),
                'domains': set()
            }
        except Exception as e:
            logger.error(f"Error loading blacklists: {e}")
            return {
                'tokens': set(),
                'developers': set(),
                'contracts': set(),
                'domains': set()
            }
    
    def _save_blacklists(self) -> None:
        """Save current blacklists to file"""
        try:
            # Create directory if it doesn't exist
            Path(self.blacklist_file).parent.mkdir(parents=True, exist_ok=True)
            
            # Convert sets to lists for YAML serialization
            data = {k: list(v) for k, v in self.blacklists.items()}
            
            with open(self.blacklist_file, 'w') as f:
                yaml.dump(data, f)
            logger.debug("Blacklists saved successfully")
        except Exception as e:
            logger.error(f"Error saving blacklists: {e}")
    
    def add_to_blacklist(self, blacklist_type: str, address: str) -> None:
        """
        Add address to specified blacklist
        
        Args:
            blacklist_type (str): Type of blacklist ('tokens', 'developers', etc.)
            address (str): Address to blacklist
        """
        if not address:
            logger.warning("Attempted to add empty address to blacklist")
            return
            
        if blacklist_type not in self.blacklists:
            logger.warning(f"Invalid blacklist type: {blacklist_type}")
            return
            
        self.blacklists[blacklist_type].add(address.lower())  # Store addresses in lowercase
        self._save_blacklists()
        logger.info(f"Added {address} to {blacklist_type} blacklist")
    
    def remove_from_blacklist(self, blacklist_type: str, address: str) -> None:
        """
        Remove address from specified blacklist
        
        Args:
            blacklist_type (str): Type of blacklist ('tokens', 'developers', etc.)
            address (str): Address to remove
        """
        if blacklist_type not in self.blacklists:
            logger.warning(f"Invalid blacklist type: {blacklist_type}")
            return
            
        self.blacklists[blacklist_type].discard(address.lower())
        self._save_blacklists()
        logger.info(f"Removed {address} from {blacklist_type} blacklist")
    
    def is_blacklisted(self, blacklist_type: str, address: str) -> bool:
        """
        Check if address is in specified blacklist
        
        Args:
            blacklist_type (str): Type of blacklist ('tokens', 'developers', etc.)
            address (str): Address to check
            
        Returns:
            bool: True if address is blacklisted, False otherwise
        """
        if blacklist_type not in self.blacklists:
            logger.warning(f"Invalid blacklist type: {blacklist_type}")
            return False
            
        return address.lower() in self.blacklists[blacklist_type]
    
    def get_blacklist(self, blacklist_type: str) -> Set[str]:
        """
        Get all addresses in specified blacklist
        
        Args:
            blacklist_type (str): Type of blacklist to retrieve
            
        Returns:
            Set[str]: Set of blacklisted addresses
        """
        return self.blacklists.get(blacklist_type, set()).copy()
    
    def clear_blacklist(self, blacklist_type: str) -> None:
        """
        Clear all entries from specified blacklist
        
        Args:
            blacklist_type (str): Type of blacklist to clear
        """
        if blacklist_type in self.blacklists:
            self.blacklists[blacklist_type].clear()
            self._save_blacklists()
            logger.info(f"Cleared {blacklist_type} blacklist")