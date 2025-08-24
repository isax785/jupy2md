# Readme

`Jupy2Md`  is a class implementing the conversion can be used from:

- the dedicated GUI;
- command line.

**Tasks**

- [ ] `#t` test `Jupy2Md` class
- [ ] `#f` count `\n` - only at the **end** of each block
- [ ] `#f` image links
- done
  - [x] `#u` finalize `jupy2md` function usage (command line)
  - [x] `#f` filepaths: absolute and relative
  - [x] `#u` upgrade to `Jupy2Md` class
  - [x] `#u` implement `Jupy2Md` class
  - [x] `#a` retrive programming language name from metadata  
  - [x] `#a` jupyter file with all the possible outputs for testing purposes

**GUI and `Jupy2Md`**

```python
class MainWindow:
    def __init__(self):
        self.jupy2md = None
        ...
```

- first file selection or select new one: `self.jupy2md=Jupy2Md`
- any checkbox selection: `self.jupy2md.convert_to_md(settings)`
- save -> `self.jupy2md.export(folder)`

## Command Line

Convert via shell:

```shell
  python jupy2md.py jupyter_notebook_path.ipynb
```

The export folder will be located in the same directory of the jupyter notebook.

The command can run from anywhere. It follows that the `jupy2md.py` file has to be properly located and provided with its complete relative path.