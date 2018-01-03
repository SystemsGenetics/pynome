# -*- coding: utf-8 -*-


class GenomeAssembly:
    """
    This models a Genome Assembly.
    """

    def __init__(self, **kwargs):
        """
        Creates a new GenomeAssembly instances.

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
        # Define public attributes, these can be directly set.
        self.species = None
        self.assembly_name = None
        self.genus = None
        self.taxonomy_id = None
        self.intraspecific_name = None

        # Define private attributes, these cannot be directly assigned.
        # Instead they are constructed from the above attributes at the
        # whenever they are requested.
        self._taxonomic_name = None
        self._base_filename = None

        # Iterate through the kwargs parameter and set the key: value
        # pairs to the attributes.
        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def taxonomic_name(self):
        """
        The 'getter' of the taxonomic name of the genome assembly. This
        property is constructed with the genus, species and intraspecific
        name, if it exists.
        """
        # Check if the intraspecific name is populated.
        if self.intraspecific_name is not None:
            # Construct the taxonomic_name from other attributes.
            return '_'.join(
                [self.genus, self.species, self.intraspecific_name])
        # Otherwise, simply return the genus and species separated by an '_'.
        else:
            return '_'.join([self.genus, self.species])

    @property
    def base_filename(self):
        """
        The 'getter' of the base filename of the genome assembly.
        """
        # Check if the intraspecific name is populated.
        if self.intraspecific_name is not None:
            # Construct the base_filename from other attributes.
            return ''.join([
                self.genus, '_',
                self.species, '_',
                self.intraspecific_name, '-',
                self.assembly_name])
        else:
            return ''.join([
                self.genus, '_',
                self.species, '-',
                self.assembly_name])

    def __str__(self):
        return str(self.taxonomic_name)
