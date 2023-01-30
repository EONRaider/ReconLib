"""
ReconLib: A collection of modules and helpers for active and passive
reconnaissance of remote hosts.

    Copyright (C) 2023 EONRaider @ keybase.io/eonraider

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see
    <https://github.com/EONRaider/ReconLib/blob/master/LICENSE>.
"""


class ReconLibException(Exception):
    def __init__(self, message: str, code: int):
        self.message = message
        self.code = code


class InvalidTargetError(ReconLibException):
    def __init__(self, message: str, code: int = 1):
        super().__init__(f"{self.__class__.__name__}: {message}", code)


class APIKeyError(ReconLibException):
    def __init__(self, message: str, code: int = 1):
        super().__init__(f"{self.__class__.__name__}: {message}", code)
