## robot listener plugin for opentmi


[![CircleCI](https://circleci.com/gh/OpenTMI/robot-opentmi/tree/master.svg?style=svg)](https://circleci.com/gh/OpenTMI/robot-opentmi/tree/master)
[![PyPI version](https://badge.fury.io/py/robot-opentmi.svg)](https://badge.fury.io/py/robot-opentmi)
<!-- [![Coverage Status](https://coveralls.io/repos/github/OpenTMI/pytest-opentmi/badge.svg)](https://coveralls.io/github/OpenTMI/pytest-opentmi) -->

This robot-framework listener listen results and upload them to OpenTMI.

## Usage

Install using pip:

`pip install robot-opentmi`

Running with robot:

```
robot --listener robot_opentmi.plugin.PythonListener:<host>:<token>:<port>:<store_logs> example/example.robot
```

Where:
* `<host>` is OpenTMI uri (required)
* `<token>` is OpenTMI access token (required)
* `<port>` is OpenTMI port (default: 80, optional)
* `<store_logs>` store logs to OpenTMI (default: False, optional)


### metadata

module utilize some special robot metadata.
Usage:

`robot -M <KEY>:<VALUE> ...`

**Keys:**
* Device Under Test:
  * `DUT_SERIAL_NUMBER`
  * `DUT_TYPE`
  * `DUT_VERSION`
  * `DUT_VENDOR`
  * `DUT_MODEL`
  * `DUT_PROVIDER`

* Software Under Test:
  * `SUT_COMPONENT`
  * `SUT_FEATURE`
  * `SUT_COMMIT_ID`
  * `SUT_BRANCH`
