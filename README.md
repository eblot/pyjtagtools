# PyJtagTools

![Python package](https://github.com/eblot/pyjtagtools/actions/workflows/pythonpackage.yml/badge.svg)

[![PyPI](https://img.shields.io/pypi/v/pyjtagtools.svg?maxAge=2592000)](https://pypi.org/project/pyjtagtools/)
[![Python Versions](https://img.shields.io/pyjtagtools/pyversions/pyjtagtools.svg)](https://pypi.org/project/pyjtagtools/)
[![Downloads](https://img.shields.io/pypi/dm/pyjtagtools.svg)](https://pypi.org/project/pyjtagtools/)

## Overview

PyJtagTools implements a JTAG TAP controller client.
It has been extracted from [PyFtdi][1] v0.60, as its core features are not specific to [PyFtdi][1],
and enable to support other JTAG backend, for example the Remote BitBang protocol.

## Supported host OSes

* macOS
* Linux
* FreeBSD

## License

`SPDX-License-Identifier: Apache2`

### Python support

PyFtdi requires Python 3.9+.

[1]: https://github.com/eblot/pyftdi/
