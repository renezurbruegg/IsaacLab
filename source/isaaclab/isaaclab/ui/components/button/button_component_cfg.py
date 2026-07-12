# Copyright (c) 2022-2025, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

# Copyright (c) 2022-2025, The Isaac Lab Project Developers.
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Configuration class for the button UI component.

This module defines the configuration dataclass for ButtonComponent, providing
options for creating interactive button elements with customizable text,
appearance, and click callbacks.
"""

from __future__ import annotations

from collections.abc import Callable

from isaaclab.utils import configclass

from ..component_cfg import ComponentCfg
from .button_component import ButtonComponent


@configclass
class ButtonComponentCfg(ComponentCfg):
    """Configuration parameters for the button UI component.

    This class extends ComponentCfg to provide button-specific configuration options
    including display text, styling, state management, and click callbacks.

    The button component supports customizable appearance and can trigger callbacks
    when clicked, making it suitable for action-oriented UI elements.

    Attributes:
        class_type: Set to ButtonComponent for instantiation.
        text: The text displayed on the button.
        tooltip: Optional tooltip text displayed on hover.
        enabled: Whether the button is clickable.
        callback_fnc: Function called when the button is clicked.
        width: Optional fixed width for the button (None for auto-sizing).
        height: Optional fixed height for the button (None for auto-sizing).

    Example:
        ```python
        def handle_click():
            print("Button was clicked!")

        cfg = ButtonComponentCfg(
            text="Execute Action",
            tooltip="Click to execute the action",
            callback_fnc=handle_click,
            enabled=True,
            width=120
        )
        ```
    """

    class_type: type[ButtonComponent] = ButtonComponent

    text: str = "Button"
    """The text displayed on the button."""

    tooltip: str = ""
    """Optional tooltip text shown when hovering over the button."""

    callback_fnc: Callable[[], None] | None = None
    """Function called when the button is clicked. Takes no parameters."""
