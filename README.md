## robot listener plugin for opentmi

This robot-framework listener listen results and upload them to OpenTMI.

## Usage

Install using pip:

`pip install robot-opentmi`

Running with robot:

```
robot --listener robot_opentmi.plugin.PythonListener:<host>:<token>:<port> example/example.robot
```

Where:
* `<host>` is OpenTMI uri
* `<port>` is OpenTMI port
* `<token>` is OpenTMI access token


### metadata

module utilize some special robot variable arguments.
Usage:

`robot -v <KEY>:<VALUE> ...`

**Keys:**
* Device Under Test:
  * `DUT_SERIAL_NUMBER`
  * `DUT_VERSION`
  * `DUT_VENDOR`
  * `DUT_MODEL`
  * `DUT_PROVIDER`

* Software Under Test:
  * `SUT_COMPONENT`
  * `SUT_FEATURE`
  * `SUT_COMMIT_ID`
