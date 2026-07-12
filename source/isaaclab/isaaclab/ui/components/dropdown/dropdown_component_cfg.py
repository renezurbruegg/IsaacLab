# Copyright (c) 2022-2025, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

# Copyright (c) 2022-2025, The Isaac Lab Project Developers.
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Configuration class for the dropdown UI component.

This module defines the configuration dataclasses for DropdownComponent, providing
flexible options for creating dropdown/combobox UI elements with customizable
options, labels, and selection callbacks.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from isaaclab.utils import configclass

from ..component_cfg import ComponentCfg
from .dropdown_component import DropdownComponent


@configclass
class DropdownComponentCfg(ComponentCfg):
    """Configuration parameters for the dropdown UI component.

    This class extends ComponentCfg to provide dropdown-specific configuration options
    including the list of selectable options, labels, default values, and callbacks.

    The dropdown component supports dynamic option lists and can trigger callbacks
    when the selection changes, making it suitable for interactive UI elements.

    Attributes:
        class_type: Set to DropdownComponent for instantiation.
        label: Display label shown above or beside the dropdown.
        options: List of available options that can be selected.
        default_value: The initially selected option value.
        tooltip: Optional tooltip text displayed on hover.
        enabled: Whether the dropdown is interactive.
        callback_fnc: Function called when selection changes.

    Example:
        ```python
        def on_selection_changed(value):
            print(f"Selected: {value}")

        cfg = DropdownComponentCfg(
            label="Render Mode",
            options=[
                DropdownComponentCfg.DropdownOptionCfg(
                    value="wireframe",
                    label="Wireframe"
                ),
                DropdownComponentCfg.DropdownOptionCfg(
                    value="solid",
                    label="Solid"
                )
            ],
            default_value="solid",
            callback_fnc=on_selection_changed
        )
        ```
    """

    @configclass
    class DropdownOptionCfg:
        """Configuration for individual dropdown options.

        Defines the properties of a single option that can be selected
        from the dropdown list.

        Attributes:
            value: The internal value associated with this option. This is what
                gets passed to callback functions and stored as the selection.
            label: The display text shown to users for this option.
            tooltip: Optional tooltip text shown when hovering over this option.
            enabled: Whether this option can be selected.
        """

        value: Any = None
        """The internal value for this option (can be any type)."""

        label: str = ""
        """Display text shown to users."""

        tooltip: str = ""
        """Optional tooltip text for this option."""

    class_type: type[DropdownComponent] = DropdownComponent

    options: list[DropdownOptionCfg] = None
    """List of available options in the dropdown."""

    default_value: Any = None
    """The initially selected value (should match one of the option values)."""

    tooltip: str = ""
    """Optional tooltip text for the entire dropdown component."""

    callback_fnc: Callable[[Any], None] | None = None
    """Function called when selection changes. Receives the new value as parameter."""
