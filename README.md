# py2so
>py2so is a toolkit to compiling your python project into dynamic link library files to hide the source code.

## Start

### Usage of py2so

```angular2
python py2so.py -h

Usage: py2so.py [options]
Options:
  -h, --help            show this help message and exit
  -l LANGUAGE, --language=LANGUAGE
                        the python version, python2 or python3, default 2
  -f FILE, --file=FILE  the local path of a file to compile
```

### Examples

- Compile a module into a binary file

  ```
  python3 py2so.py -f xxxx/test.py
  ```

- Compile a package or project into dynamic link library files

  first, you should put this script into the root directory of that project

  ```
  python3 py2so.py
  ```
  For example, there is a python project that needs to be compiled. Put the `py2so.py` script in the root directory of the project. And now the directory structure is as follows.
```angular2
.
├── README.md
├── data
│   └── conf
│       └── conf.ini
├── py2so.py         
├── src
│   ├── __init__.py
│   ├── classifier
│   │   ├── __init__.py
│   │   ├── textcnn
│   │   │   ├── __init__.py
│   │   │   ├── evaluate.py
│   │   │   ├── infer.py
│   │   │   ├── preprocess.py
│   │   │   ├── textcnn.py
│   │   │   └── train.py
│   │   └── train.py
│   ├── utils
│   │   ├── __init__.py
│   │   ├── common
│   │   │   ├── __init__.py
│   │   │   ├── common.py
│   │   │   ├── config.py
│   │   │   └── log.py
│   │   └── helper
│   │       ├── __init__.py
│   │       ├── data_helper.py
│   │       ├── io_helper.py
│   │       └── spark_helper.py
│   └── web
│       ├── __init__.py
│       ├── app
│       │   ├── __init__.py
│       │   ├── control
│       │   │   ├── __init__.py
│       │   │   ├── message.py
│       │   │   └── templete.py
│       │   ├── extension.py
│       │   ├── router
│       │   │   ├── __init__.py
│       │   │   ├── audit_router.py
│       │   │   ├── temp_router.py
│       │   ├── status.py
│       │   └── storage
│       │       ├── __init__.py
│       │       ├── common.py
│       │       ├── message.py
│       │       ├── model.py
│       │       └── templete.py
│       ├── config.so
│       ├── gunicorn_config.py
│       └── manager.py
├── start.sh
└── stop.sh
```
Execute the command `python3 py2so.py` in the terminal, then the project is compiled. You can find the compiled files in the `build` directory of this project as follows:
 ```
 .
├── README.md
├── data
│   └── conf
│       └── conf.ini
├── src
│   ├── __init__.py
│   ├── classifier
│   │   ├── __init__.py
│   │   ├── textcnn
│   │   │   ├── __init__.py
│   │   │   ├── evaluate.so
│   │   │   ├── infer.so
│   │   │   ├── preprocess.so
│   │   │   ├── textcnn.so
│   │   │   └── train.so
│   │   └── train.so
│   ├── utils
│   │   ├── __init__.py
│   │   ├── common
│   │   │   ├── __init__.py
│   │   │   ├── common.so
│   │   │   ├── config.py
│   │   │   └── log.so
│   │   └── helper
│   │       ├── __init__.py
│   │       ├── data_helper.so
│   │       ├── io_helper.so
│   │       └── spark_helper.so
│   └── web
│       ├── __init__.py
│       ├── app
│       │   ├── __init__.py
│       │   ├── control
│       │   │   ├── __init__.py
│       │   │   ├── message.so
│       │   │   └── templete.so
│       │   ├── extension.so
│       │   ├── router
│       │   │   ├── __init__.py
│       │   │   ├── audit_router.so
│       │   │   ├── temp_router.so
│       │   ├── status.so
│       │   └── storage
│       │       ├── __init__.py
│       │       ├── common.so
│       │       ├── message.so
│       │       ├── model.so
│       │       └── templete.so
│       ├── config.so
│       ├── gunicorn_config.py  # Ignore compiled files specified in scripts
│       └── manager.so
├── start.sh
└── stop.sh
 ```
In this case, you can start your project by executing the command `gunicorn -c web/gunicorn_config.py web.manager:app `. 

When a python file is compiled into a dynamic link library file, you can also use it in the original way. 

```
from src.classifier.evaluate import Infer
```

### Note 

The ignore compiled files, directories are specified in the script, you can modify it according to your own needs. Keep in mind that when modifying the configuration, you need to be careful not to copy `.git` directory.

## requirements
Make sure that `gcc` and `cython` are installed.
## Author
leyiwang.cn@gmail.com
