# tableio-cfg-json

`tableio-cfg-json` is a small encapulation package of tableio configuration
in json format. This encapsulates the bridiging between 2 independent
packages [https://pypi.org/project/tableio/](https://pypi.org/project/tableio/)
and [https://pypi.org/project/config-as-json/](https://pypi.org/project/config-as-json/).

`tableio-cfg-json` provides a complete configuration of `tableio` using `config-as-json`.
This configuration can be used as a complete configuration file, or it can be used as
a nested configuration for the tablio input/output of an application with also other
configurations.

## Installation

`tableio-cfg-json` requires Python 3.12 or newer.

```sh
pip install --upgrade tableio-cfg-json
```

## Main entry points

To be written

## Documentation 

- Public API notes: [doc/api.md](https://bitbucket.org/tom-bjorkholm/tableio_cfg_json/src/master/doc/api.md)

- Protected/internal API notes: [doc/protected_api.md](https://bitbucket.org/tom-bjorkholm/tableio_cfg_json/src/master//doc/protected_api.md)

- Source repository: [config_as_json](https://bitbucket.org/tom-bjorkholm/tableio_cfg_json/)

## License

MIT

## Test summary

- Test result: 262 passed in 9s
- No flake8 warnings.
- No mypy errors found.
- No python layout warnings.
- Built version(s): 0.0.1
- Build and test using Python 3.14.4
