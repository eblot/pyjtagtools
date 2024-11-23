# Copyright (c) 2010-2024, Emmanuel Blot <emmanuel.blot@free.fr>
# All rights reserved.
#
# SPDX-License-Identifier: Apache2

"""JTAG Errors"""

class JtagError(Exception):
    """Generic JTAG error."""


class JtagStateError(JtagError):
    """JTAG state machine error."""
