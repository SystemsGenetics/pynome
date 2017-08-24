"""
===========
SRA Helpers
===========


This module will provide tools that will extract the accession numbers from
the metadata file, ``species.txt``.

This module works by examining ``species.txt`` as a pandas data frame. It has
the following columns.

    #name
    species
    division
    **taxonomy_id** <-- The one we are interested in.
    assembly
    assembly_accession
    genebuild
    variation
    pan_compara
    peptide_compara
    genome_alignments
    other_alignments
    core_db
    species_id

"""
