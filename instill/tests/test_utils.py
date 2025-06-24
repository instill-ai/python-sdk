"""Unit tests for the instill.utils module."""

# pylint: disable=unused-argument,unused-variable
import logging
import os
import tempfile
from unittest.mock import MagicMock, patch

import grpc
import pytest

from instill.utils.error_handler import (
    NamespaceException,
    NotServingException,
    grpc_handler,
)
from instill.utils.logger import Logger
from instill.utils.process_file import get_file_type, process_file


class TestLogger:
    """Test cases for the Logger class."""

    def setup_method(self):
        """Set up test fixtures."""
        # Reset logger state before each test
        Logger.Initialized = False

    def test_logger_initialization(self):
        """Test logger initialization."""
        # Test that logger is not initialized initially
        assert Logger.Initialized is False

        # Initialize logger
        Logger.initialize()

        # Test that logger is now initialized
        assert Logger.Initialized is True

    def test_logger_singleton_pattern(self):
        """Test that logger follows singleton pattern."""
        # Initialize logger twice
        Logger.initialize()
        initial_state = Logger.Initialized

        Logger.initialize()

        # Should remain initialized
        assert Logger.Initialized is True

    def test_logger_handler_setup(self):
        """Test that logger has correct handlers."""
        Logger.initialize()

        # Get the root logger
        logger = logging.getLogger()

        # Check that logger has handlers
        assert len(logger.handlers) >= 3  # runlog, errorlog, and console handlers

        # Check for specific handler types
        file_handlers = [
            h for h in logger.handlers if isinstance(h, logging.FileHandler)
        ]
        stream_handlers = [
            h for h in logger.handlers if isinstance(h, logging.StreamHandler)
        ]

        assert len(file_handlers) >= 2  # runlog and errorlog handlers
        assert len(stream_handlers) >= 1  # console handler

    def test_logger_level(self):
        """Test logger level."""
        Logger.initialize()
        logger = logging.getLogger()

        # Default level should be INFO
        assert logger.level == logging.INFO

    def test_logger_format(self):
        """Test logger format."""
        Logger.initialize()
        logger = logging.getLogger()

        # Check that formatter is set
        for handler in logger.handlers:
            if handler.formatter:
                format_string = handler.formatter._fmt
                if format_string is not None:
                    assert "%(asctime)s" in format_string
                    assert (
                        "%(levelname)" in format_string
                    )  # Check for levelname with any modifiers
                    assert "%(message)s" in format_string

    def test_logger_logging_methods(self):
        """Test logger logging methods."""
        Logger.initialize()

        # Test all logging methods
        Logger.d("debug message")
        Logger.i("info message")
        Logger.w("warning message")
        Logger.e("error message")

        # These should not raise exceptions
        assert True

    def test_logger_exception_method(self):
        """Test logger exception method."""
        Logger.initialize()

        # Test exception logging
        try:
            raise ValueError("Test exception")
        except ValueError:
            Logger.exception("Exception occurred")

        # Should not raise exception
        assert True

    def test_logger_uninitialized_error(self):
        """Test that logger methods fail when not initialized."""
        # Reset to uninitialized state
        Logger.Initialized = False

        # All methods should raise AssertionError when not initialized
        with pytest.raises(AssertionError, match="Logger has not been initialized"):
            Logger.d("test")

        with pytest.raises(AssertionError, match="Logger has not been initialized"):
            Logger.i("test")

        with pytest.raises(AssertionError, match="Logger has not been initialized"):
            Logger.w("test")

        with pytest.raises(AssertionError, match="Logger has not been initialized"):
            Logger.e("test")

        with pytest.raises(AssertionError, match="Logger has not been initialized"):
            Logger.exception("test")

    def test_logger_custom_paths(self):
        """Test logger initialization with custom paths."""
        with tempfile.TemporaryDirectory() as temp_dir:
            runlog_path = os.path.join(temp_dir, "run.log")
            errorlog_path = os.path.join(temp_dir, "error.log")

            Logger.initialize(runlog_path=runlog_path, errorlog_path=errorlog_path)

            # Check that files were created
            assert os.path.exists(runlog_path)
            assert os.path.exists(errorlog_path)

            # Test logging
            Logger.i("test message")

            # Check that message was written to run log
            with open(runlog_path, "r", encoding="utf-8") as f:
                content = f.read()
                assert "test message" in content


