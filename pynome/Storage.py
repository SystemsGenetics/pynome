# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod


class Storage(ABC):

    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def save_assembly(self, GenomeAssembly):
        pass
