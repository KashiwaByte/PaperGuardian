#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""
@DATE: 2025-03-02 16:47:53
@File: PaperLoader/wordloader.py
@IDE: vscode
@Description:
    Word论文加载类
"""

from unittest import loader
from .absloader import AbPaperLoader


class WordPaperLoader(AbPaperLoader):
    def __init__(self, api: str, filetype: str = "docx"):
        super().__init__(filetype=filetype, api=api)
        
    def read_paper(self):
        pass        
    
    def convert_paper():
        pass
    
    
    

if __name__ == "__main__":
    loader = WordPaperLoader("word")
    