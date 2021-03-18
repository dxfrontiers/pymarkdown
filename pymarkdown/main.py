"""
Module to provide for a simple implementation of a title case algorithm.
"""
import argparse
import glob
import logging
import os
import sys
import traceback

from pymarkdown.application_properties import (
    ApplicationProperties,
    ApplicationPropertiesJsonLoader,
)
from pymarkdown.bad_tokenization_error import BadTokenizationError
from pymarkdown.parser_logger import ParserLogger
from pymarkdown.plugin_manager import BadPluginError, PluginManager
from pymarkdown.source_providers import FileSourceProvider
from pymarkdown.tokenized_markdown import TokenizedMarkdown

POGGER = ParserLogger(logging.getLogger(__name__))

LOGGER = logging.getLogger(__name__)


class PyMarkdownLint:
    """
    Class to provide for a simple implementation of a title case algorithm.
    """

    available_log_maps = {
        "CRITICAL": logging.CRITICAL,
        "ERROR": logging.ERROR,
        "WARNING": logging.WARNING,
        "INFO": logging.INFO,
        "DEBUG": logging.DEBUG,
    }

    def __init__(self):
        self.__version_number = "0.1.0"
        self.__show_stack_trace = False

        self.__properties = ApplicationProperties()

        self.__plugins = PluginManager()
        self.__tokenizer = None
        self.default_log_level = "CRITICAL"

    @staticmethod
    def log_level_type(argument):
        """
        Function to help argparse limit the valid log levels.
        """
        if argument in PyMarkdownLint.available_log_maps:
            return argument
        raise ValueError(f"Value '{argument}' is not a valid log level.")

    def __parse_arguments(self):
        parser = argparse.ArgumentParser(description="Lint any found Markdown files.")

        parser.add_argument(
            "-e",
            "--enable-rules",
            dest="enable_rules",
            action="store",
            default="",
            help="comma separated list of rules to enable",
        )
        parser.add_argument(
            "-d",
            "--disable-rules",
            dest="disable_rules",
            action="store",
            default="",
            help="comma separated list of rules to disable",
        )
        parser.add_argument(
            "-x-scan",
            dest="x_test_scan_fault",
            action="store_true",
            default="",
            help=argparse.SUPPRESS,
        )
        parser.add_argument(
            "-x-init",
            dest="x_test_init_fault",
            action="store_true",
            default="",
            help=argparse.SUPPRESS,
        )
        parser.add_argument(
            "--add-plugin",
            dest="add_plugin",
            action="append",
            default=None,
            help="path to a plugin containing a new rule to apply",
        )
        parser.add_argument(
            "--config",
            "-c",
            dest="configuration_file",
            action="store",
            default=None,
            help="path to the configuration file to use",
        )
        parser.add_argument(
            "--stack-trace",
            dest="show_stack_trace",
            action="store_true",
            default=False,
            help="if an error occurs, print out the stack trace for debug purposes",
        )
        parser.add_argument(
            "--log-level",
            dest="log_level",
            action="store",
            help="minimum level required to log messages",
            type=PyMarkdownLint.log_level_type,
            choices=list(PyMarkdownLint.available_log_maps.keys()),
        )
        parser.add_argument(
            "--log-file",
            dest="log_file",
            action="store",
            help="destination file for log messages",
        )

        subparsers = parser.add_subparsers(dest="frodo")

        new_sub_parser = subparsers.add_parser("plugins", help="B command")
        new_sub_parser.add_argument(
            "-p",
            "--list-plugins",
            dest="list_plugins",
            action="store_true",
            default=False,
            help="list the available plugins and exit",
        )
        new_sub_parser.add_argument(
            "paths",
            metavar="path",
            type=str,
            nargs="+",
            help="one or more paths to scan for eligible Markdown files",
        )

        new_sub_parser = subparsers.add_parser(
            "scan", help="scan the Markdown files in the specified paths"
        )
        new_sub_parser.add_argument(
            "-l",
            "--list-files",
            dest="list_files",
            action="store_true",
            default=False,
            help="list the markdown files found and exit",
        )
        new_sub_parser.add_argument(
            "paths",
            metavar="path",
            type=str,
            nargs="+",
            help="one or more paths to scan for eligible Markdown files",
        )

        subparsers.add_parser("version", help="version of the application")

        parse_arguments = parser.parse_args()

        if not parse_arguments.frodo:
            parser.print_help()
            sys.exit(2)
        elif parse_arguments.frodo == "version":
            print(f"{self.__version_number}")
            sys.exit(0)
        return parse_arguments

    @classmethod
    def __is_file_eligible_to_scan(cls, path_to_test):
        """
        Determine if the presented path is one that we want to scan.
        """
        return path_to_test.endswith(".md")

    # pylint: disable=broad-except
    def __scan_file(self, args, next_file):
        """
        Scan a given file and call the plugin manager for any significant events.
        """

        POGGER.info(f"Scanning file '{next_file}'.")
        source_provider = FileSourceProvider(next_file)

        POGGER.info(f"Scanning file '{next_file}' line-by-line.")
        line_number = 1
        next_line = source_provider.get_next_line()
        context = self.__plugins.starting_new_file(next_file)
        while next_line is not None:
            self.__plugins.next_line(context, line_number, next_line)
            line_number += 1
            next_line = source_provider.get_next_line()

        POGGER.info(f"Scanning file '{next_file}' token-by-token.")
        source_provider = FileSourceProvider(next_file)
        if args.x_test_scan_fault:
            source_provider = None
        actual_tokens = self.__tokenizer.transform_from_provider(source_provider)

        for next_token in actual_tokens:
            self.__plugins.next_token(context, next_token)

        POGGER.info(f"Complated scanning file '{next_file}'.")
        self.__plugins.completed_file(context, line_number)

    # pylint: enable=broad-except

    def __process_next_path(self, next_path, files_to_parse):

        did_find_any = False
        POGGER.info("Determining files to scan for path '$'.", next_path)
        if not os.path.exists(next_path):
            print(
                f"Provided path '{next_path}' does not exist.",
                file=sys.stderr,
            )
            POGGER.debug("Provided path '$' does not exist.", next_path)
        elif os.path.isdir(next_path):
            POGGER.debug(
                "Provided path '$' is a directory. Walking directory.", next_path
            )
            did_find_any = True
            for root, _, files in os.walk(next_path):
                root = root.replace("\\", "/")
                for file in files:
                    rooted_file_path = f"{root}/{file}"
                    if self.__is_file_eligible_to_scan(rooted_file_path):
                        files_to_parse.add(rooted_file_path)
        else:
            if self.__is_file_eligible_to_scan(next_path):
                POGGER.debug(
                    "Provided path '$' is a valid file. Adding.",
                    next_path,
                )
                files_to_parse.add(next_path)
                did_find_any = True
            else:
                POGGER.debug(
                    "Provided path '$' is not a valid file. Skipping.",
                    next_path,
                )
                print(
                    f"Provided file path '{next_path}' is not a valid file. Skipping.",
                    file=sys.stderr,
                )
        return did_find_any

    def __determine_files_to_scan(self, eligible_paths):

        did_error_scanning_files = False
        files_to_parse = set()
        for next_path in eligible_paths:
            if "*" in next_path or "?" in next_path:
                globbed_paths = glob.glob(next_path)
                if not globbed_paths:
                    print(
                        f"Provided glob path '{next_path}' did not match any files.",
                        file=sys.stderr,
                    )
                    did_error_scanning_files = True
                    break
                for next_globbed_path in globbed_paths:
                    next_globbed_path = next_globbed_path.replace("\\", "/")
                    self.__process_next_path(next_globbed_path, files_to_parse)
            else:
                if not self.__process_next_path(next_path, files_to_parse):
                    did_error_scanning_files = True
                    break

        files_to_parse = list(files_to_parse)
        files_to_parse.sort()

        POGGER.info("Number of files found: $", len(files_to_parse))
        return files_to_parse, did_error_scanning_files

    @classmethod
    def __handle_list_files(cls, files_to_scan):

        if files_to_scan:
            print("\n".join(files_to_scan))
            return 0
        print("No matching files found.", file=sys.stderr)
        return 1

    def __handle_list_plugins(self):
        print("\n".join(self.__plugins.all_plugin_ids))
        return 0

    def __apply_configuration_to_plugins(self):

        try:
            self.__plugins.apply_configuration(self.__properties)
        except BadPluginError as this_exception:
            formatted_error = f"{str(type(this_exception).__name__)} encountered while configuring plugins:\n{str(this_exception)}"
            self.__handle_error(formatted_error)

    def __initialize_parser(self, args):

        resource_path = None
        if args.x_test_init_fault:
            resource_path = "fredo"

        try:
            self.__tokenizer = TokenizedMarkdown(resource_path)
            self.__tokenizer.apply_configuration(self.__properties)
        except BadTokenizationError as this_exception:
            formatted_error = f"{str(type(this_exception).__name__)} encountered while initializing tokenizer:\n{str(this_exception)}"
            self.__handle_error(formatted_error)

    def __initialize_plugin_manager(self, args, plugin_dir):
        """
        Make sure all plugins are ready before being initialized.
        """

        self.__plugins = PluginManager()
        try:
            self.__plugins.initialize(
                plugin_dir,
                args.add_plugin,
                args.enable_rules,
                args.disable_rules,
                self.__properties,
            )
        except BadPluginError as this_exception:
            formatted_error = f"BadPluginError encountered while loading plugins:\n{str(this_exception)}"
            self.__handle_error(formatted_error)

    def __handle_error(self, formatted_error):

        LOGGER.warning(formatted_error, exc_info=True)
        print(f"\n\n{formatted_error}", file=sys.stderr)
        if self.__show_stack_trace:
            traceback.print_exc(file=sys.stderr)
        sys.exit(1)

    def __handle_scan_error(self, next_file, this_exception):

        formatted_error = f"{str(type(this_exception).__name__)} encountered while scanning '{next_file}':\n{str(this_exception)}"
        self.__handle_error(formatted_error)

    def __set_initial_state(self, args):

        self.__show_stack_trace = args.show_stack_trace
        base_logger = logging.getLogger()
        base_logger.setLevel(
            logging.DEBUG if self.__show_stack_trace else logging.WARNING
        )

        if args.configuration_file:
            LOGGER.debug("Loading configuration file: %s", args.configuration_file)
            ApplicationPropertiesJsonLoader.load_and_set(
                self.__properties, args.configuration_file, self.__handle_error
            )

    def __initialize_logging(self, args):

        new_handler = None
        effective_log_file = args.log_file
        if effective_log_file is None:
            effective_log_file = self.__properties.get_string_property("log.file")

        if effective_log_file:
            new_handler = logging.FileHandler(args.log_file)
            logging.getLogger().addHandler(new_handler)

        effective_log_level = args.log_level if args.log_level else None
        if effective_log_level is None:
            effective_log_level = self.__properties.get_string_property(
                "log.level", valid_value_fn=PyMarkdownLint.log_level_type
            )
        if effective_log_level is None:
            effective_log_level = self.default_log_level

        log_level_to_enact = PyMarkdownLint.available_log_maps[effective_log_level]

        logging.getLogger().setLevel(log_level_to_enact)
        ParserLogger.sync_on_next_call()
        return new_handler

    def __initialize_plugins(self, args):
        try:
            plugin_dir = os.path.dirname(os.path.realpath(__file__))
            plugin_dir = os.path.join(plugin_dir, "plugins")
            self.__initialize_plugin_manager(args, plugin_dir)
            self.__apply_configuration_to_plugins()
        except ValueError as this_exception:
            formatted_error = f"{str(type(this_exception).__name__)} encountered while initializing plugins:\n{str(this_exception)}"
            self.__handle_error(formatted_error)

    def main(self):
        """
        Main entrance point.
        """
        args = self.__parse_arguments()
        self.__set_initial_state(args)

        new_handler = None
        total_error_count = 0
        try:
            new_handler = self.__initialize_logging(args)

            if args.frodo == "plugins":
                self.__initialize_plugins(args)
                return_code = self.__handle_list_plugins()
                sys.exit(return_code)

            POGGER.info("Determining files to scan.")
            files_to_scan, did_error_scanning_files = self.__determine_files_to_scan(
                args.paths
            )
            if did_error_scanning_files:
                total_error_count = 1
            else:
                self.__initialize_plugins(args)
                self.__initialize_parser(args)

                if args.list_files:
                    POGGER.info(
                        "Sending list of files that would have been scanned to stdout."
                    )
                    return_code = self.__handle_list_files(files_to_scan)
                    sys.exit(return_code)

                for next_file in files_to_scan:
                    try:
                        self.__scan_file(args, next_file)
                    except BadPluginError as this_exception:
                        self.__handle_scan_error(next_file, this_exception)
                    except BadTokenizationError as this_exception:
                        self.__handle_scan_error(next_file, this_exception)
        finally:
            if new_handler:
                new_handler.close()
        if self.__plugins.number_of_scan_failures or total_error_count:
            sys.exit(1)


if __name__ == "__main__":
    PyMarkdownLint().main()
