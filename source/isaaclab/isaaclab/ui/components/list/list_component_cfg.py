# Copyright (c) 2022-2025, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

from collections.abc import Callable

from isaaclab.utils import configclass

from ..component_cfg import ComponentCfg
from .list_component import ListComponent


@configclass
class ListComponentCfg(ComponentCfg):

    @configclass
    class ListEntryCfg:
        """Configuration parameters for a list entry."""

        name: str = "Entry"
        label: str = "Entry"
        tooltip: str = ""
        enabled: bool = True

    """Configuration parameters for a sensor."""

    class_type: type[ListComponent] = ListComponent

    entries: list[ListEntryCfg] | None = None

    callback_fnc: Callable[[str, bool], None] | None = None
