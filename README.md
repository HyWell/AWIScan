# AWIScan 0.0.0.1

AWIScan(All web information scan) is a fast information gathering tool for pentesters.

# Change Log

- [2019-10-23]
  - Dev release

## Dependencies

```
Python3.7
Nmap
aiodns
aiohttp
python-libnmap
```

## Installation

```
git clone https://github.com/HyWell/AWIScan.git
cd AWIScan
python3 -m pip install -r requirement.txt
```

## Usage

```
Usage: AWIScan.py [-h] [-i IP | -f FILE] [-l {1,2,3}]

            python AWIScan.py -i 10.10.10.10 -l 1
            python AWIScan.py -f target.com -l 1

Options arguments:
  -h, --help            show this help message and exit
  -i IP, --ip IP        scan a target or network(e.g. target.com
                        ,192.168.1.1[/24], 192.168.1.1-192.168.1.100)
  -f FILE, --file FILE  load target from targetFile (e.g. target.txt)
  -l {1,2,3}, --level {1,2,3}
                        This option is used to provide the scan level.
```

## Features

- Fast Async
- Support port scan、dir scan、subdomain scan
  - Dir scan
    - Random user-agent
    - Support proxy(Default:Close)
  - Subdomain scan
    - Customize DNS Server 

# Setting

Most configurations are set by lib/core/settings

# Tips

- Please use sudo or set SUDO_PASSWORD in lib/core/setting.py
- Result save output/result/{end_time}.txt