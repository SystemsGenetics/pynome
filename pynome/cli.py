"""This module contains the command line interface for Pynome.

.. module:: cli
    :platform: Unix
    :synopsis: This module contains the command line interface for
    Pynome.
"""

# General Python imports.
import click
from tqdm import tqdm
from irods.session import iRODSSession

# Inter-package imports.
from pynome.ensembldatabase import EnsemblDatabase
from pynome.assemblystorage import AssemblyStorage
from pynome.utils import read_json_config


@click.group(chain=True)
@click.pass_context
@click.option('--config', default='pynome_config.json', type=click.Path(exists=True))
def pynome(ctx, config):
    """
    This is the function which the command line invocation
    of pynome calls.

    The entry point to this command is created when program is installed
    with the setup.py file included.

    This function is run whenever a sub-command of it is called. Since
    all of these requre the database to be initialized, the code to do
    so is placed here.

    Read more in the click documentation:
    http://click.pocoo.org/5/commands/#callback-invocation
    """
    # Create a parent context object that can be passed to other cli functions.
    if ctx.obj is None:
        ctx.obj = dict()

    # Read the configuration file to get values for the databases.
    ctx.obj['config'] = read_json_config(config)

    # Initialize the instance of AssemblyStorage. Load either the variables
    # found in the configuration files, or `None` which will cause Pynome to
    # use the directory it was launched from to save files.
    # The dictionary.get() function is used here, as it returns `None` if the key
    # value pair is not found.
    ctx.obj['as'] = AssemblyStorage(
        sqlite_path=ctx.obj['config']["storage_config"].get("sqlite_path"),
        base_path=ctx.obj['config']["storage_config"].get("base_path"),
        irods_base_path=ctx.obj['config']["storage_config"].get("irods_base_path"),
    )

    # Initialize the databases.
    ctx.obj['ed'] = EnsemblDatabase(
        # Required values.
        name=ctx.obj['config']['ensembl_config']['name'],
        url=ctx.obj['config']['ensembl_config']['url'],
        description=ctx.obj['config']['ensembl_config']['description'],
        ignored_dirs=ctx.obj['config']['ensembl_config']['ignored_dirs'],
        data_types=ctx.obj['config']['ensembl_config']['data_types'],
        ftp_url=ctx.obj['config']['ensembl_config']['ftp_url'],
        kingdoms=ctx.obj['config']['ensembl_config']['kingdoms'],
        release_version=ctx.obj['config']['ensembl_config']['release_version'],
        bad_filenames=ctx.obj['config']['ensembl_config']['bad_filenames'],
        # Optional values. See above for .get() usage.
        crawl_urls=ctx.obj['config']['ensembl_config'].get('crawl_urls')
    )

    # Add the ensembl_database to the source list of assembly_storage.
    ctx.obj['as'].add_source(ctx.obj['ed'])


# Since it is bad form to redefine Python primatives, pass the
# `name` argument to the click command decorator, this prevents us
# from having to write `def list():`.
@pynome.command(name='list')
@click.pass_context
def list_assemblies(ctx):
    """List assemblies."""
    local_assemblies = [a for a in ctx.obj['as'].query_local_assemblies()]
    click.echo(
        click.style(
            f'Displaying {len(local_assemblies)} assemblies.', fg='green'))
    click.echo(local_assemblies)


@pynome.command()
@click.pass_context
def sra(ctx):
    """Download SRA metadata for each genome in the local sql database."""
    local_assemblies = [a for a in ctx.obj['as'].query_local_assemblies()]

    click.echo(
        click.style(
            f'Downloading {len(local_assemblies)} SRA files.', fg='green'))

    ctx.obj['as'].download_all_sra()


@pynome.command()
@click.pass_context
def download(ctx):
    """Download assembly files."""
    # Call the download_all() function of the AssemblyStorage class.
    ctx.obj['as'].download_all()

    # Download the SRA files.
    ctx.obj['as'].download_all_sra()


@pynome.command()
@click.pass_context
def prepare(ctx):
    """Prepare the downloaded files for further use."""

    for a in tqdm(ctx.obj['as'].query_local_assemblies(),
                  desc='Preparing assembly files.'):
        ctx.obj['as'].decompress(a)
        ctx.obj['as'].hisat_index(a)
        ctx.obj['as'].gtf(a)
        ctx.obj['as'].splice_site(a)


@pynome.command()
def push_irods():
    """Push all of the local genome files to an iRODs server."""
    # TODO: Look up irods pyton API to implement this function.


    pass


@pynome.command()
@click.pass_context
def discover(ctx):
    """Discover new genomes from a given source. If 'crawl_urls' are given
    in the configuration file, these will be used in place of any automatically
    generated urls.

    This will create the containing files and fill them with metadata.json
    files.
    """

    # Tell the user the crawl is starting, and what urls are to be examined.
    click.echo('Crawl of the Ensembl FTP server starting...')

    # Build a display of URI for the user to see.
    url_str = ctx.obj['config']['ensembl_config'].get('crawl_urls') \
        or ctx.obj['ed'].top_dirs
    url_str = '\n\t' + '\n\t'.join(url_str)

    click.echo(f'Begining a crawl at the following URIs: {url_str}')

    # Download the metadata file.
    click.echo('Downloading metadata file...')
    ctx.obj['ed'].download_metadata()

    # Crawl ensembl with either the given url list, or the autogenerated
    # complete list generated based on the config file.
    click.echo('Begining the main crawl...')
    ctx.obj['ed'].crawl(ctx.obj['config']['ensembl_config'].get('crawl_urls'))

    # Save those assemblies found.
    ctx.obj['as'].save_assemblies()

    # Get a list of all asemblies found by the crawl.
    assemblies = ctx.obj['as'].query_local_assemblies()
    click.echo(f'Crawl completed. Found {len(assemblies)} assemblies.')

    # Search for matching taxonomy IDs within the species.txt metadata file,
    # and update the assemblies with that information.
    click.echo('Mapping taxonomy id numbers to discovered assemblies.')
    tax_id_update = ctx.obj['ed'].add_taxonomy_ids(assemblies)

    # Save (update) each of these assembly ids.
    for pk, update_dict in tax_id_update:
        ctx.obj['as'].update_assembly(pk, update_dict)

    click.echo('Creating folders and writing .json metadata...')
    ctx.obj['as'].sources['ensembl'].write_metadata_jsons()

    # Report back to the user.
    click.echo('Discovery complete.')
