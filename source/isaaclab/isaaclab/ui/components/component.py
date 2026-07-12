# Copyright (c) 2022-2025, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

# Copyright (c) 2022-2025, The Isaac Lab Project Developers.
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Base class for UI components.

This module defines the abstract base class for all UI components in Isaac Lab's user interface
framework. Components are reusable UI elements that can be configured, instantiated, and managed
through a standardized interface.

The component system provides:
- Consistent lifecycle management (initialization, visualization, cleanup)
- Debug visualization support with toggle callbacks
- Event-driven interaction model through callback functions
- Integration with Omni Kit's event system for real-time updates

All concrete UI components should inherit from the Component class and implement the required
abstract methods to ensure proper integration with the Isaac Lab UI framework.
"""

from __future__ import annotations

import weakref
from typing import TYPE_CHECKING

import omni.kit.app

from ..widgets import UiVisualizerBase

if TYPE_CHECKING:
    from .component_cfg import ComponentCfg


class Component(UiVisualizerBase):
    """Abstract base class for all UI components in Isaac Lab.

    This class provides the foundational interface and common functionality that all UI components
    should implement. It handles the lifecycle of UI components including initialization, debug
    visualization management, and event subscription.

    Key Features:
    - **Debug Visualization**: Built-in support for toggling debug visualization on/off
    - **Event Integration**: Automatic subscription to Omni Kit's post-update event stream
    - **Callback System**: Flexible callback mechanisms for user interactions
    - **Lifecycle Management**: Proper initialization and cleanup of UI resources

    Components operate through a configuration-driven approach where behavior is defined
    by passing a ComponentCfg object during initialization. This promotes reusability
    and makes components easily configurable.

    Attributes:
        cfg: The configuration object passed during initialization

    Example:
        ```python
        class MyComponent(Component):
            def __init__(self, cfg: MyComponentCfg):
                super().__init__(cfg)
                # Component-specific initialization

            def _build_ui(self) -> bool:
                # Implement UI construction logic
                return True
        ```

    Note:
        This is an abstract base class. Concrete implementations must override
        the abstract methods to provide component-specific functionality.
    """

    def __deepcopy__(self, memo):
        # prevent a new copy, return this instance instead
        return self

    def __init__(self, cfg: ComponentCfg):
        """Initialize the component instance.

        Sets up the component with the provided configuration and initializes
        internal state for debug visualization management. This includes setting
        up callback function placeholders and visualization handles.

        Args:
            cfg: The configuration parameters for the component. This should be
                an instance of ComponentCfg or a subclass containing component-specific
                configuration options.
        """
        # Store the configuration object
        self.cfg = cfg

        # Initialize callback function references
        self._debug_vis_cb_fnc = None
        self._debug_vis_toggle_fnc = None

        # Handle for debug visualization event subscription (set in set_debug_vis)
        self._debug_vis_handle = None

        self.set_debug_vis(cfg.debug_vis)

    @property
    def has_debug_vis_implementation(self) -> bool:
        """Check if this component supports debug visualization.

        Returns:
            bool: Always True for the base Component class, indicating that debug
                visualization is supported. Subclasses can override this to return
                False if they don't implement debug visualization features.
        """
        return True

    # ------------------------------------------------------------------
    # Public Operations
    # ------------------------------------------------------------------

    def set_debug_vis_callback(self, debug_vis_cb_fnc):
        """Register a callback function for debug visualization updates.

        This callback will be invoked on each frame when debug visualization is enabled,
        allowing the component to update its visual representation with current data.

        Args:
            debug_vis_cb_fnc: A callable that will be invoked with an event parameter
                on each update frame. The function signature should be:
                ``callback(event) -> None``

        Example:
            ```python
            def my_debug_callback(event):
                # Update visualization with current data
                pass

            component.set_debug_vis_callback(my_debug_callback)
            ```
        """
        self._debug_vis_cb_fnc = debug_vis_cb_fnc

    def set_debug_vis_toggle_callback(self, debug_vis_toggle_fnc):
        """Register a callback function for debug visualization state changes.

        This callback will be invoked whenever debug visualization is toggled on or off,
        allowing the component to perform setup or cleanup operations.

        Args:
            debug_vis_toggle_fnc: A callable that will be invoked with a boolean parameter
                indicating the new debug visualization state. The function signature should be:
                ``callback(enabled: bool) -> None``

        Example:
            ```python
            def my_toggle_callback(enabled: bool):
                if enabled:
                    # Setup debug visualization resources
                    pass
                else:
                    # Cleanup debug visualization resources
                    pass

            component.set_debug_vis_toggle_callback(my_toggle_callback)
            ```
        """
        self._debug_vis_toggle_fnc = debug_vis_toggle_fnc

    def set_debug_vis(self, debug_vis: bool) -> bool:
        """Enable or disable debug visualization for this component.

        This method manages the lifecycle of debug visualization, including subscribing
        to or unsubscribing from Omni Kit's update events and building the UI interface.

        Args:
            debug_vis: Whether to enable debug visualization. When True, the component
                will subscribe to update events and display debug information. When False,
                it will clean up resources and hide debug UI elements.

        Returns:
            bool: True if the debug visualization state was successfully changed,
                False if the component doesn't support debug visualization or if
                the UI failed to build.

        Note:
            This method automatically handles event subscription management and calls
            the registered toggle callback if one has been set.
        """

        # toggle debug visualization objects
        self._set_debug_vis_impl(debug_vis)
        # toggle debug visualization flag
        self._is_visualizing = debug_vis

        # toggle debug visualization handles
        if debug_vis:
            # create a subscriber for the post update event if it doesn't exist
            if self._debug_vis_handle is None:
                app_interface = omni.kit.app.get_app_interface()
                self._debug_vis_handle = app_interface.get_post_update_event_stream().create_subscription_to_pop(
                    lambda event, obj=weakref.proxy(self): obj._debug_vis_callback(event)
                )
        else:
            # remove the subscriber if it exists
            if self._debug_vis_handle is not None:
                self._debug_vis_handle.unsubscribe()
                self._debug_vis_handle = None

        return self._build_ui()

    # ------------------------------------------------------------------
    # Private Implementation
    # ------------------------------------------------------------------

    def _build_ui(self) -> bool:
        """Build the user interface for this component.

        This method should be implemented by subclasses to create and configure
        the actual UI elements for the component. It's called when the component
        needs to construct or reconstruct its visual representation.

        Returns:
            bool: True if the UI was successfully built, False otherwise.

        Note:
            This is a template method that subclasses should override to provide
            component-specific UI construction logic.
        """
        return True

    def _set_debug_vis_impl(self, debug_vis: bool) -> None:
        """Internal implementation for setting debug visualization state.

        This method handles the actual work of enabling or disabling debug visualization
        for the component. It updates the configuration and calls any registered toggle
        callback functions.

        Args:
            debug_vis: Whether to enable debug visualization for this component.
        """
        self.cfg.debug_vis = debug_vis
        if self._debug_vis_toggle_fnc is not None:
            self._debug_vis_toggle_fnc(debug_vis)

    def _debug_vis_callback(self, event):
        """Internal callback handler for debug visualization updates.

        This method is automatically called by Omni Kit's event system when debug
        visualization is enabled. It serves as a bridge between the framework's
        event system and the user-defined debug visualization callback.

        Args:
            event: The update event from Omni Kit's post-update event stream.
                Contains timing and frame information that can be used for
                animation or performance monitoring.

        Note:
            This method is called automatically and should not be invoked directly.
            Use set_debug_vis_callback() to register your own visualization logic.
        """
        if self._debug_vis_cb_fnc is not None:
            self._debug_vis_cb_fnc(event)


import contextlib

with contextlib.suppress(ImportError):
    import omni.ui


class FrameComponent(Component):

    def _set_vis_frame_impl(self, vis_frame: omni.ui.Window) -> None:
        """Sets the visualization frame.

        Args:
            vis_frame: The visualization frame.
        """
        self._vis_frame = vis_frame
        if self.cfg.debug_vis:
            self._build_ui()

    def _set_debug_vis_impl(self, debug_vis: bool) -> None:
        """Set the debug visualization implementation.

        Args:
            debug_vis: Whether to enable debug visualization.
        """
        super()._set_debug_vis_impl(debug_vis)

        if not debug_vis and hasattr(self, "_vis_frame"):
            print("Setting vis frame to invisible")
            self._vis_frame.clear()
            self._vis_frame.visible = False

    def _build_ui(self) -> bool:
        """Build the button user interface.

        Creates the Omni UI button element with the configured appearance
        and behavior.

        Returns:
            bool: True if the UI was successfully built, False if Omni UI
                is not available or if there's no visualization frame set.
        """

        if not hasattr(self, "_vis_frame"):
            return False  # No frame set for debug visualization.

        self._vis_frame.clear()
        self._vis_frame.visible = self.cfg.debug_vis

        if not self.cfg.debug_vis:
            return True

        with self._vis_frame:
            return self._populate_vis_frame()

    def _populate_vis_frame(self) -> bool:
        raise NotImplementedError("_populate_vis_frame must be implemented by subclasses")
