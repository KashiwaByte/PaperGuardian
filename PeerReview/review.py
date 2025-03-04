#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""
@DATE: 2025-03-04 15:42:13
@File: PeerReview/review.py
@IDE: vscode
@Description:
    评审类
"""
import os
import sys
from openai import OpenAI
from prompt import PROMPT_DICT

class Reviewer:
    
    def __init__(self, api, model):
        """_summary_

        Args:
            api (_type_): _description_   LLM模型的API  
            model (_type_): _description_ 选用的LLM模型
        """
        self.api = api
        self.model = model
        self.client = OpenAI(
            api_key=self.api,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        
    def read_paper(self, paper, external_knowledge=None, style='Formal'):
        # 定义允许的风格列表
        allowed_styles = ['Formal', 'Encouraging', 'Sharp', 'Academic']
        # 检查传入的 style 是否在允许的风格列表中
        if style not in allowed_styles:
            raise ValueError(f"Invalid style. Allowed styles are {', '.join(allowed_styles)}.")
        
        system_prompt = PROMPT_DICT[style]
        content = paper
        if external_knowledge:
            content += f"请参考相关资料辅助评价论文，以下是这篇论文的相关资料:{external_knowledge}"
        completion = self.client.chat.completions.create(

                    model=self.model, 
                    messages=[
                        {'role': 'system', 'content': system_prompt},
                        {'role': 'user', 'content': content}],
                    stream=True,
                    stream_options={"include_usage": False}
                )
        for chunk in completion:
            print(chunk.model_dump_json())
    

    
    
    

if __name__ == "__main__":
    print(PROMPT_DICT.keys())
    print(PROMPT_DICT["Sharp"])
