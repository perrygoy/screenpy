"""
An action to select an item from a multi-selection field or dropdown.
"""

from typing import Optional, Union

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import Select as SeleniumSelect

from screenpy.actor import Actor
from screenpy.exceptions import DeliveryError, UnableToAct
from screenpy.pacing import beat
from screenpy.target import Target


class Select:
    """Select an option from a dropdown menu.

    This is an entry point that will create the correct specific Select action
    to be used, depending on how the option needs to be selected.

    Abilities Required:
        |BrowseTheWeb|

    Examples::

        the_actor.attempts_to(
            Select.the_option_named("January").from_the(MONTH_DROPDOWN)
        )

        the_actor.attempts_to(
            Select.the_option_at_index(0).from_the(MONTH_DROPDOWN)
        )

        the_actor.attempts_to(
            Select.the_option_with_value("jan").from_the(MONTH_DROPDOWN)
        )
    """

    @staticmethod
    def the_option_named(text: str) -> "SelectByText":
        """Select the option by its text."""
        return SelectByText(text)

    @staticmethod
    def the_option_at_index(index: Union[int, str]) -> "SelectByIndex":
        """Select the option by its index. This index is 0-based."""
        return SelectByIndex(index)

    @staticmethod
    def the_option_with_value(value: str) -> "SelectByValue":
        """Select the option by its value."""
        return SelectByValue(value)


class SelectByText:
    """Select an option in a dropdown or multi-select field by its text.

    This action will probably not be used directly, rather it will be used by
    calling |Select.the_option_named|.

    Abilities Required:
        |BrowseTheWeb|
    """

    target: Optional[Target]

    def from_the(self, target: Target) -> "SelectByText":
        """
        Target the dropdown or multi-select field to select the option from.
        """
        self.target = target
        return self

    from_ = from_the

    @beat('{} selects the option "{text}" from the {target}.')
    def perform_as(self, the_actor: Actor) -> None:
        """
        Direct the actor to select the option from the targeted dropdown or
        multiselect field by its text.
        """
        if self.target is None:
            raise UnableToAct(
                "Target was not provided for SelectByText. Provide a target using the "
                ".from_() or .from_the() methods."
            )

        element = self.target.found_by(the_actor)
        select = SeleniumSelect(element)
        try:
            select.select_by_visible_text(self.text)
        except WebDriverException as e:
            msg = (
                "Encountered an issue while attempting to select the option with text "
                f"'{self.text}' from {self.target}: {e.__class__.__name__}"
            )
            raise DeliveryError(msg).with_traceback(e.__traceback__)

    def __init__(self, text: str, target: Optional[Target] = None) -> None:
        self.target = target
        self.text = text


class SelectByIndex:
    """Select an option in a dropdown or multi-select field by its index.

    This action will probably not be used directly, rather it will be used by
    calling |Select.the_option_at_index|.

    Abilities Required:
        |BrowseTheWeb|
    """

    target: Optional[Target]

    def from_the(self, target: Target) -> "SelectByIndex":
        """
        Target the dropdown or multi-select field to select the option from.
        """
        self.target = target
        return self

    from_ = from_the

    @beat("{} selects the option at index {index} from the {target}.")
    def perform_as(self, the_actor: Actor) -> None:
        """
        Direct the actor to select the option from the targeted dropdown or
        multiselect field using its index.
        """
        if self.target is None:
            raise UnableToAct(
                "Target was not provided for SelectByIndex. Provide a target using the "
                ".from_() or .from_the() methods."
            )

        element = self.target.found_by(the_actor)
        select = SeleniumSelect(element)
        try:
            select.select_by_index(self.index)
        except WebDriverException as e:
            msg = (
                "Encountered an issue while attempting to select the option at index "
                f"{self.index} from {self.target}: {e.__class__.__name__}"
            )
            raise DeliveryError(msg).with_traceback(e.__traceback__)

    def __init__(self, index: Union[int, str], target: Optional[Target] = None) -> None:
        self.target = target
        self.index = str(index)


class SelectByValue:
    """Select an option in a dropdown or multi-select field by its value.

    This action will probably not be used directly, rather it will be used by
    calling |Select.the_option_with_value|.

    Abilities Required:
        |BrowseTheWeb|
    """

    target: Optional[Target]

    def from_the(self, target: Target) -> "SelectByValue":
        """
        Target the dropdown or multi-select field to select the option from.
        """
        self.target = target
        return self

    from_ = from_the

    @beat('{} selects the option with value "{value}" from the {target}.')
    def perform_as(self, the_actor: Actor) -> None:
        """
        Direct the actor to select the option from the targeted dropdown or
        multiselect field by its value.
        """
        if self.target is None:
            raise UnableToAct(
                "Target was not provided for SelectByValue. Provide a target using the "
                ".from_() or .from_the() methods."
            )

        element = self.target.found_by(the_actor)
        select = SeleniumSelect(element)
        try:
            select.select_by_value(self.value)
        except WebDriverException as e:
            msg = (
                "Encountered an issue while attempting to select the option with value "
                f"{self.value} from {self.target}: {e.__class__.__name__}"
            )
            raise DeliveryError(msg).with_traceback(e.__traceback__)

    def __init__(self, value: Union[int, str], target: Optional[Target] = None) -> None:
        self.target = target
        self.value = str(value)
