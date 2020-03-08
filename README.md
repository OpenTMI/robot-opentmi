## robot listener plugin for opentmi

This robot-framework listener listen results and upload them to OpenTMI.

## Usage

```
robot --listener robot_opentmi.plugin.PythonListener example/example.robot
```

## Usage

Install using pip:

`pip install robot-opentmi`

Running with robot:

`robot -v...`


### metadata

module utilize some special robot variable arguments.
Usage:

`robot -v <KEY>:<VALUE> ...`

**Keys:**
* OpenTMI
  * `opentmi`, server address
  * `opentmi_token`, access token

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
