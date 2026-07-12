# Copyright (c) 2022-2025, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

# Copyright (c) 2022-2025, The Isaac Lab Project Developers.
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Dropdown UI Component Package.

This package provides a dropdown/combobox UI component for selecting from a list of options.
The dropdown component offers:

1. **Single Selection**: Users can select one option from a predefined list
2. **Dynamic Options**: Options can be updated programmatically at runtime
3. **Callbacks**: Custom functions triggered when selections change
4. **Flexible Configuration**: Support for labels, tooltips, and default values

The dropdown component is ideal for:
- Settings and configuration panels
- Mode selection interfaces
- Dynamic option lists based on context
- Form-like UI elements

Components included:
- DropdownComponent: A dropdown/combobox component for option selection
- DropdownComponentCfg: Configuration for the dropdown component

Example Usage:
    ```python
    from isaaclab.ui.components.dropdown import DropdownComponent, DropdownComponentCfg

    # Configure dropdown options
    cfg = DropdownComponentCfg(
        label="Select Mode",
        options=[
            DropdownComponentCfg.DropdownOptionCfg(value="mode1", label="Mode 1"),
            DropdownComponentCfg.DropdownOptionCfg(value="mode2", label="Mode 2")
        ],
        default_value="mode1"
    )

    # Create the component
    dropdown = DropdownComponent(cfg)
    ```
"""
