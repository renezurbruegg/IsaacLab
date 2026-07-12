# Copyright (c) 2022-2025, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

# Copyright (c) 2022-2025, The Isaac Lab Project Developers.
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Button UI Component Package.

This package provides a simple button UI component for triggering actions and callbacks.
The button component offers:

1. **Click Actions**: Execute callbacks when the button is pressed
2. **Visual States**: Support for enabled/disabled states with visual feedback
3. **Customizable Appearance**: Configurable text, tooltips, and styling
4. **Event Integration**: Seamless integration with Isaac Lab's event system

The button component is ideal for:
- Action triggers in control panels
- Command execution interfaces
- Interactive demonstrations
- User input collection

Components included:
- ButtonComponent: A clickable button that executes callbacks
- ButtonComponentCfg: Configuration for the button component

Example Usage:
    ```python
    from isaaclab.ui.components.button import ButtonComponent, ButtonComponentCfg

    def my_action():
        print("Button clicked!")

    # Configure button
    cfg = ButtonComponentCfg(
        text="Click Me",
        tooltip="This button does something",
        callback_fnc=my_action
    )

    # Create the component
    button = ButtonComponent(cfg)
    ```
"""
