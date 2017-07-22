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
from . ensembldatabase import EnsemblDatabase
# import pynome
# from . import EnsemblDatabase
# from .genome import Genome
# TODO: Define an __all__ attribute and simplify these imports.


def main():
    print('#'*80)
    print('\n')
    print('Command line interface to Pynome activated.')
    print('#'*80)
    print('There are no options! There are no rails! Are you sure? TOO BAD.')
    test_ensembl_db = EnsemblDatabase()
    test_ensembl_db.find_genomes()



if __name__ == '__main__':
    main()