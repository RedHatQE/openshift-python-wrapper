# Function Call Force Names (a flake8 plugin)
FunctionCallForceNames (FCFN001) is a flake8 plugin, which role is enforcing
that functions are called with arg=value, rather than value only.

### Example:
Valid call:
```python
 foo(num=1, txt="txt")
```

Invalid call:
```python
 foo(1, txt="txt")
```

In case of an invalid call - the plugin will trigger a flake8 failure:
```bash
$ pre-commit run --all-files
...
flake8...................................................................Failed
...
<path-to-file>:<line#>:<function-call-column#>: FCFN001: [<calling-function-name>] function should be called with keywords arguments. value: <value> (line:<line#> column:<missing-name-column#>)
```
(pre-commit includes invokation of flake8).

For example:
```bash
$ pre-commit run --all-files
...
flake8...................................................................Failed
...
tests/network/general/test_bridge_marker.py:135:5: FCFN001: [test_bridge_marker_no_device] function should be called with keywords arguments. value: pod (line:135 column:45)
```

### Note:
1. It's no necessary to explictly call pre-commit to enforce FCFN001,
as flake8 is invoked automatically when running "git commit".
2. To test flake8 validity of a specific file, you can run
```bash
$ pre-commit run --file <path-to-file>
```
For example:
```bash
$ pre-commit run --file tests/network/general/test_bridge_marker.py
```
