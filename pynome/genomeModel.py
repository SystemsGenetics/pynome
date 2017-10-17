import os
import subprocess


class Genome:
    def __init__(self, **kwds):
        self.assembly_name = None
        self.genus = None
        self.species = None
        self.taxonomic_name = None
        self.infraspecific_name = None
        self.taxonomy_id = None
        super().__init__(**kwds)

    def save_genome_metadata_json(self):
        pass


class GenomeLocalStorage(Genome):
    def __init__(self, root_storage_path, **kwds):
        self._root_storage_path = root_storage_path
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


class EnsemblFasta(GenomeLocalStorage):
    def __init__(self, **kwds):
        self.fasta_uri = None
        self.fasta_remote_size = None
        super().__init__(**kwds)

    @property
    def local_fasta_path(self):
        return os.path.join(self.genome_path, self.genome_filename + 'fa.gz')

    @property
    def local_fasta_checksum(self):
        return os.path.join(self.genome_path, 'fasta_CHECKSUM')

    @property
    def remote_fasta_checksum_uri(self):
        uri, filename = self.fasta_uri.rsplit('/', 1)
        return uri

    @property
    def remote_fasta_filename(self):
        uri, filename = self.fasta_uri.rsplit('/', 1)
        return filename

    def download_fasta_gz(self, active_ftp_connection):
        active_ftp_connection.retrbinary(
            cmd='RETR {}'.format(self.fasta_uri),
            open(self.local_fasta_path, 'wb').write())

    def download_fasta_checksum(self):
        active_ftp_connection.retrbinary(
            cmd='RETR {}'.format(self.fasta_uri),
            open(self.local_fasta_checksum, 'wb').write())

        with open(self.local_fasta_checksum, 'r') as chk_file:
            content = chk_file.readlines()
            for line in content:
                line = content.split()
                if line[-1] == self.remote_fasta_filename:
                    chksum, blocks = line[0:1]
            return [chksum, blocks]

    def local_fasta_checksum_blocks(self):
        command = subprocess.run(
            ["sum", self.local_fasta_path],
            stdout=subprocess.PIPE)
        outsum, blocks = command.stdout.strip().split()
        return [outsum, blocks]


class EnsemblGFF3(GenomeLocalStorage):
    def __init__(self, **kwds):
        self.gff3_uri = None
        self.gff3_remote_size = None
        super().__init__(**kwds)

    @property
    def local_gff3_path(self):
        return os.path.join(self.genome_path, self.genome_filename + 'fa.gz')

    @property
    def local_gff3_checksum(self):
        return os.path.join(self.genome_path, 'gff3_CHECKSUM')

    @property
    def remote_gff3_checksum_uri(self):
        uri, filename = self.gff3_uri.rsplit('/', 1)
        return uri

    @property
    def remote_gff3_filename(self):
        uri, filename = self.gff3_uri.rsplit('/', 1)
        return filename

    def download_gff3_gz(self, active_ftp_connection):
        active_ftp_connection.retrbinary(
            cmd='RETR {}'.format(self.gff3_uri),
            open(self.local_gff3_path, 'wb').write())

    def download_gff3_checksum(self):
        active_ftp_connection.retrbinary(
            cmd='RETR {}'.format(self.gff3_uri),
            open(self.local_gff3_checksum, 'wb').write())

        with open(self.local_gff3_checksum, 'r') as chk_file:
            content = chk_file.readlines()
            for line in content:
                line = content.split()
                if line[-1] == self.remote_gff3_filename:
                    chksum, blocks = line[0:1]
            return [chksum, blocks]

    def local_gff3_checksum_blocks(self):
        command = subprocess.run(
            ["sum", self.local_gff3_path],
            stdout=subprocess.PIPE)
        outsum, blocks = command.stdout.strip().split()
        return [outsum, blocks]
