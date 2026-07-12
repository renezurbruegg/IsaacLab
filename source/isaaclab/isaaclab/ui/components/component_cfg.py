# Copyright (c) 2022-2025, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Configuration class for UI components.

This module defines the base configuration dataclass that all UI components should use.
It provides common configuration parameters and establishes the pattern for component
configuration in Isaac Lab's UI framework.
"""

from isaaclab.utils import configclass

from .component import Component


@configclass
class ComponentCfg:
    """Base configuration parameters for UI components.

    This class serves as the foundation for all UI component configurations in Isaac Lab.
    It defines common parameters that every component should support, such as the component
    class type and debug visualization settings.

    The configuration follows Isaac Lab's standard configuration pattern using the
    `@configclass` decorator, which provides automatic validation and type checking.

    Attributes:
        class_type: The associated component class that will be instantiated from this config.
            This must be a subclass of :class:`Component` and cannot be left undefined (MISSING).
        debug_vis: Whether to enable debug visualization for this component. When enabled,
            the component may display additional visual elements, logging, or debugging
            information. Defaults to False for performance reasons.

    Example:
        ```python
        @configclass
        class MyComponentCfg(ComponentCfg):
            class_type: type[MyComponent] = MyComponent

            # Add component-specific configuration parameters
            my_param: str = "default_value"
        ```

    Note:
        All UI component configuration classes should inherit from this base class to
        ensure consistency across the framework and enable proper type checking.
    """

    class_type: type[Component] = Component
    """The associated component class.

    This should be a subclass of :class:`Component` that implements the specific
    functionality for this component type. The class will be instantiated using
    this configuration object.

    This field is required and must be set in derived configuration classes.
    """

    debug_vis: bool = False
    """Whether to enable debug visualization for the component.

    When set to True, the component may display additional debugging information,
    visual overlays, or logging output. This is useful during development and
    troubleshooting but should typically be disabled in production for performance
    reasons.

    Defaults to False.
    """
