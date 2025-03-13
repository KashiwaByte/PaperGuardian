#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""
@DATE: 2025-03-13 20:39:01
@File: FormatDetection/FormatChecker.py
@IDE: vscode
@Description:
    格式检测器
"""


from docx import Document
from docx.shared import Inches
import re



def fuzzy_match(text, target):
    """
    使用正则表达式进行模糊匹配。

    Args:
        text: 要匹配的文本。
        target: 目标字符串。

    Returns:
        如果匹配成功则返回True，否则返回False。
    """
    pattern = r"\s*".join(list(target))  # 将目标字符串转换为正则表达式模式，允许空格
    match = re.search(pattern, text)
    return bool(match)

class FormatChecker:
    def __init__(self,filetype,filepath):
        self.filetype = filetype
        self.filepath = filepath
        self.doc = Document(filepath)
        self.cover_page = self.doc.paragraphs 
        self.total_paragraphs = len(self.cover_page)
        self.extracted_info = {}
        print(f"段落总数为{self.total_paragraphs}")
        pass
    
    def chunk_match(self,target_content,need_times=1):

        i = 0
        times = 0 
        found = False
        while not found:
            content = self.cover_page[i].text #  你需要自己实现这个函数

            if fuzzy_match(content, target_content):
                times+=1
                if times == need_times:
                    found = True
                    print(f"匹配到固定内容 '{target_content}'，计数器值为: {i}")
                else:
                    i += 1
            else:
                i += 1
        
        return i
    
    
    def check_cover_page(self):
        
        need_times = 1     # 匹配到第一次为目录，第二次才是具体章节
        target_content = "摘要"  # 替换为你的固定内容


        self.end_paragraph = self.chunk_match(target_content,need_times)


        for i in range(self.end_paragraph): #封面页有30个段落
            if self.cover_page[i].text == "":
                pass
            else:
                print(self.cover_page[i].text)
                return self.cover_page[i].text
    
    def check_abstract(self):
        
        need_times = 1     # 匹配到第一次为目录，第二次才是具体章节
        target_content = "目录"  # 替换为你的固定内容

        self.begin_paragraph = self.end_paragraph
        self.end_paragraph = self.chunk_match(target_content,need_times)

        for i in range(self.begin_paragraph,self.end_paragraph): #封面页有30个段落
            if self.cover_page[i].text == "":
                pass
            else:
                print(self.cover_page[i].text)
                return self.cover_page[i].text
    
    def check_table_of_contents(self):  
        
        need_times = 2     # 匹配到第一次为目录，第二次才是具体章节
        target_content = "第一章"  # 替换为你的固定内容

        self.begin_paragraph = self.end_paragraph
        self.end_paragraph = self.chunk_match(target_content,need_times)

        for i in range(self.begin_paragraph,self.end_paragraph): #封面页有30个段落
            if self.cover_page[i].text == "":
                pass
            else:
                print(self.cover_page[i].text)
                return self.cover_page[i].text
            
    
    def check_chapter_titles(self):
        pass
    
    def check_page_header(self):
        pass
    
    def check_page_footer(self):
        pass
    
    def check_body(self):
        need_times = 2     # 匹配到第一次为目录，第二次才是具体章节
        target_content = "参考文献"  # 替换为你的固定内容

        self.begin_paragraph = self.end_paragraph
        self.end_paragraph = self.chunk_match(target_content,need_times)

        for i in range(self.begin_paragraph,self.end_paragraph): #封面页有30个段落
            if self.cover_page[i].text == "":
                pass
            else:
                print(self.cover_page[i].text)
                return self.cover_page[i].text
    
    def check_references(self):
        self.begin_paragraph = self.end_paragraph

        for i in range(self.begin_paragraph,self.total_paragraphs): #封面页有30个段落
            if self.cover_page[i].text == "":
                pass
            else:
                print(self.cover_page[i].text)
    

    
    
    
    def check_format(self):
        # 检查封面页
        self.check_cover_page()
        # 检查声明与摘要
        self.check_abstract()
        # 检查目录
        self.check_table_of_contents()
        # 检查章节标题
        self.check_chapter_titles()
        # 检查页眉
        self.check_page_header()
        # 检查页脚
        self.check_page_footer()
        # 检查正文
        self.check_body()
        # 检查参考文献
        self.check_references()
        # 检查附录
        self.check_appendix()
        pass
    
    