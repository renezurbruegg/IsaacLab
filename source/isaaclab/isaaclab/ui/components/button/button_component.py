# Copyright (c) 2022-2025, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

# Copyright (c) 2022-2025, The Isaac Lab Project Developers.
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Button UI component implementation.

This module provides a simple button component that allows users to trigger
actions and callbacks through mouse clicks. The component integrates with
Omni UI to create interactive buttons with customizable appearance and behavior.
"""

from __future__ import annotations

import contextlib
import weakref
from typing import TYPE_CHECKING

from ..component import FrameComponent

if TYPE_CHECKING:
    from .button_component_cfg import ButtonComponentCfg

with contextlib.suppress(ImportError):
    import omni.ui


class ButtonComponent(FrameComponent):
    """A simple button UI component for triggering actions.

    This component creates a clickable button that can execute callback functions
    when pressed. It supports customizable text, tooltips, enabled/disabled states,
    and integrates seamlessly with the Isaac Lab UI framework.

    Key Features:
    - **Click Actions**: Execute callbacks on button press
    - **Visual States**: Support for enabled/disabled visual feedback
    - **Customizable Appearance**: Text, size, and tooltip configuration
    - **Event Integration**: Proper integration with Omni UI event system

    The button maintains internal state for its enabled/disabled condition and
    provides methods for programmatic state changes.

    Example:
        ```python
        def my_callback():
            print("Button clicked!")

        cfg = ButtonComponentCfg(
            text="Start Process",
            tooltip="Click to start the background process",
            callback_fnc=my_callback,
            enabled=True
        )

        button = ButtonComponent(cfg)
        ```

    Note:
        The component requires Omni UI to be available for proper functionality.
        It will gracefully handle cases where Omni UI is not imported.
    """

    cfg: ButtonComponentCfg

    def __init__(self, cfg: ButtonComponentCfg):
        """Initialize the button component.

        Sets up the button with the provided configuration, including text,
        callback function, and initial state.

        Args:
            cfg: Configuration object containing button text, callback,
                appearance settings, and behavioral parameters.
        """
        super().__init__(cfg)

        # UI reference (set when UI is built)
        self._button_widget = None

        # Store callback functions
        self._callbacks: list = []
        if self.cfg.callback_fnc is not None:
            self._callbacks.append(self.cfg.callback_fnc)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def add_callback(self, callback_fnc) -> None:
        """Add a callback function to be executed when the button is clicked.

        Args:
            callback_fnc: A callable with no parameters that will be executed
                when the button is pressed.
        """
        if callback_fnc not in self._callbacks:
            self._callbacks.append(callback_fnc)

    # ------------------------------------------------------------------
    # Private Implementation
    # ------------------------------------------------------------------

    def _populate_vis_frame(self):
        """Build the button user interface.

        Creates the Omni UI button element with the configured appearance
        and behavior.

        Returns:
            bool: True if the UI was successfully built, False if Omni UI
                is not available or if there's no visualization frame set.
        """
        with self._vis_frame:
            button_kwargs = {
                "text": self.cfg.text,
                "clicked_fn": lambda obj=weakref.proxy(self): obj._on_button_clicked(),
            }

            # Add tooltip if specified
            if self.cfg.tooltip:
                button_kwargs["tooltip"] = self.cfg.tooltip

            self._button_widget = omni.ui.Button(**button_kwargs)

        return True

    def _on_button_clicked(self) -> None:
        """Handle button click events.

        Called when the user clicks the button. Executes all registered
        callback functions.
        """

        for callback in self._callbacks:
            try:
                callback()
            except Exception as e:
                # Log the error but continue executing other callbacks
                print(f"Error in button callback: {e}")

    def _set_vis_frame_impl(self, vis_frame) -> None:
        """Set the visualization frame for this component.

        Args:
            vis_frame: The Omni UI frame to use for rendering this component.
        """
        self._vis_frame = vis_frame
        if self.cfg.debug_vis:
            self._build_ui()
