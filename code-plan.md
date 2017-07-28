# Outline of Pynome module

## Genome - class

### Properties

- _genomeDir
- _assebmlyVersion
- _taxonomicName

### Functions

- __init__(assebmlyVersion, taxonomicName, genomeDir)
- _uncompressFile() - uncompress a .gz file
- _compressFile() - compress a .gz file.
- getFilePrefix() - builds a prefix for all genome files.
- getGFF3() - gets the path of the GFF3 or NULL if not available.
- getFASTA() - gets the path of the FASTA or NULL if not available.
- printGenome() - output to terminal
- buildIndex() - uses the hisat2-build tool to index the .fa file
- buildGTF() - converts the GFF3 to GTF
- buildSpliceSites() - uses the hisat2_extract_splice_sites.py

## GenomeDatabase - class

### Properties

- _baseGenomeDir
- _genomeList[Genome1[], Genome2[], ...] an array of Genome objects
- _downloadProtocol ???

### Functions

- __init__(baseGenomeDir)
- initializes the genomeList array
- saveGenomes - saves the list of genomes to a .json file
- printGenomes - prints the list of genomes to the terminal
- findGenomes - overwritten by child class
- downloadGenomes - overwritten by child class

## EnsemblDatabase(GenomeDatabase)

### Properties

- _releaseVersion - eg. ‘realease-36’
- _ftp_genomes[]
- Functions
- _crawlFTP($current_dir, $listing_array) - recursive function to crawl the ftp server to find genome files.
  call _ftp.sendcmd function to get the current URL
  add each file in the current directory to the _ftp_LIST dictionary
  if a new directory is found then recurse _crawlFTP()
- _generateURI - generates the starting point uri for the recursive crawler - generates 8 urls, variable on the version requested.
- _parseListings() - iterate through the _ftp_LIST dictionary to find the genome files.
    - Path with filename
    - File size
    - findGenomes - Recursively traverses ftp directories in a depth first search. Calls:
    - ftp_listing = []
    - _ftp.connect()
    - startURL = _generateURI()
    - _crawlFTP(startURL, ftp_listing)
    - _ftp.close()
    - _parseListings(ftp_listings)
- downloadGenomes - downloads from an input list of uri / filepaths & write them to a local dir.


---

Learning
--------

On ftplib use:

http://effbot.org/librarybook/ftplib.htm

FILE NAMES

The files are consistently named following this pattern:
   <species>.<assembly>.<_version>.gff3.gz
   
   
Assembly accession numbers are distinctly-formatted sequence accession numbers that NCBI staff assign to individual genomic assemblies. Unlike other sequence accession numbers, assembly accessions do not represent a single sequence record, but rather the collection of sequence records that comprise an individual genomic assembly.

The format for GenBank (primary) assembly accessions is: [ GCA ][ _ ][nine digits][.][version number]
The format for RefSeq (NCBI-derived) assembly accessions is: [ GCF ][ _ ][nine digits][.][version number]