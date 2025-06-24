"""Unit tests for the instill.config module."""

# pylint: disable=consider-using-with

import importlib
import os
import shutil
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest
import yaml

import instill.config
from instill.config import Configuration, _Config, _InstillHost
from instill.helpers.const import HOST_URL_PROD


class TestInstillHost:
    """Test cases for the _InstillHost model."""

    def test_instill_host_creation(self):
        """Test creating an _InstillHost instance."""
        host = _InstillHost(url="https://test.com", secure=True, token="test-token")

        assert host.url == "https://test.com"
        assert host.secure is True
        assert host.token == "test-token"

    def test_instill_host_default_values(self):
        """Test _InstillHost with default values."""
        host = _InstillHost(url="https://test.com", secure=False, token="")

        assert host.url == "https://test.com"
        assert host.secure is False
        assert host.token == ""

    def test_instill_host_validation(self):
        """Test _InstillHost validation."""
        # Should not raise any exceptions for valid data
        _InstillHost(url="https://test.com", secure=True, token="test-token")
        _InstillHost(url="http://localhost:8080", secure=False, token="")


class TestConfig:
    """Test cases for the _Config model."""

    def test_config_creation(self):
        """Test creating an _Config instance."""
        config = _Config()
        assert not config.hosts

    def test_config_with_hosts(self):
        """Test _Config with hosts."""
        hosts = {
            "default": _InstillHost(
                url="https://test.com", secure=True, token="test-token"
            ),
            "custom": _InstillHost(
                url="https://custom.com", secure=False, token="custom-token"
            ),
        }
        config = _Config(hosts=hosts)

        assert len(config.hosts) == 2
        assert "default" in config.hosts
        assert "custom" in config.hosts
        assert config.hosts["default"].url == "https://test.com"
        assert config.hosts["custom"].url == "https://custom.com"


