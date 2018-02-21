# Pynome

Pynome, a Python command line interface tool, provides the user with a way to
download desired genome assembly files from the
[Ensembl](https://www.ensembl.org/) database.


## TODO

- [x] Gather TODOs.
- [x] Add metadata json files - one with pynome info, the other with ensembl info.
- [x] Factor out cd from prepare methods.
- [x] Docstring for prepare methods.
- [x] Update hisat2 indexing to use more than one CPU.
- [x] Consider API linkage to the crawl command.
- [x] assembly.delete() -- move to AssemblyStorage
- [x] assembly.prepare() -- move to AssemblyStorage
- [x] assembly.update() -- move to AssemblyStorage
- [x] Create api for selecting assemblies by:
  + Species
  + Genus
  + Intraspecific_name
  + Assembly_ID
- [x] Add a column that records the source remote database.
- [x] assemblystorage.download()
- [x] assemblystorage.query_local_assemblies_by()
- [x] assemblystorage.add_source()
- [x] assemblystorage.prepare()
- [x] Consider the changes needed to the CLI for SRA functionality.
- [ ] Download function from CLI interface needs to call all needed ensembl functions
- [ ] assemblystorage.push_irods()
- [ ] cli.push_irods()
- [ ] Create Docker image.
- [ ] Add Travis-CI integration.


## Installation

- [ ] Go over setup.py
- [ ] Write instructions.
