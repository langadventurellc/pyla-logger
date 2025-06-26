import pytest
from unittest.mock import Mock, patch
import structlog

from pyla_logger.logger import Logger


class TestLogger:
    def setup_method(self):
        self.mock_logger = Mock()
        self.logger = Logger(self.mock_logger)

    def test_init(self):
        assert self.logger.logger == self.mock_logger
        assert self.logger.context == {}

    def test_add_context(self):
        self.logger.add_context(key1="value1", key2="value2")
        assert self.logger.context == {"key1": "value1", "key2": "value2"}
        
        self.logger.add_context(key3="value3")
        assert self.logger.context == {"key1": "value1", "key2": "value2", "key3": "value3"}

    def test_debug(self):
        self.logger.add_context(context_key="context_value")
        self.logger.debug("debug message", extra_key="extra_value")
        
        self.mock_logger.debug.assert_called_once_with(
            "debug message", 
            extra_key="extra_value", 
            context_key="context_value"
        )

    def test_info(self):
        self.logger.add_context(context_key="context_value")
        self.logger.info("info message", extra_key="extra_value")
        
        self.mock_logger.info.assert_called_once_with(
            "info message", 
            extra_key="extra_value", 
            context_key="context_value"
        )

    def test_warning(self):
        self.logger.add_context(context_key="context_value")
        self.logger.warning("warning message", extra_key="extra_value")
        
        self.mock_logger.warning.assert_called_once_with(
            "warning message", 
            extra_key="extra_value", 
            context_key="context_value"
        )

    def test_error(self):
        self.logger.add_context(context_key="context_value")
        self.logger.error("error message", extra_key="extra_value")
        
        self.mock_logger.error.assert_called_once_with(
            "error message", 
            extra_key="extra_value", 
            context_key="context_value"
        )

    def test_critical(self):
        self.logger.add_context(context_key="context_value")
        self.logger.critical("critical message", extra_key="extra_value")
        
        self.mock_logger.critical.assert_called_once_with(
            "critical message", 
            extra_key="extra_value", 
            context_key="context_value"
        )

    def test_exception(self):
        exc = Exception("test exception")
        self.logger.add_context(context_key="context_value")
        self.logger.exception(exc, "exception message", extra_key="extra_value")
        
        self.mock_logger.exception.assert_called_once_with(
            "exception message", 
            extra_key="extra_value", 
            context_key="context_value",
            exc_info=exc
        )

    def test_combine_with_context(self):
        self.logger.add_context(context_key="context_value")
        values = {"extra_key": "extra_value"}
        
        result = self.logger._combine_with_context(values)
        
        assert values == {"extra_key": "extra_value", "context_key": "context_value"}

    def test_logging_methods_without_context(self):
        self.logger.debug("debug message")
        self.mock_logger.debug.assert_called_once_with("debug message")
        
        self.logger.info("info message")
        self.mock_logger.info.assert_called_once_with("info message")

    def test_logging_methods_with_args(self):
        self.logger.info("message", "arg1", "arg2", key="value")
        self.mock_logger.info.assert_called_once_with("message", "arg1", "arg2", key="value")


class TestLoggerIntegration:
    @patch('pyla_logger.logger.structlog.get_logger')
    def test_logger_instance_creation(self, mock_get_logger):
        mock_structlog_logger = Mock()
        mock_get_logger.return_value = mock_structlog_logger
        
        from pyla_logger.logger import logger
        
        assert isinstance(logger, Logger)
        assert logger.logger == mock_structlog_logger
        mock_get_logger.assert_called_once()

    def test_structlog_configuration(self):
        import structlog
        
        config = structlog.get_config()
        
        assert len(config["processors"]) == 5
        assert config["wrapper_class"] is not None
        assert config["context_class"] == dict
        assert config["cache_logger_on_first_use"] is False