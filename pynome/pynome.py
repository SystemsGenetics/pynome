"""Retrieves genome data files & metadata form online databases.

In this version (0.1.0) only the Ensembl database is implemented.

Usage:
    pynome [--mode=find-genomes]
    pynome [--mode=download-genomes] [--download-dir=DIRECTORY]
"""
import pynome
import docopt

def get_mode():
    """Modes are:
        + find-genomes
        + download-genomes"""
    return {
        'find-genomes': find_genomes,
        'download-genomes': download_genomes,
    }

def main():
    # Set the help script.
    args = docopt.docopt(__doc__)
    mode = args['--mode'] or 'find-genomes'


if __name__ == '__main__':
    main()