class TestConfiguration:
    """Test cases for the Configuration class."""

    def setup_method(self):
        """Set up test fixtures."""
        # Create a temporary directory for config files
        self.temp_dir = tempfile.TemporaryDirectory()
        self.config_dir = Path(self.temp_dir.name) / "instill" / "sdk" / "python"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.config_file = self.config_dir / "config.yml"

    def teardown_method(self):
        """Clean up test fixtures."""
        self.temp_dir.cleanup()

    def test_configuration_initialization(self):
        """Test Configuration initialization."""
        with patch("instill.config.CONFIG_DIR", self.config_dir):
            config = Configuration()

            # Test that config has the expected structure and default host
            assert hasattr(config, "_config")
            assert "default" in config.hosts
            assert config.hosts["default"].url == HOST_URL_PROD
            assert config.hosts["default"].secure is True
            assert config.hosts["default"].token == ""

    def test_configuration_load_nonexistent_file(self):
        """Test loading configuration when file doesn't exist."""
        with patch("instill.config.CONFIG_DIR", self.config_dir):
            config = Configuration()

            # When no config file exists, a default host should still be created
            assert "default" in config.hosts
            assert config.hosts["default"].url == HOST_URL_PROD
            assert config.hosts["default"].secure is True
            assert config.hosts["default"].token == ""

    def test_configuration_load_valid_file(self):
        """Test loading configuration from a valid YAML file."""
        with patch("instill.config.CONFIG_DIR", self.config_dir):
            # Create a valid config file
            config_data = {
                "hosts": {
                    "default": {
                        "url": "https://custom.com",
                        "secure": False,
                        "token": "custom-token",
                    },
                    "test": {
                        "url": "https://test.com",
                        "secure": True,
                        "token": "test-token",
                    },
                }
            }

            with open(self.config_file, "w", encoding="utf-8") as f:
                yaml.dump(config_data, f)

            config = Configuration()

            assert len(config.hosts) == 2
            assert config.hosts["default"].url == "https://custom.com"
            assert config.hosts["default"].secure is False
            assert config.hosts["default"].token == "custom-token"
            assert config.hosts["test"].url == "https://test.com"
            assert config.hosts["test"].secure is True
            assert config.hosts["test"].token == "test-token"

    def test_configuration_load_file_without_default(self):
        """Test loading configuration from file that doesn't have a default host."""
        with patch("instill.config.CONFIG_DIR", self.config_dir):
            # Create a config file without a default host
            config_data = {
                "hosts": {
                    "test": {
                        "url": "https://test.com",
                        "secure": True,
                        "token": "test-token",
                    }
                }
            }

            with open(self.config_file, "w", encoding="utf-8") as f:
                yaml.dump(config_data, f)

            config = Configuration()

            # Should have both the loaded host and a default host
            assert len(config.hosts) == 2
            assert "default" in config.hosts
            assert config.hosts["default"].url == HOST_URL_PROD
            assert config.hosts["default"].secure is True
            assert config.hosts["default"].token == ""
            assert config.hosts["test"].url == "https://test.com"
            assert config.hosts["test"].secure is True
            assert config.hosts["test"].token == "test-token"

    def test_configuration_load_invalid_file(self):
        """Test loading configuration from an invalid YAML file."""
        with patch("instill.config.CONFIG_DIR", self.config_dir):
            # Create an invalid config file
            with open(self.config_file, "w", encoding="utf-8") as f:
                f.write("invalid: yaml: content: [")

            with pytest.raises(BaseException, match="Invalid configuration file"):
                Configuration()

    def test_configuration_load_invalid_schema(self):
        """Test loading configuration with invalid schema."""
        with patch("instill.config.CONFIG_DIR", self.config_dir):
            # Create a config file with invalid schema
            config_data = {
                "hosts": {
                    "default": {
                        "url": "https://test.com",
                        # Missing required fields
                    }
                }
            }

            with open(self.config_file, "w", encoding="utf-8") as f:
                yaml.dump(config_data, f)

            with pytest.raises(BaseException, match="Invalid configuration file"):
                Configuration()

    def test_configuration_save(self):
        """Test saving configuration to file."""
        with patch("instill.config.CONFIG_DIR", self.config_dir):
            config = Configuration()

            # Add a custom host
            config.set_default("https://saved.com", "saved-token", False)

            # Save configuration
            config.save()

            # Verify file was created
            assert self.config_file.exists()

            # Load the saved configuration
            with open(self.config_file, "r", encoding="utf-8") as f:
                saved_data = yaml.load(f, Loader=yaml.FullLoader)

            assert "hosts" in saved_data
            assert "default" in saved_data["hosts"]
            assert saved_data["hosts"]["default"]["url"] == "https://saved.com"
            assert saved_data["hosts"]["default"]["secure"] is False
            assert saved_data["hosts"]["default"]["token"] == "saved-token"

    def test_configuration_save_creates_directory(self):
        """Test that save creates the config directory if it doesn't exist."""
        # Remove the config directory

        if self.config_dir.exists():
            shutil.rmtree(self.config_dir)

        with patch("instill.config.CONFIG_DIR", self.config_dir):
            config = Configuration()
            config.save()

            # Verify directory and file were created
            assert self.config_dir.exists()
            assert self.config_file.exists()

    def test_configuration_set_default(self):
        """Test setting the default host configuration."""
        with patch("instill.config.CONFIG_DIR", self.config_dir):
            config = Configuration()

            # Set default host
            config.set_default("https://new-default.com", "new-token", True)

            assert "default" in config.hosts
            assert config.hosts["default"].url == "https://new-default.com"
            assert config.hosts["default"].token == "new-token"
            assert config.hosts["default"].secure is True

    def test_configuration_set_default_overwrites_existing(self):
        """Test that set_default overwrites existing default host."""
        with patch("instill.config.CONFIG_DIR", self.config_dir):
            config = Configuration()

            # Set default host initially
            config.set_default("https://initial.com", "initial-token", False)

            # Overwrite with new values
            config.set_default("https://overwritten.com", "overwritten-token", True)

            assert config.hosts["default"].url == "https://overwritten.com"
            assert config.hosts["default"].token == "overwritten-token"
            assert config.hosts["default"].secure is True

    def test_configuration_hosts_property(self):
        """Test the hosts property."""
        with patch("instill.config.CONFIG_DIR", self.config_dir):
            config = Configuration()

            # Add some hosts
            config._config.hosts["test1"] = _InstillHost(
                url="https://test1.com", secure=True, token="token1"
            )
            config._config.hosts["test2"] = _InstillHost(
                url="https://test2.com", secure=False, token="token2"
            )

            hosts = config.hosts

            assert len(hosts) == 3  # Including default
            assert "default" in hosts
            assert "test1" in hosts
            assert "test2" in hosts
            assert hosts["test1"].url == "https://test1.com"
            assert hosts["test2"].url == "https://test2.com"

    def test_configuration_with_environment_variable(self):
        """Test configuration with custom config path from environment variable."""
        custom_config_dir = Path(self.temp_dir.name) / "custom" / "config"
        custom_config_dir.mkdir(parents=True, exist_ok=True)

        with patch.dict(
            os.environ, {"INSTILL_SYSTEM_CONFIG_PATH": str(custom_config_dir)}
        ):
            # Re-import to get the updated CONFIG_DIR
            importlib.reload(instill.config)

            # Create a config file in the custom directory
            config_file = custom_config_dir / "config.yml"
            config_data = {
                "hosts": {
                    "custom": {
                        "url": "https://custom-env.com",
                        "secure": True,
                        "token": "env-token",
                    }
                }
            }

            with open(config_file, "w", encoding="utf-8") as f:
                yaml.dump(config_data, f)

            config = instill.config.Configuration()

            # Should have both the loaded host and a default host
            assert len(config.hosts) == 2
            assert "default" in config.hosts
            assert config.hosts["default"].url == HOST_URL_PROD
            assert "custom" in config.hosts
            assert config.hosts["custom"].url == "https://custom-env.com"
            assert config.hosts["custom"].token == "env-token"

    def test_configuration_save_excludes_none_values(self):
        """Test that save excludes None values from the output."""
        with patch("instill.config.CONFIG_DIR", self.config_dir):
            config = Configuration()

            # Save configuration
            config.save()

            # Load the saved configuration
            with open(self.config_file, "r", encoding="utf-8") as f:
                saved_data = yaml.load(f, Loader=yaml.FullLoader)

            # Verify no None values in the saved data
            def check_no_none_values(data):
                if isinstance(data, dict):
                    for key, value in data.items():
                        assert value is not None, f"Found None value for key: {key}"
                        check_no_none_values(value)
                elif isinstance(data, list):
                    for item in data:
                        check_no_none_values(item)

            check_no_none_values(saved_data)

    def test_configuration_with_complex_yaml(self):
        """Test configuration with complex YAML structure."""
        with patch("instill.config.CONFIG_DIR", self.config_dir):
            # Ensure the config directory exists before writing the file
            self.config_dir.mkdir(parents=True, exist_ok=True)

            # Create a complex config file
            config_data = {
                "hosts": {
                    "production": {
                        "url": "https://api.instill.tech",
                        "secure": True,
                        "token": "prod-token-123",
                    },
                    "staging": {
                        "url": "https://staging.instill.tech",
                        "secure": True,
                        "token": "staging-token-456",
                    },
                    "development": {
                        "url": "http://localhost:8080",
                        "secure": False,
                        "token": "",
                    },
                }
            }

            with open(self.config_file, "w", encoding="utf-8") as f:
                yaml.dump(config_data, f)

            config = Configuration()

            # Verify all hosts are loaded correctly (including default)
            assert len(config.hosts) == 4  # Including default
            assert config.hosts["production"].url == "https://api.instill.tech"
            assert config.hosts["production"].token == "prod-token-123"
            assert config.hosts["production"].secure is True
            assert config.hosts["staging"].url == "https://staging.instill.tech"
            assert config.hosts["staging"].token == "staging-token-456"
            assert config.hosts["staging"].secure is True
            assert config.hosts["development"].url == "http://localhost:8080"
            assert config.hosts["development"].token == ""
            assert config.hosts["development"].secure is False
            # Default host should still be present
            assert "default" in config.hosts
            assert config.hosts["default"].url == HOST_URL_PROD


