import ftplib
import tqdm
from pynome.ftpHelper import crawl_ftp_dir

ENSEMBL_FTP_URI = 'ftp.ensemblgenomes.org'
ENSEMBL_DATA_TYPES = ['gff3', 'fasta']
ENSEMBL_KINGDOMS = ['fungi', 'metazoa', 'plants', 'protists']


class EnsemblGenomeController:

    def __init__(self, release_version='release-37'):
        self.release_version = release_version
        self.local_base_path = None
        self.ftp = ftplib.FTP()

    @property
    def metadata_uri(self):
        return '/'.join(('pub', self.release_version, 'species.txt'))

    def download_metadata(self):
        self.ftp.connect(ENSEMBL_FTP_URI)
        self.ftp.login()
        self.ftp.retrbinary(
            cmd='RETR {}'.format(self.metadata_uri),
            open(self.local_base_path + 'species.txt', 'wb').write())
        self.ftp.quit()

    def find_genomes(self, uri_list, parsing_function=ensembl_line_parser):
        self.ftp.connect(ENSEMBL_FTP_URI)
        self.ftp.login()
        for uri in tqdm(uri_list):
            crawl_ftp_dir(
                database=self,
                top_dir=uri,
                parsing_function=parsing_function)
        self.ftp.quit()
        return

    def ensembl_line_parser(self, line, top_dir):
        """This function parses one 'line' at a time retrieved from an
        ``ftp.dir()`` command. This line has already been confirmed to
        not be a directory.

        :param top_dir: The parent directory.
        :param line: An input line, described in detail below.

        An example of one such line:

            ``"drwxr-sr-x  2 ftp   ftp    4096 Jan 13  2015 filename"``

        The files are consistently named following this pattern:

            ``<species>.<assembly>.<_version>.gff3.gz``

        This line is split by whitespace. For future reference, the indexes
        correspond (usually) to::

            + [0]:    the directory information.
            + [1]:    the number of items therein?
            + [2]:    unknown always 'ftp'
            + [3]:    unknown always 'ftp'
            + [4]:    the file size in bytes, 4096 is one block
            + [5]:    Month
            + [6]:    Day
            + [7]:    Year
            + [8]:    filename

        Either adds a genome, or returns nothing."""

        bad_words = ('chromosome', 'abinitio')

        def split_line(in_line):
            """Parse an individual item line from an ftp.dir() call.
            This function handles splitting, without assuming the line
            contains a valid genome file."""

            # Split the listing by whitespace.
            item = in_line.split()
            return {
                'dir_info': item[0],
                'dir_subfolders': item[1],
                'size': item[4],
                'item_name': item[-1]
            }

        def parse_genome_name(line_dict):
            """Takes an item line dictionary and splits the genomes name
            to get the desired values from it."""
            name_list = line_dict['item_name'].split('.', 2)
            genus_species = name_list[0]
            assembly_name = name_list[1]
            # Some species have sub-names
            try:
                gen_species_list = list(filter(None, genus_species.split('_')))
                # The first element should be the genus
                genus = gen_species_list[0]
                # The second should be the species
                species = gen_species_list[1]
                # The remainder should be the intra-specific name
                if len(gen_species_list) > 2:
                    intraspecific_name = '_'.join(gen_species_list[2:])
                    taxonomic_name = '_'.join(
                        [genus, species, intraspecific_name])
                    local_path = os.path.join(
                        self.download_path,
                        genus + '_' + species + '_' + intraspecific_name,
                        assembly_name)

                else:
                    taxonomic_name = '_'.join([genus, species])
                    intraspecific_name = None
                    local_path = os.path.join(
                        self.download_path,
                        genus + '_' + species, assembly_name)

            except:
                taxonomic_name = name_list[0]
                assembly_name = name_list[1]
                genus, species = genus_species.split('_', 1)
                intraspecific_name = None
                local_path = os.path.join(
                    self.download_path,
                    genus + '_' + species, assembly_name)

            return {
                'assembly_name': assembly_name,
                'genus': genus,
                'species': species,
                'taxonomic_name': taxonomic_name,
                'local_path': local_path,
                'intraspecific_name': intraspecific_name}

        def add_fasta(line_dict):
            fasta_genome = parse_genome_name(line_dict)
            update_dict = {
                'fasta_size': line_dict['size'],
                'fasta_uri': ''.join((top_dir, line_dict['item_name'])),
            }
            fasta_genome.update(update_dict)
            self.save_genome(**fasta_genome)
            return

        def add_gff3(line_dict):
            gff3_genome = parse_genome_name(line_dict)
            update_dict = {
                'gff3_size': line_dict['size'],
                'gff3_uri': ''.join((top_dir, line_dict['item_name'])),
            }
            gff3_genome.update(update_dict)
            self.save_genome(**gff3_genome)
            return

        line_dict = split_line(line)

        if any(bw in line_dict['item_name'] for bw in bad_words):
            # This means that one of the undesired files has been located.
            return

        elif line_dict['item_name'].endswith('dna.toplevel.fa.gz'):
            add_fasta(line_dict)
            return

        elif line_dict['item_name'].endswith('gff3.gz'):
            add_gff3(line_dict)
            return
