"""
===========
SRA Helpers
===========

This module will write an sra.txt to each genome. sra.txt will contain a list
of accession numbers that are retrieved from a search using the corresponding
taxonomy id.


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

FETCH = ('https://eutils.ncbi.nlm.nih.gov'
         '/entrez/eutils/efetch.fcgi?db=sra&id=')


def build_sra_search(tax_id):
    """
    Builds the SRA search string based on an input taxonomy id number.
    An example search string:

    (((((txid39946[Organism:noexp]) AND "biomol rna"[Properties]) AND
    "illumina"[Platform]) AND "type rnaseq"[Filter])) AND 100:1000[ReadLength]

    """

    # Define discreet portions of the search string.
    tax_id_str = "txid{}[Organism:noexp]".format(tax_id)
    properties_str = 'biomol+rna[Properties]'
    platform_str = 'platform+illumina[Properties]'
    read_length_str = '100:1000[ReadLength]'
    layout_paired_str = '"paired"[Layout]'

    # Build the output string.
    out_str = '+AND+'.join((
        tax_id_str,
        properties_str,
        platform_str,
        read_length_str,
        layout_paired_str))

    return out_str


def run_sra_search(sra_query_str):
    """
    Runs the actual query.

    :param sra_query_str:
        A string that defines the desired search term.

    :returns:
        Eutils server response formatted as a dictionary.

    """

    # Build the query string, &retmax=100000 is the maximum number
    # of values that eutils will be return.
    query = QUERY + sra_query_str + "&retmax=100000"

    # Query the remote source and read the response.
    with urllib.request.urlopen(query) as response:
        response_xml = response.read()

    # Parse the returned XML and return the data as a dictionary.
    response = xmltodict.parse(response_xml)

    return response


def fetch_sra_info(sra_ID):
    """
    Retrieves the information associated with a response ID.

    :param sra_ID:
        A query ID returned by run_sra_search().

    """

    # Build the search string.
    fetch_str = FETCH + sra_ID

    # Query the remote source and save the response.
    with urllib.request.urlopen(fetch_str) as response:
        response_xml = response.read()

    # Parse the XML returned and return an dictionary.
    response = xmltodict.parse(response_xml)

    return response
