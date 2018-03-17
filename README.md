# Watchdock 
>#### Simple `docker management` and `monitoring` tool based on `DOCKER CLI` for developers

[![Build Status](https://travis-ci.org/gnoopy/watchdock.svg?branch=master)](https://travis-ci.org/gnoopy/watchdock)
[![Test Coverage](https://api.codeclimate.com/v1/badges/a4a236451d5f7b0f5968/test_coverage)](https://codeclimate.com/github/gnoopy/watchdock/test_coverage)
[![GitHub release](https://img.shields.io/badge/release-v0.7.6-green.svg)](https://github.com/gnoopy/watchdock/releases/tag/v0.7.6)

----

There are many great, multi-functinoal and beautiful GUI tools for `docker` engineers out there. As a beginner, however, I feel those are too complex for me to use in my development environment. Watchdock will give you quick overview and monitoring method of docker with `light` and `fast` UI operation. Moreover this tool will contribute to your docker study with easy understanding and learning curve at private development space.

Although I don't want you to expect more features surpassing great docker tools like [`Kubernetes`](https://kubernetes.io/) or [`Kitematic`](https://kitematic.com/) for commercial service operation, I have a goal to help devleopers can reduce their time and feel its usefulness. 

## The major objectives of this tool
1. Less typing docker commands during development
2. Prompt UI respond on development PC
3. Extended functions related to `docker management` for development effectiveness
 

----


## History

- v0.7.6   - 03/17/2018 - SSH for double clicked container, Automated pytest and coverage test
- rel-v0.7 - 03/12/2018 - Docker image delete 
- rel-v0.6 - 03/10/2018 - Vagrant docker information consolidation feature
- Version 0.5   - 03/09/2018
![Screenshot](screenshot.png)


## Requirement
- Docker community edition for Win/Mac/Ubuntu, 18.01.x+
- Python 2.7.x
- wxPython 3.0.2.0+


## Installation & Execution

### Mac 
```
brew install wxmac wxpython
pip install -r requirements.txt
python watchdock/run.py

```


### Windows
```
pip install -r requirements.txt
python watchdock/run.py
```

### Ubuntu
```
pip install -U -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-16.04 wxPython
python watchdock/run.py
```

Installation script like below would be helpful if the installation above does not work properly 

```
# Set up and update package repos
add-apt-repository ppa:deadsnakes/ppa
apt-get update

# Install necessary development tools, libs, etc.
apt-get install -y build-essential dpkg-dev
apt-get install -y aptitude

apt-get install -y libgtk2.0-dev libgtk-3-dev
apt-get install -y libjpeg-dev libtiff-dev \
	libsdl1.2-dev libgstreamer-plugins-base0.10-dev \
	libgstreamer-plugins-base1.0-dev \
	libnotify-dev freeglut3 freeglut3-dev libsm-dev \
	libwebkitgtk-dev libwebkitgtk-3.0-dev libwebkit2gtk-4.0-dev \
	libxtst-dev
```


## Current Features
- SSH to double clicked container for Windows, Mac and Ubuntu
- Container/Image/System Information check
- Container survival (start,stop,restart )
- Process information of each container
- Logs of each container
- Image save
- Docker image watch in [`Vagrant`](https://www.vagrantup.com/) VMs
- Fixed Font support for all environment


## Roadmap
- Container delete
- Attaching management tools (eg. sql query tool, web browser etc.)
- Volume manaement
- Network management
- Advanced Image management
- Deployment management
- Universal installer for Mac, Windows and Ubuntu
- Coloring for better readiability

