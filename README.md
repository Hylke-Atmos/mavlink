[![Build Status](https://travis-ci.org/ArduPilot/pymavlink.svg?branch=master)](https://travis-ci.org/ArduPilot/pymavlink)
# Pymavlink
This is a python implementation of the MAVLink protocol.
It includes a source code generator (generator/mavgen.py) to create MAVLink protocol implementations for other programming languages as well.
Also contains tools for analizing flight logs.

# Documentation

Please see http://ardupilot.org/dev/docs/mavlink-commands.html for mavlink command reference.

For realtime discussion please see the pymavlink [gitter channel](https://gitter.im/ArduPilot/pymavlink)

Examples can be found [in the repository](examples/) or in the [ArduSub book](https://www.ardusub.com/developers/pymavlink.html)


# Installation 

Pymavlink supports both python2 and python3.

The following instructions assume you are using Python 2 and a Debian-based (like Ubuntu) installation.

## Dependencies

Pymavlink has several dependencies :

    - [future](http://python-future.org/) : for python 2 and python 3 interoperability 
    - [lxml](http://lxml.de/installation.html) : for checking and parsing xml file 
    - python-dev : for mavnative
    - a C compiler : for mavnative

Optional :

    - numpy : for FFT
    - pytest : for tests

### On linux

lxml has some additional dependencies that can be installed with your package manager (here with `apt-get`) :

```bash
sudo apt-get install gcc python-dev libxml2-dev libxslt-dev
```

Optional for FFT scripts and tests:

```bash
sudo apt-get install python-numpy python-pytest
```

Using pip you can install the required dependencies for pymavlink :

```bash
sudo pip2 install -U future lxml
```

The -U parameter allows updating future and lxml version if it is already installed.

### On Windows

Use pip to install future as for linux.
Lxml can be installed with a windows installer from here : https://pypi.org/project/lxml


## Installation

### For users

It is recommended to install pymavlink from PyPi with pip, that way dependencies should be auto install by pip.

```bash
sudo pip2 install -U pymavlink
```

The -U parameter allow to update pymavlink version if it is already installed.

#### Mavnative

By default, pymavlink will try to compile and install mavnative which is a C extension for parsing mavlink. Mavnative only supports mavlink1.
To skip mavnative installation and reduce dependencies like `gcc` and `python-dev`, you can pass `DISABLE_MAVNATIVE=True` environment variable to the installation command:

```bash
sudo DISABLE_MAVNATIVE=True pip2 install -U pymavlink
```

### For developers

From the pymavlink directory, you can use :

```bash
sudo MDEF=PATH_TO_message_definitions pip2 install . -v
```

Since pip installation is executed from /tmp, it is necessary to point to the directory containing message definitions with MDEF. MDEF should not be set to any particular message version directory but the parent folder instead. If you have cloned from mavlink/mavlink then this is ```/mavlink/message_definitions``` . Using pip should auto install dependencies and allow you to keep them up-to-date. 

Or:

```bash
sudo python2 setup.py install
```


# License
---------

pymavlink is released under the GNU Lesser General Public License v3 or later.

The source code generated by generator/mavgen.py is available under the permissive MIT License.

