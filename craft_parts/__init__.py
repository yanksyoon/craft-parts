# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4 -*-
#
# Copyright 2021-2023 Canonical Ltd.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License version 3 as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Craft a project from several parts."""

__version__ = "2.1.3"

from . import plugins
from .actions import Action, ActionProperties, ActionType
from .dirs import ProjectDirs
from .errors import PartsError
from .executor import expand_environment
from .features import Features
from .infos import PartInfo, ProjectInfo, StepInfo
from .lifecycle_manager import LifecycleManager
from .parts import Part, part_has_overlay, validate_part
from .steps import Step

__all__ = [
    "Features",
    "Action",
    "ActionProperties",
    "ActionType",
    "ProjectDirs",
    "PartsError",
    "ProjectInfo",
    "PartInfo",
    "StepInfo",
    "LifecycleManager",
    "Part",
    "Step",
    "plugins",
    "expand_environment",
    "validate_part",
    "part_has_overlay",
]
