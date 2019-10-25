from ftplib import FTP
from ..assembly import register_crawler

# For FASTA files: they ALWAYS end in *.toplevel.fa.gz
# Found in http://ftp.ensemblorg.ebi.ac.uk/pub/release-92/fasta/

# For GFF3 files: they ALWAYS end in *.92.gff3.gz
# Found in http://ftp.ensemblorg.ebi.ac.uk/pub/release-92/gff3/






FTP_HOST = "ftp.ensembl.org"
FTP_ROOT_DIR = "/pub"
FTP_RELEASE_BASENAME = "release-"
FTP_FASTA_DIR = "/fasta"
FTP_IGNORED_DIRS = ["cdna","cds","dna_index","ncrna","pep"]
FASTA_EXTENSION = ".dna.toplevel.fa.gz"






@register_crawler("ensemble")
def crawl():
    ftp = FTP(FTP_HOST)
    ftp.login()
    release_version = 0
    listing = [x.split("/").pop() for x in ftp.nlst(FTP_ROOT_DIR)]
    for file_ in listing:
        if file_.startswith(FTP_RELEASE_BASENAME):
            version = file_[len(FTP_RELEASE_BASENAME):]
            if version.isdigit():
                version = int(version)
                if version > release_version:
                    release_version = version
    if release_version:
        crawl_fasta(ftp,f"{FTP_ROOT_DIR}/{FTP_RELEASE_BASENAME}{release_version}{FTP_FASTA_DIR}")






def crawl_fasta(ftp,directory):
    listing = [x.split("/").pop() for x in ftp.nlst(directory)]
    for file_ in listing:
        if file_.endswith(FASTA_EXTENSION):
            print(f"{directory}/{file_}")
        elif "." not in file_ and file_ not in FTP_IGNORED_DIRS:
            crawl_fasta(ftp,directory + "/" + file_)






def crawl_gff3(ftp):
    pass
