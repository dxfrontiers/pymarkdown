"""
Module to provide tests related to the MD050 rule.
"""
import os
from test.markdown_scanner import MarkdownScanner
from test.utils import write_temporary_configuration

import pytest


@pytest.mark.rules
def test_md050_external_reference_used():
    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md050", "internal-reference-bad.md"
    )
    message = "Links should be internal."
    supplied_configuration = {
        "log": {"level": "INFO", "stack-trace": True},
        "plugins": {
            "md050": {
                "enabled": True,
                "regexes": {
                    "1": {
                        "regex": r"^(https?:)?(\/\/)?git\.example\.com\/path\/.*$",
                        "errorMessage": message,
                    }
                },
            }
        },
    }
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        supplied_arguments = [
            "-c",
            configuration_file,
            "-e md050",
            "scan",
            source_path,
        ]

        expected_return_code = 1
        expected_output = f"{source_path}:1:1: MD050: Reference should match regular expressions [{message}] (refs-regex)"
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


@pytest.mark.rules
def test_md050_internal_reference_used():
    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md050", "internal-reference-good.md"
    )
    message = "Links should be internal."
    supplied_configuration = {
        "log": {"level": "INFO", "stack-trace": True},
        "plugins": {
            "md050": {
                "enabled": True,
                "regexes": {
                    "1": {
                        "regex": r"^(https?:)?(\/\/)?git\.example\.com\/path\/.*$",
                        "errorMessage": message,
                    }
                },
            }
        },
    }
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        supplied_arguments = [
            "-c",
            configuration_file,
            "-e md050",
            "scan",
            source_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


@pytest.mark.rules
def test_md050_ref_does_not_contain_path_traversal():
    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md050", "path-traversal-good.md"
    )
    message = "Links should not use navigation (. or ..)."
    supplied_configuration = {
        "log": {"level": "INFO", "stack-trace": True},
        "plugins": {
            "md050": {
                "enabled": True,
                "regexes": {
                    "1": {
                        "regex": r"^((^\.\.?/)|(.*/\.\.?/)).*$",
                        "errorMessage": message,
                    }
                },
            }
        },
    }
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        supplied_arguments = [
            "-c",
            configuration_file,
            "-e md050",
            "scan",
            source_path,
        ]

        expected_return_code = 0
        expected_output = ""
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)


@pytest.mark.rules
def test_md050_ref_does_contain_path_travels():
    # Arrange
    scanner = MarkdownScanner()
    source_path = os.path.join(
        "test", "resources", "rules", "md050", "path-traversal-bad.md"
    )
    message = "Links should not use path traversal (. or ..)."
    supplied_configuration = {
        "log": {"level": "INFO", "stack-trace": True},
        "plugins": {
            "md050": {
                "enabled": True,
                "regexes": {
                    "1": {
                        "regex": r"^((^\.\.?/)|(.*/\.\.?/)).*$",
                        "errorMessage": message,
                    }
                },
            }
        },
    }
    configuration_file = None
    try:
        configuration_file = write_temporary_configuration(supplied_configuration)
        supplied_arguments = [
            "-c",
            configuration_file,
            "-e md050",
            "scan",
            source_path,
        ]

        expected_return_code = 1
        expected_output = f"{source_path}:1:1: MD050: Reference should match regular expressions [{message}] (refs-regex)"
        expected_error = ""

        # Act
        execute_results = scanner.invoke_main(arguments=supplied_arguments)

        # Assert
        execute_results.assert_results(
            expected_output, expected_error, expected_return_code
        )
    finally:
        if configuration_file and os.path.exists(configuration_file):
            os.remove(configuration_file)
