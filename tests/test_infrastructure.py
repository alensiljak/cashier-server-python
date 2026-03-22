'''
Test infrastructure endpoints
'''

import os
import pytest
import main
from fastapi.testclient import TestClient


client = TestClient(main.app)


# Get the directory of the test files
TEST_DIR = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture(autouse=True)
def set_bean_file():
    """Set BEANCOUNT_FILE to use the test book.bean file."""
    # Set the environment variable to the test book.bean
    test_bean_file = os.path.join(TEST_DIR, "book.bean")
    os.environ["BEANCOUNT_FILE"] = test_bean_file
    # Reload the main module's BEAN_FILE
    main.BEAN_FILE = test_bean_file
    yield
    # Cleanup (optional)


class TestInfrastructureConfig:
    """Tests for /infrastructure/config endpoint"""

    def test_infrastructure_config_returns_config_file(self):
        """Test that config endpoint returns the config.bean file content."""
        response = client.get("/infrastructure/config")
        assert response.status_code == 200
        result = response.json()
        assert "content" in result
        
        # Read expected content from tests/config.bean
        config_path = os.path.join(TEST_DIR, "config.bean")
        with open(config_path, "r", encoding="utf-8") as f:
            expected_content = f.read()
        
        assert result["content"] == expected_content

    def test_infrastructure_config_returns_required_files(self):
        """Test that config endpoint returns the required config.bean file."""
        response = client.get("/infrastructure/config")
        assert response.status_code == 200
        result = response.json()
        assert "content" in result
        assert isinstance(result["content"], str)
        assert len(result["content"]) > 0


class TestInfrastructureAccounts:
    """Tests for /infrastructure/accounts endpoint"""

    def test_infrastructure_accounts_returns_accounts_file(self):
        """Test that accounts endpoint returns the accounts.bean file content."""
        response = client.get("/infrastructure/accounts")
        assert response.status_code == 200
        result = response.json()
        assert "content" in result
        
        # Read expected content from tests/accounts.bean
        accounts_path = os.path.join(TEST_DIR, "accounts.bean")
        with open(accounts_path, "r", encoding="utf-8") as f:
            expected_content = f.read()
        
        assert result["content"] == expected_content

    def test_infrastructure_accounts_returns_required_files(self):
        """Test that accounts endpoint returns the required accounts.bean file."""
        response = client.get("/infrastructure/accounts")
        assert response.status_code == 200
        result = response.json()
        assert "content" in result
        assert isinstance(result["content"], str)


class TestInfrastructureCommodities:
    """Tests for /infrastructure/commodities endpoint"""

    def test_infrastructure_commodities_returns_commodities_file(self):
        """Test that commodities endpoint returns the commodities.bean file content."""
        response = client.get("/infrastructure/commodities")
        assert response.status_code == 200
        result = response.json()
        assert "content" in result
        
        # Read expected content from tests/commodities.bean
        commodities_path = os.path.join(TEST_DIR, "commodities.bean")
        with open(commodities_path, "r", encoding="utf-8") as f:
            expected_content = f.read()
        
        assert result["content"] == expected_content

    def test_infrastructure_commodities_returns_required_files(self):
        """Test that commodities endpoint returns the required commodities.bean file."""
        response = client.get("/infrastructure/commodities")
        assert response.status_code == 200
        result = response.json()
        assert "content" in result
        assert isinstance(result["content"], str)
