# vim: set fileencoding=utf-8
"""
pythoneda/shared/base_object.py

This script defines the BaseObject class.

Copyright (C) 2023-today rydnr's pythoneda-shared-pythonlang/domain

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import inspect
from . import (
    full_class_name,
    has_class_method,
    has_method,
    has_one_param_constructor,
    simplify_class_name,
)
from .logging_port import LoggingPort
from .logging_port_fallback import LoggingPortFallback
import re
from typing import Dict, Type


class BaseObject:
    """
    Ancestor of all PythonEDA classes.

    Class name: BaseObject

    Responsibilities:
        - Define common behavior for all PythonEDA classes.

    Collaborators:
        - None
    """

    _logging_port = None

    @classmethod
    def class_name(cls, target: Type = None) -> str:
        """
        Retrieves the class name of given class.
        :param target: The class. If omitted, this very class.
        :type target: Class
        :return: The key.
        :rtype: str
        """
        return full_class_name(target).split(".")[-1]

    @classmethod
    def full_class_name(cls) -> str:
        """
        Retrieves the full class name of given class.
        :return: The key.
        :rtype: str
        """
        return full_class_name(cls)

    @classmethod
    def logger(cls, category: str = None):
        """
        Retrieves the logger instance.
        :param category: The logging category.
        :type category: str
        :return: Such instance.
        :rtype: Any
        """
        temporary = False
        port = cls._logging_port
        if port is None:
            temporary = True
            from .ports import Ports

            ports = Ports.instance(False)
            if ports is not None:
                port = ports.resolve_first(LoggingPort)
        if port is None and temporary:
            port = LoggingPortFallback("info")

        aux = category
        if aux is None:
            aux = simplify_class_name(full_class_name(cls))

        if not temporary:
            cls._logging_port = port

        return port.logger(aux)


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
