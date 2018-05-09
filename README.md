# Pynome

Pynome, a Python command line interface tool, provides the user with a way to
download desired genome assembly files from the
[Ensembl](https://www.ensembl.org/) database.


## Installation

```bash
$ python setup.py install
```


## Usage

Commands can be run one at a time:

```bash
$ pynome discover
$ pynome list
$ pynome download
$ pynome prepare
```

Or strung together.

```bash
pynome discover download prepare
```

## Docker Implementation

Pynome can be run as a Docker application. For iRODs integration you must
create a docker secret named `irods_password` with the password of the iRODs
user to be used to `put` files into iRODs.

The docker node used must be part of a swarm.

```bash
$ docker swarm init
```

## TODO

- [ ] Add delete() functions.
