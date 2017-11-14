"""
===========
SRA Helpers
===========

This module will write an sra.txt to each genome. sra.txt will contain a list
of accession numbers that are retrieved from a search using the corresponding
taxonomy id.


Filter criteria:

Filter criteria:

1)  read length >= 100bp
2)  # of spots (reads): 10 Million
3)  PAIRED reads only
4)  Species with genome and GFF3 file.
5)  Illumina sequencers.
6)  Assay Type: RNA-Seq

https://www.ncbi.nlm.nih.gov/books/NBK25499/
"""

import urllib
import xmltodict


QUERY = ("https://eutils.ncbi.nlm.nih.gov"
         "/entrez/eutils/esearch.fcgi?db=sra&term=")


def build_sra_search_string(tax_ID):
        """
        Builds an SRA search string based on a taxonomy ID number.
        The search string is built to work with Eutils, and searches
        the SRA database and returns a list of SRA accession numbers.

        :param tax_ID: The taxonomy ID of a species.
        :returns: A string built from the taxonomy ID.

        Example::
            (((((txid39946[Organism:noexp]) AND "biomol rna"[Properties])
            AND "illumina"[Platform]) AND "type rnaseq"[Filter])) AND
            100:1000[ReadLength]
        """

        tax_id_str = "txid{0}[Organism:noexp]".format(tax_ID)
        properties_str = 'biomol+rna[Properties]'
        platform_str = 'platform+illumina[Properties]'
        read_length_str = '100:1000[ReadLength]'
        layout_paired_str = '"paired"[Layout]'

        return '+AND+'.join((tax_id_str, properties_str, platform_str,
                             read_length_str, layout_paired_str))


def run_sra_search(sra_term):
    """
    Runs the actual SRA query.
    :param
    """
    # &retmax= sets the maximum number of retrivable terms.
    # the value 100000 is the maximum allowed.
    query = QUERY + sra_term + "&retmax=100000"
    with urllib.request.urlopen(query) as response:
        response_xml = response.read()

    response = xmltodict.parse(response_xml)
    retr_id_l = response['eSearchResult']['IdList']['Id']

    return retr_id_l
