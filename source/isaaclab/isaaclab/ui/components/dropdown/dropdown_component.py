# Copyright (c) 2022-2025, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause


"""Dropdown UI component implementation.

This module provides a dropdown component that allows users to select
from a list of predefined options. The component integrates with Omni UI
to create interactive dropdown menus with customizable options and callbacks.
"""

from __future__ import annotations

import contextlib
import weakref
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from ..component import FrameComponent

if TYPE_CHECKING:
    from .dropdown_component_cfg import DropdownComponentCfg

# Optional UI imports
with contextlib.suppress(ImportError):
    import omni.ui  # noqa: F401
with contextlib.suppress(ImportError):
    # Isaac Lab convenience wrapper around an omni.ui dropdown
    from isaacsim.gui.components.element_wrappers import DropDown  # type: ignore[attr-defined]


class DropdownComponent(FrameComponent):
    """A dropdown UI component for option selection.

    Key Features:
    - Dynamic options (runtime updates)
    - Selection callbacks
    - Omni UI styling integration
    - State management (value-based)
    - Tooltips and enabled/disabled state
    """

    cfg: DropdownComponentCfg

    def __init__(self, cfg: DropdownComponentCfg):
        super().__init__(cfg)

        # Option bookkeeping
        self._options: dict[Any, DropdownComponentCfg.DropdownOptionCfg] = {}
        self._option_labels: list[str] = []
        self._option_values: list[Any] = []
        self._label_to_value: dict[str, Any] = {}
        self._callbacks = []

        # UI refs
        self._dropdown_widget = None  # DropDown wrapper instance
        self._current_selection = self.cfg.default_value  # stores *value* (not label)

        # Init options & default
        self._update_options_from_config()

        if self.cfg.callback_fnc is not None:
            self._callbacks.append(self.cfg.callback_fnc)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def add_callback(self, callback_fnc: Callable[[str], None]):
        """Add a callback function to be called on selection change."""
        if callback_fnc not in self._callbacks:
            self._callbacks.append(callback_fnc)

    # ------------------------------------------------------------------
    # Private Implementation
    # ------------------------------------------------------------------

    def _update_options_from_config(self):
        """Rebuild internal label/value maps from cfg."""
        self._options.clear()
        self._option_labels.clear()
        self._option_values.clear()
        self._label_to_value.clear()

        for option_cfg in self.cfg.options:
            self._options[option_cfg.value] = option_cfg
            self._option_labels.append(option_cfg.label)
            self._option_values.append(option_cfg.value)
            self._label_to_value[option_cfg.label] = option_cfg.value

    def _populate_vis_frame(self):
        """Build the dropdown UI using the DropDown wrapper."""

        # Populate function returns display labels
        def _populate_fn():
            return list(self._option_labels)

        # Selection callback receives a label from DropDown; convert to value
        def _on_selection_fn(selected_label: str, obj=weakref.proxy(self)):
            try:
                value = obj._label_to_value.get(selected_label)
                if value is None:
                    return
                obj._current_selection = value
            except ReferenceError:
                # widget destroyed
                pass

        with self._vis_frame:
            with omni.ui.VStack(spacing=4):
                # Create DropDown wrapper
                self._dropdown_widget = DropDown(
                    "",
                    tooltip=self.cfg.tooltip or "Select an option",
                    populate_fn=_populate_fn,
                    on_selection_fn=_on_selection_fn,
                    keep_old_selections=True,  # Preserve selection if options change
                )

                self._dropdown_widget.enabled = True
                # Build items & set selection
                current_selection = self._current_selection
                # somehow "selection" gets lost when calling repopulate even if keep_old_selections=True.
                self._dropdown_widget.repopulate()

                if current_selection in self._option_labels:
                    self._dropdown_widget.set_selection_by_index(self._option_labels.index(current_selection))

        return True

    def _set_vis_frame_impl(self, vis_frame) -> None:
        """Set the visualization frame for this component."""
        self._vis_frame = vis_frame
        if self.cfg.debug_vis:
            self._build_ui()

    def _debug_vis_callback(self, event):
        """Callback function for the debug visualization.

        Args:
            event: The event that triggered the callback.
        """
        for cb in self._callbacks:
            cb(self._current_selection)
