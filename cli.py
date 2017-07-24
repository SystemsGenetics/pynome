"""
Command Line Interface for Pynome
=================================

This is the script that should be run from the terminal. It will
walk the user through the steps needed to scrape genomes from 
the internet.

EnsemblGenomes is the only database currently initialized.

## EnsemblGenomes

The `cli.py` script will ask the following of the user:

    + Where the download location should be.
    + Where the SQL database URL or location is.

The script will then read the databases supplied, or create a 
new sqlite database if one is not found. Then it will ask the
user if they would like to collect the available genomes. 

After running the ftp scraper, the script will report the 
number of genomes found, as well as their total sizes.
"""

# from .genomedatabase import GenomeDatabase
# from .  import EnsemblDatabase
import pynome.ensembldatabase
# from . import EnsemblDatabase
# from .genome import Genome
# TODO: Define an __all__ attribute and simplify these imports.
# from .ensembldatabase import EnsemblDatabase
endb = pynome.ensembldatabase.EnsemblDatabase

def main():
    print('#'*80)
    print('\n')
    print('Command line interface to Pynome activated.')
    print('#'*80)
    print('There are no options! There are no rails! Are you sure? TOO BAD.')
    crawl_test_uri = ['pub/fungi/release-36/gff3/fungi_rozellomycota1_collection/',
    'pub/fungi/release-36/fasta/fungi_rozellomycota1_collection/']
    TEDB = endb()
    TEDB.crawl_ftp(crawl_test_uri, TEDB.ensembl_dir_parser)
    test_query = TEDB.print_genomes()
    print(test_query)

if __name__ == '__main__':
    main()