class TestErrorHandler:
    """Test cases for error handling utilities."""

    def test_not_serving_exception(self):
        """Test NotServingException."""
        exception = NotServingException()
        assert str(exception) == "target host is not serving"

        custom_message = "Custom error message"
        exception = NotServingException(custom_message)
        assert str(exception) == custom_message

    def test_namespace_exception(self):
        """Test NamespaceException."""
        exception = NamespaceException()
        assert str(exception) == "namespace ID not available"

        custom_message = "Custom namespace error"
        exception = NamespaceException(custom_message)
        assert str(exception) == custom_message

    @patch("instill.utils.error_handler.Logger")
    @patch("os._exit")
    def test_grpc_handler_not_serving(self, mock_exit, mock_logger):
        """Test grpc_handler when target is not serving."""
        # Create a mock object that returns False for is_serving()
        mock_obj = MagicMock()
        mock_obj.is_serving.return_value = False

        # Create a test function
        def test_func(obj, *args, **kwargs):
            return "success"

        # Apply the decorator
        decorated_func = grpc_handler(test_func)

        # Call the decorated function with the mock object as first argument
        decorated_func(mock_obj)

        # Verify is_serving was called
        mock_obj.is_serving.assert_called_once()

        # Verify that Logger.exception was called (because NotServingException was caught)
        mock_logger.exception.assert_called_once()

        # Verify that os._exit was called with exit code 1
        mock_exit.assert_called_once_with(1)

    @patch("instill.utils.error_handler.Logger")
    @patch("os._exit")
    def test_grpc_handler_serving_success(self, mock_exit, mock_logger):
        """Test grpc_handler when target is serving and function succeeds."""
        # Create a mock object that returns True for is_serving()
        mock_obj = MagicMock()
        mock_obj.is_serving.return_value = True

        # Create a test function
        def test_func(obj, *args, **kwargs):
            return "success"

        # Apply the decorator
        decorated_func = grpc_handler(test_func)

        # Call the decorated function
        result = decorated_func(mock_obj)

        # Verify result
        assert result == "success"
        mock_obj.is_serving.assert_called_once()

    @patch("instill.utils.error_handler.Logger")
    @patch("os._exit")
    def test_grpc_handler_grpc_error(self, mock_exit, mock_logger):
        """Test grpc_handler when GRPC error occurs."""
        # Create a mock object that returns True for is_serving()
        mock_obj = MagicMock()
        mock_obj.is_serving.return_value = True

        # Create a proper GRPC error that inherits from grpc.RpcError
        class MockRpcError(grpc.RpcError):
            def code(self):
                return grpc.StatusCode.UNAVAILABLE

            def details(self):
                return "Service unavailable"

        # Create a test function that raises the mock GRPC error
        def test_func(obj, *args, **kwargs):
            raise MockRpcError()

        # Apply the decorator
        decorated_func = grpc_handler(test_func)

        # Call the decorated function
        decorated_func(mock_obj)

        # Verify that Logger.w was called twice (once for code, once for details)
        assert mock_logger.w.call_count == 2
        mock_logger.w.assert_any_call(grpc.StatusCode.UNAVAILABLE)
        mock_logger.w.assert_any_call("Service unavailable")

        # Verify that os._exit was called with exit code 1
        mock_exit.assert_called_once_with(1)

    @patch("instill.utils.error_handler.Logger")
    @patch("os._exit")
    def test_grpc_handler_grpc_error_silent(self, mock_exit, mock_logger):
        """Test grpc_handler when GRPC error occurs with silent=True."""
        # Create a mock object that returns True for is_serving()
        mock_obj = MagicMock()
        mock_obj.is_serving.return_value = True

        # Create a proper GRPC error class that inherits from grpc.RpcError
        class MockRpcError(grpc.RpcError):
            def code(self):
                return grpc.StatusCode.UNAVAILABLE

            def details(self):
                return "Service unavailable"

        # Create a test function that raises the proper GRPC error
        def test_func(obj, *args, **kwargs):
            raise MockRpcError()

        # Apply the decorator
        decorated_func = grpc_handler(test_func)

        # Call the decorated function with silent=True
        decorated_func(mock_obj, silent=True)

        # Verify that Logger.w was NOT called (because silent=True)
        mock_logger.w.assert_not_called()

        # Verify that os._exit was NOT called (because silent=True)
        mock_exit.assert_not_called()

    @patch("instill.utils.error_handler.Logger")
    @patch("os._exit")
    def test_grpc_handler_general_exception(self, mock_exit, mock_logger):
        """Test grpc_handler when general exception occurs."""
        # Create a mock object that returns True for is_serving()
        mock_obj = MagicMock()
        mock_obj.is_serving.return_value = True

        # Create a test function that raises general exception
        def test_func(obj, *args, **kwargs):
            raise ValueError("Test error")

        # Apply the decorator
        decorated_func = grpc_handler(test_func)

        # Call the decorated function
        decorated_func(mock_obj)

        # Verify that Logger.exception was called and os._exit was called
        mock_logger.exception.assert_called_once()
        mock_exit.assert_called_once_with(1)


