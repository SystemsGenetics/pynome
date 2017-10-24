import os
from abc import ABC, abstractmethod


class Genome:
    def __init__(self, **kwds):
        self.assembly_name = None
        self.genus = None
        self.species = None
        self.taxonomic_name = None
        self.infraspecific_name = None
        self.taxonomy_id = None
        super().__init__(**kwds)

    @property
    def genome_filename(self):
        if self.infraspecific_name:
            return ''.join([
                self.genus,
                '_', self.species,
                '_', self.infraspecific_name,
                '-', self.assembly_name])
        else:
            return ''.join([
                self.genus,
                '_', self.species,
                '-', self.assembly_name])

    @property
    def genome_path(self):
        if self.infraspecific_name:
            return os.path.join(
                self._root_storage_path,
                self.genus +
                '_' + self.species +
                '_' + self._intraspecific_name,
                self.assembly_name)
        else:
            return os.path.join(
                self._root_storage_path,
                self.genus + '_' + self.species,
                self.assembly_name)

    def create_local_path(self):
        if not os.path.exists(self.genome_path):
            os.makedirs(self.genome_path)


class LocalGenomeFile(ABC):
    """This is the base/virtual class for each Genome file."""

    def __init__(self, genome_filename, base_path, extension):
        self.genome_filename = genome_filename
        self.base_path = base_path
        self.extension = extension

    @property
    def filepath_and_filename(self):
        return os.path.join(self.root_filepath, self.filename)


class FastaGz(LocalGenomeFile):
    def compare_checksum():
        pass


class Gff3Gz(LocalGenomeFile):
    def compare_checksum():
        pass


class Fasta(LocalGenomeFile):
    pass


class Gff3(LocalGenomeFile):
    pass


class HisatIndex(LocalGenomeFile):
    pass


class SpliceSites(LocalGenomeFile):
    pass


class GTF(LocalGenomeFile):
    pass


class EnsemblGenome(
        Genome, LocalGenomeFile, FastaGz, Fasta,
        Gff3Gz, Gff3, HisatIndex, SpliceSites, GTF):
    pass
