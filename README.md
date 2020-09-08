# Pynome

Pynome, a Python command line interface tool, provides the user with a way to
download desired genome assembly files from the
[Ensembl](https://www.ensembl.org/) and [NCBI](https://www.ncbi.nlm.nih.gov/) databases.


## Installation

Pip can be used for installation.

```bash
$ pip install .
```

## Usage

Commands can be run one at a time for crawling and mirroring.

Crawling:

```bash
$ pynome -c
```

Mirroring:

```bash
$ pynome -m
```

Or strung together.

```bash
pynome -cm
```

## Parallel indexing

Indexing is designed to be done in parallel due to the large volume of assemblies that is mirrored.
Parellel execution is done with two steps. The first step generated a list of pynome job files, each
file being a single assembly whose indexes require updating. The second step is processing a single
job and is meant to be done in parallel.

Generate job files:

```bash
pynome -I
```

Process a job file:

```bash
pynome -i -f <PATH>
```

Where <PATH\> is the path to a generated pynome job file that has the format 'pynome_job_#####.txt'
where ##### is the job number.

## Local database root directory

The default root directory where assemblies are stored is $HOME/species. To change that to a
different directory use the -d argument. For example to crawl using a custom directory:

```bash
$ pynome -d /custom -c
```
