# Watchdock 
>#### Simple `docker management` and `monitoring` tool based on `DOCKER CLI` for developers
There are many great, multi-functinoal and beautiful GUI tools for `docker` engineers out there. As a beginner, however, I feel those are too complex for me to use in my development environment. Watchdock will give you quick overview and monitoring method of docker with `light` and `fast` UI operation. Moreover this tool will contribute to your docker study with easy understanding and learning curve at private development space.

Although I don't want you to expect more features surpassing great docker tools like [`Kubernetes`](https://kubernetes.io/) or [`Kitematic`](https://kitematic.com/) for commercial service operation, I have a goal to help devleopers can reduce their time and feel its usefulness. 

## The major objectives of this tool
1. Less typing docker commands during development
2. Prompt UI respond on development PC
3. Extended functions related to `docker management` for development effectiveness


----


## History
- Version 0.5 - 03/09/2018
![Screenshot](screenshot.png)


## Requirement
- Docker community edition for Win/Mac/Ubuntu, 18.01.x+
- Python 2.7.x
- wxPython 3.0.2.0+


## Installation & Execution

### Mac & Windows
```
pip install -r requirements.txt
python watchdock.py
```

### Ubuntu
```
sudo apt-get update
sudo apt-get install python-wxgtk3.0
python watchdock.py
```


## Current Features
- Container/Image/System Information check
- Container survival (start,stop,restart )
- Process information of each container
- Logs of each container
- Image save


## Roadmap
- Fixed Font support for all environment
- Network management
- Coloring for better readiability
- Advanced Image management
- Attaching shell
- Docker image watch in [`Vagrant`](https://www.vagrantup.com/) VMs
- Deployment management
- Universal installer for Mac, Windows and Ubuntu

