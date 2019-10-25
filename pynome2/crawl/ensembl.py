from ..assembly import register_crawler

# For FASTA files: they ALWAYS end in *.toplevel.fa.gz
# Found in http://ftp.ensemblorg.ebi.ac.uk/pub/release-92/fasta/

# For GFF3 files: they ALWAYS end in *.92.gff3.gz
# Found in http://ftp.ensemblorg.ebi.ac.uk/pub/release-92/gff3/






@register_crawler("ensemble")
def crawl():
    pass






def crawl_fasta():
    pass






def crawl_gff3():
    pass
