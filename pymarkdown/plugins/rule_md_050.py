"""
Module to implement a plugin that validates references based on configurable regexes.
"""
import dataclasses
import re
from typing import Generator, List, Optional, Pattern, Tuple, cast

from pymarkdown.inline_markdown_token import ReferenceMarkdownToken
from pymarkdown.markdown_token import MarkdownToken
from pymarkdown.plugin_manager.plugin_details import PluginDetails
from pymarkdown.plugin_manager.plugin_scan_context import PluginScanContext
from pymarkdown.plugin_manager.rule_plugin import RulePlugin


class RuleMd050(RulePlugin):
    """
    Class to implement a plugin that validates references based on configurable regexes.
    """

    def __init__(self) -> None:
        super().__init__()
        self.__regexes: List[RegexPair] = []

    def get_details(self) -> PluginDetails:
        """
        Get the details for the plugin.
        """
        return PluginDetails(
            plugin_name="refs-regex",
            plugin_id="MD050",
            plugin_enabled_by_default=False,
            plugin_description="Reference should match regular expressions",
            plugin_version="0.0.1",
            plugin_interface_version=1,
            plugin_url="https://github.com/jackdewinter/pymarkdown/blob/main/docs/rules/rule_md050.md",
            plugin_configuration="regexes",
        )

    def initialize_from_config(self) -> None:
        """
        Event to allow the plugin to load configuration information.
        """
        for index in self.config_indeces():
            self.__regexes.append(
                RegexPair(
                    re.compile(
                        self.plugin_configuration.get_string_property(
                            f"regexes.{index}.regex"
                        )
                    ),
                    self.plugin_configuration.get_string_property(
                        f"regexes.{index}.errorMessage"
                    ),
                )
            )

    def config_indeces(self) -> Generator[int, None, None]:
        """
        Generator for indices for variable-size list of config arguments.
        """
        idx = 1

        while (
            self.plugin_configuration.get_string_property(f"regexes.{idx}.regex")
            is not None
        ):
            yield idx
            idx += 1

    def next_token(self, context: PluginScanContext, token: MarkdownToken) -> None:
        """
        Event that a new token is being processed.
        """
        if not token.is_inline_image and not token.is_inline_link:
            return
        link_uri, _ = self._extract_link_uri(token)
        for regex in self.__regexes:
            if regex.regex.match(link_uri):
                self.report_next_token_error(
                    context, token, extra_error_information=regex.error_message
                )

    @staticmethod
    def _extract_link_uri(token: MarkdownToken) -> Tuple[str, Optional[str]]:
        """
        Extract the relevant link part of the URI
        """
        ref_token = cast(ReferenceMarkdownToken, token)
        link_uri_split = ref_token.link_uri.split("#", 1)
        if len(link_uri_split) == 2:
            return link_uri_split[0], link_uri_split[1]

        return link_uri_split[0], None


@dataclasses.dataclass
class RegexPair:
    """
    Class to contain the regex and its error message.
    """

    regex: Pattern[str]
    error_message: str
