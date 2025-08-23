# `Jupy2Md` Development Readme

The class implementing the conversion can be used from:

- the dedicated GUI
- command line

**Tasks**
- [ ] `#f` filepaths: absolute and relative
- [ ] `#u` upgrade to `Jupy2Md` class
- [ ] `#t` test `Jupy2Md` class
- [ ] `#f` count `\n` - only at the **end** of each block
- [ ] `#u` finalize `jupy2md` function usage (command line)
- done
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

`>>` to be fully tested (absolute and relative path)