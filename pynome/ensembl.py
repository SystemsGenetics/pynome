"""
================
Ensembl Database
================

The ensembl database module. A child class of the genome database class,
this module cotains all code directly related to connecting and parsing data
from the ensembl geneome database.
"""

import ftplib
import os
import logging
import itertools
import pandas
import subprocess
from pynome.database import GenomeDatabase
from pynome.ftpHelper import crawl_ftp_dir
from tqdm import tqdm

ENSEMBL_FTP_URI = 'ftp.ensemblgenomes.org'
ENSEMBL_DATA_TYPES = ['gff3', 'fasta']
ENSEMBL_KINGDOMS = ['fungi', 'metazoa', 'plants', 'protists']


class EnsemblDatabase(GenomeDatabase):
    """The EnsemblDatabase class. This handles finding and downloading
    genomes from the ensembl genome database. The database url is:

        ``ftp.ensemblgenomes.org``

    It does so by recursively walking the ftp directory. It only collects
    those genomes that have a ``*.gff3.gz`` or a ``*.fa.gz`` file.
    """

    def __init__(self, release_version=37, **kwargs):
        super().__init__(**kwargs)  # Call parent class init
        self._release_version = None  # set by the release version setter
        self._release_number = None  # set by the release version setter
        self.release_version = release_version
        self.ftp = ftplib.FTP()  # the ftp instance for the database
        self.species_metadata = None

    @property
    def release_version(self):
        """Release version property. Should be in the form:
            ``"release-#", "release-36"``"""
        return self._release_version

    @release_version.setter
    def release_version(self, value):
        """Setter for the release_version. Accepts an input integer and returns
        a string in the form: 'release-##' """
        self._release_number = value
        self._release_version = 'release-' + str(value)

    def generate_metadata_uri(self):
        """Generates a URI that will locate the metadata. This URI is of the
        form:

        ``/pub/release-36/species.txt``
        """
        uri_dict = {}
        species_txt = 'species.txt'
        uri = '/'.join(('pub', self._release_version, species_txt))
        uri_dict[uri] = species_txt
        return uri_dict

    def download_metadata(self):
        """Downloads the `species.txt` files. This is a tab delimited listing
        of metadata. """

        metadata_uri_dict = self.generate_metadata_uri()

        self.ftp.connect(ENSEMBL_FTP_URI)
        self.ftp.login()

        for uri, file_name in metadata_uri_dict.items():

            size_estimate = self.ftp.size(uri) / 8.192
            target_dir = os.path.join(self.download_path, file_name)

            if os.path.isfile(target_dir):
                return

            if not os.path.exists(os.path.dirname(target_dir)):
                os.makedirs(os.path.dirname(target_dir))

            with tqdm(total=int(size_estimate), unit_scale=True,
                      unit='MB') as meta_pbar:

                with open(target_dir, 'wb') as curr_file:

                    def callback(data):
                        update_size = len(data) / 8.192
                        meta_pbar.update(int(update_size))
                        curr_file.write(data)

                    try:
                        self.ftp.retrbinary(
                            cmd='RETR {}'.format(uri),
                            callback=callback)
                    except:
                        logging.warning('UNABLE TO DOWNLOAD METADATA!')
        return

    def generate_uri(self):
        """Generates the uri strings needed to download the genomes
        from the ensembl database.

        **Returns**: List of Strings of URIs for the ensembl database. eg::

            'pub/fungi/release-36/gff3/',
            'pub/metazoa/release-36/gff3/',
            ...

        This is an extremely case-specific function."""
        uri_list = []
        # Unique permutations of data types and kingdoms.
        uri_gen = itertools.product(ENSEMBL_DATA_TYPES, ENSEMBL_KINGDOMS)
        # For each iteration, return the desired URI.
        for item in uri_gen:
            uri = '/'.join(('pub', item[1],  # the clade or kingdom
                            self._release_version,
                            item[0], '',))  # the data type
            uri_list.append(uri)
        return uri_list

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
                gen_species_list = genus_species.split('_')
                gen_species_list = list(filter(None, gen_species_list))
                logging.debug('filtered_gen_species_list')
                logging.debug(gen_species_list)
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

                    base_filename = "".join([
                        genus,
                        "_",
                        species,
                        "_",
                        intraspecific_name,
                        "-",
                        assembly_name
                    ])

                else:
                    taxonomic_name = '_'.join([genus, species])

                    intraspecific_name = None

                    local_path = os.path.join(
                        self.download_path,
                        genus + '_' + species, assembly_name)

                    base_filename = "".join([
                        genus,
                        "_",
                        species,
                        "-",
                        assembly_name
                    ])

            except:
                taxonomic_name = name_list[0]
                assembly_name = name_list[1]
                genus, species = genus_species.split('_', 1)
                intraspecific_name = None
                local_path = os.path.join(
                    self.download_path,
                    genus + '_' + species, assembly_name)
                base_filename = "".join([
                    genus,
                    "_",
                    species,
                    "-",
                    assembly_name
                ])

            return {
                'taxonomic_name': taxonomic_name,
                'genus': genus,
                'assembly_name': assembly_name,
                'species': species,
                'local_path': local_path,
                'base_filename': base_filename,
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

    def find_genomes(self, uri_list, parsing_function=ensembl_line_parser):
        """Private function that handles finding the list of genomes.

        :param uri_list: This should be a list of base URIs to start
            the ftp crawler from.
        :param parsing_function: This should be a function that reads an
            ``ftplib.dir()`` line output. The  output sent to such a function
            will always be a file, not a directory.

        """
        self.ftp.connect(ENSEMBL_FTP_URI)  # connect to the ensemble ftp
        self.ftp.login()
        for uri in tqdm(uri_list):
            # logging.info('Parent crawl dir initialized as: {}'.format(uri))
            crawl_ftp_dir(
                database=self,
                top_dir=uri,
                parsing_function=parsing_function)
        self.ftp.quit()  # close the ftp connection
        return

    def estimate_download_size(self):
        size = []
        genomes = self.get_found_genomes()
        for genome in genomes:
            size.extend((
                genome.gff3_size,
                genome.fasta_size
            ))
        return sum(filter(None, size))

    def download_genomes(self):
        """This function downloads all genomes that have been found and stored
        in the database.

        The directory structure to fit the files downloaded is as follows::

            Genome/
              [genus]_[species]{_[intraspecific_name]}/
                [assembly_name]/
                  [genus]_[species]{_[intraspecific_name]}-[assembly_name].gff3
                  [genus]_[species]{_[intraspecific_name]}-[assembly_name].fasta

        """
        size_estimate = self.estimate_download_size() / 8.192
        genomes = self.get_found_genomes()
        self.ftp.connect(ENSEMBL_FTP_URI)
        self.ftp.login()

        with tqdm(total=int(size_estimate), unit_scale=True,
                  unit='B') as total_pbar:
            # Iterate through the list of acquired genomes.
            for genome in genomes:
                # Create a dictionary. This is kind of awkward.
                download_dict = {
                    genome.fasta_uri: '.fa.gz',
                    genome.gff3_uri: '.gff3.gz',
                }
                # Create the target directory.
                target_dir = genome.local_path
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir)

                # Iterate through the download dictionary
                for uri, file_ext in download_dict.items():
                    if genome.intraspecific_name:
                        filename = "".join([
                            genome.genus,
                            "_",
                            genome.species,
                            "_",
                            genome.intraspecific_name,
                            "-",
                            genome.assembly_name
                        ])
                    else:
                        filename = "".join([
                            genome.genus,
                            "_",
                            genome.species,
                            "-",
                            genome.assembly_name
                        ])

                    target_file = os.path.join(
                        target_dir, filename + file_ext)

                    with open(target_file, 'wb') as curr_file:
                        def callback(data):
                            update_size = len(data) / 8.192
                            total_pbar.update(int(update_size))
                            curr_file.write(data)
                        try:
                            self.ftp.retrbinary(
                                cmd='RETR {}'.format(uri),
                                callback=callback)
                        except:
                            logging.warning('UNABLE TO DOWNLOAD A GENOME')
                            logging.warning(genome.taxonomic_name)
        self.ftp.quit()  # close the ftp connection
        return

    def check_local_genome_integrity(self):
        """
        Checks the local genome files downloaded and ensures that they match
        the linux sum provided by ensemble. Returns True if the genome is good,
        and false otherwise. Assumes the files are still zipped.
        """
        def get_checksum_uri(uri):
            """
            Breaks apart a remote uri to ensure the correct checksum file is
            considered.

            :param uri: The base uri where the deisred CHECKSUMS file is.
            :param tag: The tag to apply, this allows us to discern between the
            fasta and gff3 checksum files.

            :returns: A list that contains the URI of the target CHECKSUMS file
            and the corresponding filename that is to be checked.
            """
            uri, filename = uri.rsplit("/", 1)
            return [uri + "/CHECKSUMS", filename]

        def download_checksum_file(checksum_URI, local_download_path, tag):
            """
            Downloads a given checksum for the fasta and gff3 files for a
            given genome. Assumes an FTP connection is already initialized.

            :param checksum_URI:
            :param local_download_path:

            :returns:
            """
            target_local_dir = os.path.join(
                local_download_path,
                "CHECKSUMS" + tag)

            self.ftp.retrbinary(
                cmd="RETR {}".format(checksum_URI),
                open(target_local_dir, "wb").write)
            return

        def read_genome_checksum_files(genome, curr_file):
            """
            Reads a downloaded checksum file, and compares the values
            therein to a locally computed one. The blocks and checksum are
            generated with the standard UNIX `sum` utility.

            :param genome:
            :param curr_file:

            :returns: A list that contains the checksum and block count.
            """
            with open(local_checksum_filepath, "r") as chk_file:
                content = chk_file.readlines()

            for line in content:
                line = content.split()
                if line[-1] == curr_file:  # then this is the right line
                    chksum, blocks = line[0:1]
            return [chksum, blocks]

        def calculate_local_unix_sum(file):
            """
            Calculates the unix sum of a given file.
            TODO: Perhaps move this to the utils.py file.

            :param file:
            :returns:
            """
            cmd = ["sum", file]
            subprocess.run(cmd, stdout=subprocess.PIPE)
            chksum, blocks = command.stdout.strip().split()
            return [chksum, blocks]

        # Connect and login to the ftp server.
        self.ftp.connect(ENSEMBL_FTP_URI)
        self.ftp.login()

        # Get all the genomes
        for genome in tqdm(self.get_found_genomes()):

            # Get the gff3 CHECKSUMS file.
            gff3_sum_uri, gff3_filename = get_checksum_uri(
                genome.gff3_uri)
            download_checksum_file(gff3_sum_uri, genome.local_path, "_gff3")

            # Get the fasta CHECKSUMS file.
            fasta_sum_uri, fasta_filename = get_checksum_uri(
                genome.fasta_uri)
            download_checksum_file(gff3_sum_uri, genome.local_path, "_fasta")

            # Check the GFF3 file.
            good_check_vals = read_genome_checksum_files(genome, gff3_filename)
            local_check_vals = calculate_local_unix_sum()

        self.ftp.quit()  # close the ftp connection
        return

    def read_species_metadata(self, file_name="species.txt"):
        """
        Reads the downloaded metadata file: ``species.txt`` file and returns a
        pandas data frame.

        :param file_name: The name of ``species.txt``.

        The following are the column names in the dataframe:

        #name
        species
        division
        **taxonomy_id** <-- The one we are interested in.
        assembly
        assembly_accession
        genebuild
        variation
        pan_compara
        peptide_compara
        genome_alignments
        other_alignments
        core_db
        species_id
        """
        # Build the path of the target file.
        species_path = os.path.join(self.download_path, file_name)
        # Read the csv.
        metadata_df = pandas.read_csv(
            filepath_or_buffer=species_path,
            error_bad_lines=False,
            sep="\t",
            index_col=False,
        )
        self.species_metadata = metadata_df
        return

    def get_taxonomy_id(self, species):
        """
        Looks an individual taxonomy_id in the given pandas data frame.

        :param species: The species to return the taxonomy id of.

        :returns: A taxonomy id
        """
        taxonomy_id = self.species_metadata[
            self.species_metadata['species'].str.match(
                species.lower())]['taxonomy_id'].values
        if taxonomy_id.size == 0:
            logging.error(
                'Unable to find a taxonomy id for {}'.format(species))
            return None
        logging.debug('Found taxonomy id: {0}'.format(taxonomy_id))
        return str(taxonomy_id[0])

    def add_taxonomy_ids(self):
        # Read the metadata file to get the pandas dataframe:
        self.read_species_metadata()
        for genome in tqdm(self.get_found_genomes()):
            taxonomy_id = self.get_taxonomy_id(genome.taxonomic_name)
            update_dict = {
                'taxonomic_name': genome.taxonomic_name,
                'taxonomy_id': taxonomy_id
            }
            self.save_genome(**update_dict)

    # def decompress_genomes(self):
    #     """
    #     Decompresses the genomes that have been downloaded. This will be
    #     changed to use a slurm array.
    #     """
    #     # Get all the genomes that have been found and saved in the SQLite db
    #     genomes = self.get_found_genomes()

    #     # Iterate over the list of genomes
    #     for genome in genomes:
    #         # Build the path in the same way as the download function.
    #         target_dir = os.path.join(
    #             self.download_path, genome.taxonomic_name)
    #         # Go to the target directory and unzip the files therein.
    #         with cd(target_dir):
    #             # TODO: Consider removing the star and specifying the files
    #             subprocess.run('gunzip *', shell=True)
    #     return

    # def slurm_decompress_genome(self, slurm_index):
    #     """
    #     This function is to be used in a slurm array. The slurm_index value
    #     refers to a list entry from a sorted call of get_found_genomes.
    #     This will fail if new entries are added to the database while the
    #     decompression command runs.

    #     This command should be called in slurm scripts in this way:

    #     >>> python3 -m pynome --slurm-decompress <idx>

    #     .. todo:: Implement the CLI interface for the above example.
    #     """
    #     # Find all genomes in the database
    #     genomes = self.get_found_genomes()
    #     # Sort these alphabetically and store them as a tuple
    #     genomes.sort()
    #     # Retrieve the index based on slurm index
    #     active_genome = genomes[slurm_index]
    #     # Build the target dir
    #     path = os.path.join(self.download_path, active_genome.taxonomic_name)
    #     # Run the decompression command
    #     with cd(path):
    #         subprocess.run('gunzip *', shell=True)
    #     return

    # def generate_hisat_index(self):
    #     """
    #     Run the hisat conversion tool on the supplied path list.

    #     HISAT tool options:

    #     -f

    #     Reads (specified with <m1>, <m2>, <s>) are FASTA files. FASTA files
    #     usually have extension .fa, .fasta, .mfa, .fna or similar. FASTA
    #     files do not have a way of specifying quality values, so when -f
    #     is set, the result is as if --ignore-quals is also set.

    #     If your computer has multiple processors/cores, use -p

    #     The -p option causes HISAT to launch a specified number of parallel
    #     search threads. Each thread runs on a different processor/core and
    #     all threads find alignments in parallel, increasing alignment
    #     throughput by approximately a multiple of the number of threads
    #     (though in practice, speedup is somewhat worse than linear).

    #     """
    #     genome_list = self.get_found_genomes()

    #     # The hisat tool will create the indexes in the current directory.
    #     for gen in tqdm(genome_list):
    #         # build the path
    #         path = os.path.join(self.download_path, gen.taxonomic_name)
    #         # build the filename
    #         fa_file = gen.taxonomic_name + '.fa'
    #         # build the hisat2-build command
    #         cmd = ['hisat2-build', '-f', fa_file, gen.taxonomic_name]
    #         # change to the path, and try to run the command.
    #         # Log an error if it fails.
    #         with cd(path):
    #             try:
    #                 subprocess.run(cmd)
    #             except:
    #                 logging.warning(
    #                     'Unable to build ht2 index of {}'.format(
    #                         gen.taxonomic_name))
    #     return

    # def generate_splice_sites(self):
    #     """
    #     Command example for splice site generation:

    #     >>> python hisat2_extract_splice_sites.py GRCh38.gtf > Splice_Sites.txt
    #     :return:
    #     """
    #     genome_list = self.get_found_genomes()

    #     for gen in tqdm(genome_list):
    #         logging.debug(
    #             'Attempting to generate splice sites for {}'.format(
    #                 gen.taxonomic_name))
    #         gtf_path = os.path.join(self.download_path, gen.taxonomic_name)
    #         gft_file = gen.taxonomic_name + '.gft'
    #         output_file = 'Splice_sites.txt'
    #         with cd(gtf_path):
    #             extract_splice_sites(gft_file, output_file)
    #     return

    # def generate_gtf(self):
    #     """
    #     Uses **gffread** command to generate `\*.gtf` files.

    #     ``gffread -T <TARGET-FILE>.gff3 -o <TARGET-FILE>.gtf``

    #     Should output to the `.gtf2` file format by default.
    #     """
    #     genome_list = self.get_found_genomes()

    #     for gen in tqdm(genome_list):
    #         # Build the path
    #         path = os.path.join(self.download_path, gen.taxonomic_name)
    #         # build the file name
    #         gff3_file = gen.taxonomic_name + '.gff3'
    #         gff_out_file = gen.taxonomic_name + '.gtf'
    #         # Build the command:
    #         cmd = ['gffread', '-T', gff3_file, '-o', gff_out_file]
    #         with cd(path):
    #             try:
    #                 subprocess.run(cmd)
    #             except:
    #                 logging.warning(
    #                     'Unable to generate gtf file for {}'.format(
    #                         gen.taxonomic_name))

    #     return
