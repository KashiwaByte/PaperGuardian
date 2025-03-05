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
from os import name
import time
import requests
import concurrent.futures
from openai import OpenAI
import re

class WordPaperLoader(AbPaperLoader):
    def __init__(self, api: str, filetype: str = "docx"):
        super().__init__(filetype=filetype, api=api)
        

    def read_paper(self,filepath,filename):
        self.filepath = filepath
        self.filename = filename
        

    
    def convert_paper(self,vlapi,output_type:str="markdown",lang:str="English"):
        print(f"Converting paper: \n Type:{self.filetype} \n Path:{self.filepath} \n Name:{self.filename} \n Language: {lang}  \n Output_Type {output_type} ")
        self.output_type = output_type
        self.lang = lang
        self.vlapi = vlapi
        self.image_understand_dict = {}
        
        request_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        url = "https://www.datalab.to/api/v1/marker"
        
        form_data = {
            'file': (self.filename, open(self.filepath, 'rb'), request_type),
            'langs': (None, lang),
            "force_ocr": (None, False),
            "paginate": (None, False),
            'output_format': (None, self.output_type),
            "use_llm": (None, False),
            "strip_existing_ocr": (None, False),
            "disable_image_extraction": (None, False)
        }

        headers = {"X-Api-Key": self.api}

        response = requests.post(url, files=form_data, headers=headers)
        data = response.json()

        max_polls = 300
        check_url = data["request_check_url"]

        for i in range(max_polls):
            time.sleep(2)
            response = requests.get(check_url, headers=headers) # Don't forget to send the auth headers
            output = response.json()

            
            if output["status"] == "complete":
                break
        
        print("Text extracted,Begin to understand images")
        
        self.images = {}
        for key, value in output["images"].items():
            self.images[key] = value 
            
        with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
            executor.map(self.image_understand,self.images.keys(), self.images.values())
        
        converted_content= self.replace_image_tags(output[self.output_type])
            
        return converted_content
    
    
    
    def image_understand(self,key,value):
        base64_image = value
        client = OpenAI(
            # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
            api_key=self.vlapi,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        completion = client.chat.completions.create(
            model="qwen-vl-plus-latest",
            messages=[
                {
                    "role": "system",
                    "content": [{"type":"text","text": "你是一个科研论文评审专家，现在需要评审一篇论文，请理解下图，并输出整段段内容。"}]},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            # 需要注意，传入Base64，图像格式（即image/{format}）需要与支持的图片列表中的Content Type保持一致。"f"是字符串格式化的方法。
                            # PNG图像：  f"data:image/png;base64,{base64_image}"
                            # JPEG图像： f"data:image/jpeg;base64,{base64_image}"
                            # WEBP图像： f"data:image/webp;base64,{base64_image}"
                            "image_url": {"url": f"data:image/png;base64,{base64_image}"}, 
                        },
                        {"type": "text", "text": "图中描述了什么，请输出一整段内容?"},
                    ],
                }
            ],
        )
        self.image_understand_dict[key] = completion.choices[0].message.content
        print(completion.choices[0].message.content)
    
    def replace_image_tags(self,text):
        # 定义正则表达式来匹配图片标记
        pattern = r'!\[\]\((.*?)\)'
        # 查找所有匹配的图片标记
        matches = re.findall(pattern, text)
        for match in matches:
            image_path = match
            print(self.image_understand_dict.keys())
            image_text = self.image_understand_dict[match] 
            print(f"{image_path}:{image_text}")
            # 替换图片标记为图片中的文本
            text = text.replace(f"![]({image_path})", f"(此处有图片)，内容为{image_text} 名称为:")
        return text
    
    
    

if __name__ == "__main__":
    loader = WordPaperLoader("word")
    