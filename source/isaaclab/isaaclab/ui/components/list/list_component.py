# Copyright (c) 2022-2025, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""UI List Component for Isaac Lab.

This class implements a user interface list component for displaying and interacting with a list of entries
in the Isaac Lab UI framework. It provides methods for managing list entries, handling callbacks, and rendering
the list in the UI. Intended to be used as part of the UI component system.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..component import FrameComponent

if TYPE_CHECKING:
    from .list_component_cfg import ListComponentCfg

import contextlib
from collections.abc import Callable

with contextlib.suppress(ImportError):
    import omni.ui


class ListComponent(FrameComponent):

    def __init__(self, cfg: ListComponentCfg):
        super().__init__(cfg)

        self._vis_terms: dict[str, ListComponentCfg.ListEntryCfg] = {}
        self._callbacks: list[Callable[[str, bool], None]] = [cfg.callback_fnc] if cfg.callback_fnc else []
        if cfg.entries is not None:
            for entry in cfg.entries:
                self._vis_terms[entry.name] = entry

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def register_callbacks(self, callback):
        self._callbacks.append(callback)

    # ------------------------------------------------------------------
    # Private Implementation
    # ------------------------------------------------------------------

    def _populate_vis_frame(self):
        import isaacsim
        from omni.kit.window.extensions import SimpleCheckBox

        self._frames = []

        with self._vis_frame:
            with omni.ui.VStack():
                for name, entry in self._vis_terms.items():
                    frame = SimpleCheckBox(
                        model=omni.ui.SimpleBoolModel(),
                        enabled=True,
                        checked=entry.enabled,
                        text=name,
                        on_checked_fn=lambda value, e=name: self._on_checked(e, value),
                    )
                    isaacsim.gui.components.ui_utils.add_line_rect_flourish()
                    self._frames.append(frame)

        self._vis_frame.visible = True

    def _debug_vis_callback(self, event):
        """Callback function for the debug visualization.

        Args:
            event: The event that triggered the callback.
        """
        for name, value in self._vis_terms.items():
            for cb in self._callbacks:
                cb(name, value.enabled)

    def _on_checked(self, name, value):
        self._vis_terms[name].enabled = value
