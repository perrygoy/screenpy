"""
A question to retrieve an element from the page.
"""

from typing import Optional

from selenium.webdriver.remote.webelement import WebElement

from screenpy.actor import Actor
from screenpy.exceptions import BrowsingError
from screenpy.pacing import beat
from screenpy.target import Target


class Element:
    """Ask to retrieve a specific element.

    Abilities Required:
        |BrowseTheWeb|

    Examples::

        the_actor.should_see_the((Element(WELCOME_BANNER), IsVisible()))
    """

    @beat("{} inspects the {target}.")
    def answered_by(self, the_actor: Actor) -> Optional[WebElement]:
        """Direct the actor to find the element."""
        try:
            return self.target.found_by(the_actor)
        except BrowsingError:
            return None

    def __init__(self, target: Target) -> None:
        self.target = target
