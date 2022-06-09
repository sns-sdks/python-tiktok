## Dependencies

These distributions will be installed automatically when installing python-tiktok.

- [Requests](https://2.python-requests.org/en/master/) is an elegant and simple HTTP library for Python, built for human beings.

## Installation

#### From [`Pypi`](https://pypi.org/project/python-tiktok/)

``` shell
$ pip install python-tiktok
```

#### From source

use [`Poetry`](https://python-poetry.org/)

``` shell
$ git clone https://github.com/sns-sdks/python-tiktok.git
$ cd python-tiktok
$ make env
$ poetry build
```

```shell
make env
```

### Testing

Test the code, Run:

```shell
make test
```

See the coverage information:

```shell
make cov-term
```
