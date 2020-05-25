# TrackyPy
A simple script that will create a task.csv file for the directory you're working in. The script allows you to view, append, and mark done ypur notes in your working directory. The script is a command line application.

# Getting Started
Upon adding the "track" function from the "track.sh" file to your .bash_profile, you will be able to create .tack.csv file in any directory you want by simply navigating to it. Once you have reached the directorPy that you wish to have a .task.csv file simply run

```
    track -a "TASK TO APPEND"
```

# Command line flags
```
    positional arguments:
    dir                   add task

    optional arguments:
    -h, --help            show this help message and exit
    -a TASK [TASK ...], --add TASK [TASK ...]
                            add task
    -l, --list            list all tasks
    -ld, --done           list all done tasks
    -lnd, --notdone       list all not done tasks
    -co TASKD, --checkout TASKD
```

# Support
TrackPy currently runs only on MacOS

## Authors
* **George Hanna** - *Initial work* - [GJHanna](https://github.com/GJHanna)

## License
This project is licensed under the Apache 2.0 - see the [LICENSE.md](LICENSE.md) file for details
