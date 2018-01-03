# Pynome

A script to handle the collection and pre-processing for the SciDAS work-flow.

## To Do:

- [x] Gather todos here.
- [ ] Refactor command line interface
- [ ] Refactor unit tests.
- [x] Add a `setup.py`.
- [ ] Re-comment `EnsemblDatabase.py`.
- [x] Write SRA functionality.
- [ ] Write SRA test functions and test sra functionality.
- [ ] Refactor `EnsemblDatabase`.
- [ ] Add `setuptools` integration.

### `cli.py`

- [x] Create command group. ie `pynome command --arguments.`
- [ ] SRA - create directory from accession number.
- [ ] SRA - download SRA metadata.

### `utils.py`

- [ ] Comment the `cd` class.
- [ ] Completely comment the `crawl_ftp_dir` class.

### 'Storage.py'

- [ ] Comment the `Storage` class.

### 'sra.py'

- [ ] Write SRA unit tests.
- [ ] Add a trailing underscore handler for the chunk_accession_id() function.

### 'SQLiteStorage.py'

- [ ] Write SRA unit tests.

### 'GenomeDatabase.py'

- [ ] Write `GenomeDatabase` unit tests.

### 'GenomeAssembly.py'

- [x] Write `GenomeAssembly` unit tests.
- [x] Comment the `GenomeAssembly` class.

### 'EnsemblDatabase.py'

- [ ] Fix exception handling within.
- [ ] Write `GenomeAssembly` unit tests.

### '__main__.py'

- [x] Refactor CLI interface using Click.
