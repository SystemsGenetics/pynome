"""
===========
SRA Helpers
===========

This module will write an sra.txt to each genome. sra.txt will contain a list
of accession numbers that are retrieved from a search using the corresponding
taxonomy id.

The functions defined here use **eutils**. For more information refer to the
`documentation <https://www.ncbi.nlm.nih.gov/books/NBK25499/>`.

**Sample Search String**:

``(((((txid39946[Organism:noexp]) AND "biomol rna"[Properties]) AND
"illumina"[Platform]) AND "type rnaseq"[Filter])) AND 100:1000[ReadLength]``

---------------
Filter criteria
---------------

**Implemented Features**

#. RNA-SEQ assays.
#. Illumina platform.
#. Paired reads.
#. A base pair read length from 100 to 1000.

"""

import os
import json
import urllib
import xmltodict

# Define the query and fetch URL strings.
QUERY = ("https://eutils.ncbi.nlm.nih.gov"
         "/entrez/eutils/esearch.fcgi?db=sra&term=")

FETCH = ('https://eutils.ncbi.nlm.nih.gov'
         '/entrez/eutils/efetch.fcgi?db=sra&id=')


def build_sra_query_string(tax_id):
    """
    Builds the SRA search string based on an input taxonomy id number.
    """

    # Place tax_id in a wrapper string to identify it as a taxonomy ID.
    tax_id_str = "txid{}[Organism:noexp]".format(tax_id)

    # Define discreet portions of the search string.
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


def run_sra_query(sra_query_str):
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


def fetch_sra_info(sra_id):
    """
    Retrieves the information associated with a response ID.

    ..todo::
        Confirm that the XML returned by this function is the
        `*.sra.json` file as outlined in the project notes.

    :param sra_id:
        A query ID returned by run_sra_search().

    :returns:
        An collections.OrderedDict object from the SRA archive.
    """

    # Build the search string.
    fetch_str = FETCH + sra_id

    # Query the remote source and save the response.
    with urllib.request.urlopen(fetch_str) as response:
        response_xml = response.read()

    # Parse the XML returned and return an dictionary.
    response = xmltodict.parse(response_xml)

    return response


def parse_sra_query_response(response):
    """
    Parses an OrderedDict response object, as retrieved
    from `fetch_sra_info`.

    The desired fetch IDs are in the nested list:

    ``response['eSearchResult']['IdList']['Id']``

    :returns:
        A list of fetch IDs.

    """

    # Return correct list from the response if it exists,
    # otherwise return `None`.
    if response['eSearchResult']['IdList']['Id'] is not None:
        return response['eSearchResult']['IdList']['Id']
    else:
        return None


def write_sra_json(base_path, sra_dict):
    """
    Creates an `"[sra_id].sra.json"` file and saves it to the
    supplied directory.

    The accession number is found within sra_dict.

    ``['EXPERIMENT_PACKAGE_SET']['EXPERIMENT_PACKAGE']
      ['SAMPLE']['@accession']``

    There are three other keys at the `'SAMPLE'` level that have
    `[@accession]` entries: `'EXPERIMENT', 'SUBMISSION', 'STUDY'`.

    :param base_path:
        The complete path to save write the file to.

    :param sra_dict:
        The response XML to save.
    """

    # Get the accession number from sra_dict.
    accession_number = sra_dict['EXPERIMENT_PACKAGE_SET']
    ['EXPERIMENT_PACKAGE']['SAMPLE']['@accession']

    # Use the retrieved accession number to build the SRA path.
    new_sra_path = build_sra_path(accession_number)

    # Create the filename.
    new_file_name = accession_number + '.sra.json'

    # Combine the base path, the sra_path and the new file name
    new_full_path = os.path.abspath(os.path.join(
        base_path, new_sra_path + new_file_name))

    # Write the file to the combined SRA and base path.
    with open(new_full_path, 'w') as nfp:
        nfp.write(json.dumps(sra_dict))


def build_sra_path(sra_dict):
    """
    Builds an sra file path based on the `sra_id` parameter.

    The file structure built should be:

    ``
    RNA-Seq/
        SRA/
            [ES]RR/[0..9]/[0..9]/[0..9]/[0..9]/
                [ES]RR[#].sra.json
    ``

    The accession number is found within sra_dict.

    ``['EXPERIMENT_PACKAGE_SET']['EXPERIMENT_PACKAGE']
      ['SAMPLE']['@accession']``

    :param sra_dict:
        The accession number of an entry.

    :returns:
        A file path from `RNA-Seq/` to
        `[ES]RR/[0..9]/[0..9]/[0..9]/[0..9]/`.
    """

    # Get the sample accession number from sra_dict.
    accession_ID = sra_dict['EXPERIMENT_PACKAGE_SET']
    ['EXPERIMENT_PACKAGE']['SAMPLE']['@accession']

    # Break the SRA ID into chunks, and construct the path.
    chunk_list = chunk_accession_id(accession_ID, chunk_size=2)

    out_path = os.path.join(
        'RNA-Seq',
        'SRA',
        chunk_list,
    )

    # Return the intermediary path.
    return out_path


def chunk_accession_id(accession_id, chunk_size):
    """
    Breaks an accession id into chunks of `chunk_size` and returns a
    list of all chunks in order that are full-sized.

    :param accession_id:
        The SRA accession id that is to be broken into chunks.

    :param chunk_size:
        The desired (and minimum) size of chunks to be returned.

    :return:
        A list of chunks of minimum length `chunk_size`.
    """

    # Split the leading three letters from the numbers.
    sra_letters = accession_id[0:3]

    # Assign the remaining numbers.
    sra_numbers = accession_id[3:]

    # Create the output list, the first entry should be the letters.
    out_list = [sra_letters]

    # Iterate through the sra_numbers by the chunk_size.
    for i in range(0, len(sra_numbers), chunk_size):
        # Build the splice chunk.
        chunk = sra_numbers[i:i + chunk_size]
        # If the chunk is large enough, append it to the out_list.
        if len(chunk) < chunk_size:
            out_list.append(chunk)
        else:
            pass

    # Return the constructed list.
    return out_list
