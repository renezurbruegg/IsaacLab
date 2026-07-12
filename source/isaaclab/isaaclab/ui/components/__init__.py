# Copyright (c) 2022-2025, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""UI Components Package.

This package provides a collection of reusable user interface components for Isaac Lab applications.
It follows a component-based architecture where each UI element is encapsulated in its own component
class with associated configuration classes.

The package includes:

* **Base Components**: Core abstract classes that define the component interface
* **Button Component**: A simple clickable button component for triggering actions
* **Dropdown Component**: A dropdown/combobox component for selecting from predefined options
* **Empty Component**: A minimal no-op component for testing and placeholder purposes
* **List Component**: A dynamic list UI component with checkboxes and callbacks

Key Features:
- Component-based architecture with separation of configuration and implementation
- Debug visualization support with toggle callbacks
- Event-driven interaction model
- Extensible design for custom component implementations

Example Usage:
    ```python
    from isaaclab.ui.components import (
        ButtonComponent, ButtonComponentCfg,
        ListComponent, ListComponentCfg,
        DropdownComponent, DropdownComponentCfg
    )

    # Configure a button component
    def my_action():
        print("Button clicked!")

    button_cfg = ButtonComponentCfg(
        text="Execute Action",
        callback_fnc=my_action
    )
    button_component = ButtonComponent(button_cfg)

    # Configure a list component
    list_cfg = ListComponentCfg(
        entries=[
            ListComponentCfg.ListEntryCfg(name="item1", label="First Item"),
            ListComponentCfg.ListEntryCfg(name="item2", label="Second Item")
        ]
    )
    list_component = ListComponent(list_cfg)

    # Configure a dropdown component
    dropdown_cfg = DropdownComponentCfg(
        label="Select Mode",
        options=[
            DropdownComponentCfg.DropdownOptionCfg(value="mode1", label="Mode 1"),
            DropdownComponentCfg.DropdownOptionCfg(value="mode2", label="Mode 2")
        ]
    )
    dropdown_component = DropdownComponent(dropdown_cfg)
    ```
"""

from .button.button_component import ButtonComponent
from .button.button_component_cfg import ButtonComponentCfg
from .component import Component
from .component_cfg import ComponentCfg
from .dropdown.dropdown_component import DropdownComponent
from .dropdown.dropdown_component_cfg import DropdownComponentCfg
from .list.list_component import ListComponent
from .list.list_component_cfg import ListComponentCfg