class TestGlobalConfig:
    """Test cases for the global configuration instance."""

    def test_global_config_singleton(self):
        """Test that global_config is a singleton instance."""
        temp_dir = Path(tempfile.mkdtemp())

        with patch("instill.config.CONFIG_DIR", temp_dir):
            # Import the module to get the global instance

            importlib.reload(instill.config)

            # Get the global config instance
            config1 = instill.config.global_config
            config2 = instill.config.global_config

            assert config1 is config2
            # Test that it has the expected attributes instead of using isinstance
            assert hasattr(config1, "hosts")
            assert hasattr(config1, "save")
            assert hasattr(config1, "set_default")

    def test_global_config_has_default_host(self):
        """Test that global_config has a default host."""
        temp_dir = Path(tempfile.mkdtemp())

        with patch("instill.config.CONFIG_DIR", temp_dir):
            # Import the module to get the global instance

            importlib.reload(instill.config)

            config = instill.config.global_config

            assert "default" in config.hosts
            assert config.hosts["default"].url == HOST_URL_PROD
            assert config.hosts["default"].secure is True
            assert config.hosts["default"].token == ""


class TestConfigurationIntegration:
    """Integration tests for the Configuration class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.config_dir = Path(self.temp_dir.name) / "instill" / "sdk" / "python"
        self.config_file = self.config_dir / "config.yml"

    def teardown_method(self):
        """Clean up test fixtures."""
        self.temp_dir.cleanup()

    def test_full_configuration_workflow(self):
        """Test a complete configuration workflow: create, modify, save, reload."""
        with patch("instill.config.CONFIG_DIR", self.config_dir):
            # Ensure the config directory exists before creating Configuration
            self.config_dir.mkdir(parents=True, exist_ok=True)

            # Create initial configuration
            config1 = Configuration()

            # Add multiple hosts
            config1.set_default("https://default.com", "default-token", True)
            config1._config.hosts["custom1"] = _InstillHost(
                url="https://custom1.com", secure=False, token="token1"
            )
            config1._config.hosts["custom2"] = _InstillHost(
                url="https://custom2.com", secure=True, token="token2"
            )

            # Save configuration
            config1.save()

            # Create new configuration instance (simulating reload)
            config2 = Configuration()

            # Verify all hosts are preserved
            assert len(config2.hosts) == 3
            assert config2.hosts["default"].url == "https://default.com"
            assert config2.hosts["default"].token == "default-token"
            assert config2.hosts["default"].secure is True
            assert config2.hosts["custom1"].url == "https://custom1.com"
            assert config2.hosts["custom1"].token == "token1"
            assert config2.hosts["custom1"].secure is False
            assert config2.hosts["custom2"].url == "https://custom2.com"
            assert config2.hosts["custom2"].token == "token2"
            assert config2.hosts["custom2"].secure is True

    def test_configuration_with_complex_yaml(self):
        """Test configuration with complex YAML structure."""
        with patch("instill.config.CONFIG_DIR", self.config_dir):
            # Ensure the config directory exists before writing the file
            self.config_dir.mkdir(parents=True, exist_ok=True)

            # Create a complex config file
            config_data = {
                "hosts": {
                    "production": {
                        "url": "https://api.instill.tech",
                        "secure": True,
                        "token": "prod-token-123",
                    },
                    "staging": {
                        "url": "https://staging.instill.tech",
                        "secure": True,
                        "token": "staging-token-456",
                    },
                    "development": {
                        "url": "http://localhost:8080",
                        "secure": False,
                        "token": "",
                    },
                }
            }

            with open(self.config_file, "w", encoding="utf-8") as f:
                yaml.dump(config_data, f)

            config = Configuration()

            # Verify all hosts are loaded correctly (including default)
            assert len(config.hosts) == 4  # Including default
            assert config.hosts["production"].url == "https://api.instill.tech"
            assert config.hosts["production"].token == "prod-token-123"
            assert config.hosts["production"].secure is True
            assert config.hosts["staging"].url == "https://staging.instill.tech"
            assert config.hosts["staging"].token == "staging-token-456"
            assert config.hosts["staging"].secure is True
            assert config.hosts["development"].url == "http://localhost:8080"
            assert config.hosts["development"].token == ""
            assert config.hosts["development"].secure is False
            # Default host should still be present
            assert "default" in config.hosts
            assert config.hosts["default"].url == HOST_URL_PROD
