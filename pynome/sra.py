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
import collections
import xmltodict


# Define the query and fetch URL strings.
QUERY = ("https://eutils.ncbi.nlm.nih.gov"
         "/entrez/eutils/esearch.fcgi?db=sra&term=")

FETCH = ('https://eutils.ncbi.nlm.nih.gov'
         '/entrez/eutils/efetch.fcgi?db=sra&id=')


def download_sra_json(base_download_path, taxonomy_id_list):
    """
    Downloads the SRA metadata for each ID found in the
    `taxonomy_id_list`. These files are saved under a series of
    two-digit file  paths generated from the SRA accession number.

    :param base_download_path:
        The base location where the SRA accession number folders
        will be placed.
    :param taxonomy_id_list:
        A list of taxonomy identification values.
    :return:
        A list of success or failures, indexed the same as the
        input `taxonomy_id_list`.
    """

    # Create the output status dictionary to track whether a given
    # taxonomy ID was downloaded successfully or not.
    status_dict = collections.defaultdict(list)

    # For each of the taxonomy ID numbers provided.
    for tid in taxonomy_id_list:

        # Generate the corresponding query.
        query = build_sra_query_string(tid)

        # Run the query.
        query_response = run_sra_query(query)

        # Parse the response, get the list of SRA identification
        # numbers so that the corresponding metadata can be
        # downloaded.
        fetch_id_list = parse_sra_query_response(query_response)

        # If there are any accession values found.
        if fetch_id_list is not None:

            # Iterate through the fetch ID numbers.
            for fetch_id in fetch_id_list:

                # Get the desired *.json file associated with
                # the current fetch ID.
                fetch_result = fetch_sra_info(fetch_id)

                # Get the ERR or SRR from the fetched result. This
                # can be a list of values.
                SRA_accession_list = get_SRA_accession(fetch_result)

                for sra_id in SRA_accession_list:
                    # print('sra_id', sra_id)

                    # Create the broken up path.
                    sra_path = build_sra_path(sra_id)
                    # print(path)

                    path = os.path.join(base_download_path, sra_path, sra_id)

                    # Write the accession number to the output dictionary.
                    status_dict[tid].extend(sra_id)

                    # Create this path if it does not exist.
                    if not os.path.exists(path):
                        os.makedirs(path)

                    # Write the file.
                    with open(os.path.join(path, sra_id + '.sra.json'), 'w') as nfp:
                        nfp.write(json.dumps(fetch_result))

    # return status_dict


def get_SRA_accession(fetched_dict):
    """
    Reads an input dictionary, and returns either the ERR or SRR
    accession identification string.

    :param fetched_dict:
        A dictionary of SRA metadata from Eutils.

    :return:
        An list of accession identification strings.
    """

    # Return the accession number, in some cases there is a list of
    # runs. To handle this all inputs will be converted to a list.

    # Create the empty list that will be returned.
    sra_out_list = list()

    # Collect the runs from the dictionary.
    runs = (
        fetched_dict
        ['EXPERIMENT_PACKAGE_SET']
        ['EXPERIMENT_PACKAGE']
        ['RUN_SET']
        ['RUN'])

    # If this value is not a list, convert it into one.
    if type(runs) is not list:
        runs = [runs]

    # Iterate over the list of runs.
    for run in runs:

        # Get the accession identification string.
        sra_out_list.append(run['@accession'])

    return sra_out_list


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


def fetch_sra_info(fetch_id):
    """
    Retrieves the information associated with a response ID.
    The data returned by this function is that which will be
    saved within the `*.sra.json` file.

    :param fetch_id:
        A query ID returned by run_sra_search().

    :returns:
        An collections.OrderedDict object from the SRA archive.
    """

    # Build the search string.
    fetch_str = FETCH + fetch_id

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

    # The search result gives None if there are no IDs to return.
    if response['eSearchResult']['IdList'] is None:
        return None

    # Otherwise we should find at least one ID.
    elif response['eSearchResult']['IdList']['Id'] is not None:

        out_list = response['eSearchResult']['IdList']['Id']

        # Convert the value to a list if it is not already one.
        if type(out_list) is not list:
            out_list = [out_list]

        return out_list

    else:
        return None


def write_sra_json(sra_accession, base_path, sra_dict):
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

    # Use the retrieved accession number to build the SRA path.
    new_sra_path = build_sra_path(sra_accession)

    # Create the filename.
    new_file_name = sra_accession + '.sra.json'

    # Combine the base path, the sra_path and the new file name
    new_full_path = os.path.abspath(os.path.join(
        base_path, new_sra_path + new_file_name))

    # Write the file to the combined SRA and base path.
    with open(new_full_path, 'w') as nfp:
        nfp.write(json.dumps(sra_dict))


def build_sra_path(sra_id_str):
    """
    Builds an sra file path based on the `sra_id` parameter.

    The file structure built should be:

    ``
    RNA-Seq/
        SRA/
            [ES]RR/[0..9]/[0..9]/[0..9]/[0..9]/
                [ES]RR[#].sra.json
    ``

    :param sra_id_str:
        The accession number of an entry.

    :returns:
        A file path from `RNA-Seq/` to
        `[ES]RR/[0..9]/[0..9]/[0..9]/[0..9]/`.
    """

    # Get the sample accession number from sra_dict.
    chunked_id = chunk_accession_id(sra_id_str)

    # Create the directory path on the system if it
    # does not already exist.
    out_path = os.path.join(
        # 'RNA-Seq',
        'SRA',
        *chunked_id)

    # Return the intermediary path.
    return out_path


def chunk_accession_id(accession_id, chunk_size=2):
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

    # Check if an underscore exists in the ID, if so, remove the underscore
    # and all other trailing characters. These will not be used in the
    # construction of any filepaths.
    # Split after '_', one time, and return the first item in that
    # resulting list. If the separator is not present, the entire
    # string will be returned.
    sra_numbers = sra_numbers.split('_', 1)[0]

    # Create the output list, the first entry should be the letters.
    out_list = [sra_letters]

    # Iterate through the sra_numbers by the chunk_size.
    for i in range(0, len(sra_numbers), chunk_size):
        # Build the splice chunk.
        chunk = sra_numbers[i:i + chunk_size]
        # If the chunk is large enough, append it to the out_list.
        if len(chunk) == chunk_size:
            out_list.append(chunk)
        else:
            pass

    # Return the constructed list.
    return out_list
