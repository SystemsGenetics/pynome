# -*- coding: utf-8 -*-


class GenomeAssembly:

    def __init__(self, taxonomic_name, **kwargs):
        """
        Creates a new GenomeAssembly instances.

        :param taxonomic_name:
          The taxonomic name of the species that the assembly belongs to.

        :param kwargs:
          A list of key/value pairs defining the genome assembly.  The
          available keys are:
           - taxonomic_name:
           - species: The species name.
           - assembly_name: The name of the assembly.
           - genus: The genus of the assembly.
           - taxonomy_id: The numerical taxonomy identifier.
           - intraspecific_name: The intra-specific name of a given entry.

           - fasta_uri: The fa.gz url as a String.
           - fasta_size: The remote size of the fa.gz file as an Integer.
           - gff3_uri: The gff3.gz uri as a String.
           - gff3_size: The remote size of the gff3.gz file as an Integer.

           - local_path: The local path of this genome as a String.
           - base_filename: The filename base for this genome item entry.
             [genus]_[species]{_[infraspecific name]}-[assembly_name]

        :Examples:

        An instance of this class should be created whenever a genome entry
        needs to be created or modified.

            >>> newGenome = GenomeAssembly([taxonomic_name], **kwargs)

        """

        # Iterater through the kwargs parameter and set the SQLAlchemy
        # table columns accordingly.
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        return str(self.taxonomic_name)

    # def save(self):
    #     self.storage.save()
