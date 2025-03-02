#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""
@DATE: 2025-03-02 16:40:28
@File: PaperLoader/absloader.py
@IDE: vscode
@Description:
    抽象论文加载类
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from random import randrange
from typing import List


class AbPaperLoader(ABC):
    
    def __init__(self,filetype:str,api:str):
        self.api = api
        self.filetype = filetype
        pass
    
    @abstractmethod
    def read_paper(self):
        pass
    
    @abstractmethod
    def convert_paper(self):
        pass