class TestProcessFile:
    """Test cases for file processing utilities."""

    def test_get_file_type_text(self):
        """Test get_file_type for text files."""
        # Test various text file extensions that are actually supported
        text_extensions = [".txt", ".log", ".ini", ".csv"]

        for ext in text_extensions:
            with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as temp_file:
                temp_file.write(b"Some text content")
                temp_file.flush()

                file_type = get_file_type(temp_file.name, ext)
                assert file_type == "FILE_TYPE_TEXT"

                # Clean up
                os.unlink(temp_file.name)

    def test_get_file_type_markdown(self):
        """Test get_file_type for markdown files."""
        with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as temp_file:
            temp_file.write(b"# Markdown content")
            temp_file.flush()

            file_type = get_file_type(temp_file.name, ".md")
            assert file_type == "FILE_TYPE_MARKDOWN"

            # Clean up
            os.unlink(temp_file.name)

    def test_get_file_type_html(self):
        """Test get_file_type for HTML files."""
        with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as temp_file:
            temp_file.write(b"<html><body>Content</body></html>")
            temp_file.flush()

            file_type = get_file_type(temp_file.name, ".html")
            assert file_type == "FILE_TYPE_HTML"

            # Clean up
            os.unlink(temp_file.name)

    def test_get_file_type_pdf(self):
        """Test get_file_type for PDF files."""
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
            temp_file.write(b"%PDF-1.4\nfake pdf content")
            temp_file.flush()

            file_type = get_file_type(temp_file.name, ".pdf")
            assert file_type == "FILE_TYPE_PDF"

            # Clean up
            os.unlink(temp_file.name)

    def test_get_file_type_office_documents(self):
        """Test get_file_type for Office documents."""
        office_extensions = [".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx"]

        for ext in office_extensions:
            with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as temp_file:
                temp_file.write(b"fake office document content")
                temp_file.flush()

                file_type = get_file_type(temp_file.name, ext)
                expected_type = ext.upper().replace(".", "FILE_TYPE_")
                assert file_type == expected_type

                # Clean up
                os.unlink(temp_file.name)

    def test_get_file_type_unknown_extension(self):
        """Test get_file_type for unknown file extensions."""
        with tempfile.NamedTemporaryFile(suffix=".unknown", delete=False) as temp_file:
            temp_file.write(b"some data")
            temp_file.flush()

            # Should raise ValueError for unknown extension
            with pytest.raises(ValueError, match="Unsupported file type"):
                get_file_type(temp_file.name, ".unknown")

            # Clean up
            os.unlink(temp_file.name)

    def test_get_file_type_content_based_detection(self):
        """Test get_file_type content-based detection for unknown extensions."""
        # Test PDF detection by content
        with tempfile.NamedTemporaryFile(suffix=".unknown", delete=False) as temp_file:
            temp_file.write(b"%PDF-1.4\nfake pdf content")
            temp_file.flush()

            file_type = get_file_type(temp_file.name, ".unknown")
            assert file_type == "FILE_TYPE_PDF"

            # Clean up
            os.unlink(temp_file.name)

        # Test HTML detection by content
        with tempfile.NamedTemporaryFile(suffix=".unknown", delete=False) as temp_file:
            temp_file.write(b"<!DOCTYPE html><html><body>Content</body></html>")
            temp_file.flush()

            file_type = get_file_type(temp_file.name, ".unknown")
            assert file_type == "FILE_TYPE_HTML"

            # Clean up
            os.unlink(temp_file.name)

    def test_get_file_type_office_xml_detection(self):
        """Test get_file_type for Office XML formats detection."""
        # Test DOCX detection
        with tempfile.NamedTemporaryFile(suffix=".unknown", delete=False) as temp_file:
            temp_file.write(b"PK\x03\x04[Content_Types].xmlword/document.xml")
            temp_file.flush()

            file_type = get_file_type(temp_file.name, ".unknown")
            assert file_type == "FILE_TYPE_DOCX"

            # Clean up
            os.unlink(temp_file.name)

    def test_process_file_text(self):
        """Test process_file for text files."""
        # Create a temporary text file
        with tempfile.NamedTemporaryFile(
            suffix=".txt", mode="w", delete=False
        ) as temp_file:
            temp_file.write("Test content")
            temp_file.flush()

            # Process the file
            result = process_file(temp_file.name)

            # Verify result properties
            assert result.name == os.path.basename(temp_file.name)
            assert result.type == 1  # FILE_TYPE_TEXT enum value
            assert result.content is not None
            assert len(result.content) > 0

            # Clean up
            os.unlink(temp_file.name)

    def test_process_file_markdown(self):
        """Test process_file for markdown files."""
        # Create a temporary markdown file
        with tempfile.NamedTemporaryFile(
            suffix=".md", mode="w", delete=False
        ) as temp_file:
            temp_file.write("# Test markdown")
            temp_file.flush()

            # Process the file
            result = process_file(temp_file.name)

            # Verify result properties
            assert result.name == os.path.basename(temp_file.name)
            assert result.type == 3  # FILE_TYPE_MARKDOWN enum value
            assert result.content is not None
            assert len(result.content) > 0

            # Clean up
            os.unlink(temp_file.name)

    def test_process_file_nonexistent(self):
        """Test process_file with nonexistent file."""
        with pytest.raises(FileNotFoundError):
            process_file("nonexistent_file.txt")

    def test_process_file_directory(self):
        """Test process_file with directory path."""
        with tempfile.TemporaryDirectory() as temp_dir:
            with pytest.raises(IsADirectoryError):
                process_file(temp_dir)

    def test_get_file_type_unsupported_extensions(self):
        """Test get_file_type for unsupported file extensions."""
        unsupported_extensions = [".js", ".css", ".json", ".xml", ".py", ".java"]

        for ext in unsupported_extensions:
            with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as temp_file:
                temp_file.write(b"Some content")
                temp_file.flush()

                # Should raise ValueError for unsupported extensions
                with pytest.raises(ValueError, match="Unsupported file type"):
                    get_file_type(temp_file.name, ext)

                # Clean up
                os.unlink(temp_file.name)


if __name__ == "__main__":
    pytest.main([__file__])
