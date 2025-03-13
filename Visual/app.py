#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""
@DATE: 2025-02-27 20:05:10
@File: Visual/app.py
@IDE: vscode
@Description: 
    论文可视化启动文件
"""
import os
from re import T
import sys
import json
from tkinter.tix import Tree
import gradio as gr
from dotenv import load_dotenv
# import spaces
from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer


current_path = os.path.abspath(__file__)
parent_path = os.path.dirname(current_path)
sys_path = os.path.dirname(parent_path)
sys.path.append(sys_path)
from PeerReview import Reviewer
from PaperLoader import PdfPaperLoader,  WordPaperLoader



load_dotenv()
marker_api = os.getenv("MARKER")
qwen_api = os.getenv("DASHSCOPE_API_KEY")


# Define prompts
SYSTEM_PROMPT_TEMPLATE = """You are an expert reviewer for AI conferences. You follow best practices and review papers according to the reviewer guidelines.
Reviewer guidelines:
1. Read the paper: It’s important to carefully read through the entire paper, and to look up any related work and citations that will help you comprehensively evaluate it. Be sure to give yourself sufficient time for this step.
2. While reading, consider the following:
    - Objective of the work: What is the goal of the paper? Is it to better address a known application or problem, draw attention to a new application or problem, or to introduce and/or explain a new theoretical finding? A combination of these? Different objectives will require different considerations as to potential value and impact.
    - Strong points: is the submission clear, technically correct, experimentally rigorous, reproducible, does it present novel findings (e.g. theoretically, algorithmically, etc.)?
    - Weak points: is it weak in any of the aspects listed in b.?
    - Be mindful of potential biases and try to be open-minded about the value and interest a paper can hold for the community, even if it may not be very interesting for you.
3. Answer four key questions for yourself, to make a recommendation to Accept or Reject:
    - What is the specific question and/or problem tackled by the paper?
    - Is the approach well motivated, including being well-placed in the literature?
    - Does the paper support the claims? This includes determining if results, whether theoretical or empirical, are correct and if they are scientifically rigorous.
    - What is the significance of the work? Does it contribute new knowledge and sufficient value to the community? Note, this does not necessarily require state-of-the-art results. Submissions bring value to the community when they convincingly demonstrate new, relevant, impactful knowledge (incl., empirical, theoretical, for practitioners, etc).
4. Write your review including the following information: 
    - Summarize what the paper claims to contribute. Be positive and constructive.
    - List strong and weak points of the paper. Be as comprehensive as possible.
    - Clearly state your initial recommendation (accept or reject) with one or two key reasons for this choice.
    - Provide supporting arguments for your recommendation.
    - Ask questions you would like answered by the authors to help you clarify your understanding of the paper and provide the additional evidence you need to be confident in your assessment.
    - Provide additional feedback with the aim to improve the paper. Make it clear that these points are here to help, and not necessarily part of your decision assessment.
Your write reviews in markdown format. Your reviews contain the following sections:
# Review
{review_fields}
Your response must only contain the review in markdown format with sections as defined above.
"""

USER_PROMPT_TEMPLATE = """Review the following paper:
{paper_text}
"""

# For now, use fixed review fields
REVIEW_FIELDS = """## Summary
Briefly summarize the paper and its contributions. This is not the place to critique the paper; the authors should generally agree with a well-written summary.
## Soundness
Please assign the paper a numerical rating on the following scale to indicate the soundness of the technical claims, experimental and research methodology and on whether the central claims of the paper are adequately supported with evidence. Choose from the following:
4: excellent
3: good
2: fair
1: poor
## Presentation
Please assign the paper a numerical rating on the following scale to indicate the quality of the presentation. This should take into account the writing style and clarity, as well as contextualization relative to prior work. Choose from the following:
4: excellent
3: good
2: fair
1: poor
## Contribution
Please assign the paper a numerical rating on the following scale to indicate the quality of the overall contribution this paper makes to the research area being studied. Are the questions being asked important? Does the paper bring a significant originality of ideas and/or execution? Are the results valuable to share with the broader ICLR community? Choose from the following:
4: excellent
3: good
2: fair
1: poor
## Strengths
A substantive assessment of the strengths of the paper, touching on each of the following dimensions: originality, quality, clarity, and significance. We encourage reviewers to be broad in their definitions of originality and significance. For example, originality may arise from a new definition or problem formulation, creative combinations of existing ideas, application to a new domain, or removing limitations from prior results.
## Weaknesses
A substantive assessment of the weaknesses of the paper. Focus on constructive and actionable insights on how the work could improve towards its stated goals. Be specific, avoid generic remarks. For example, if you believe the contribution lacks novelty, provide references and an explanation as evidence; if you believe experiments are insufficient, explain why and exactly what is missing, etc.
## Questions
Please list up and carefully describe any questions and suggestions for the authors. Think of the things where a response from the author can change your opinion, clarify a confusion or address a limitation. This is important for a productive rebuttal and discussion phase with the authors.
## Flag For Ethics Review
If there are ethical issues with this paper, please flag the paper for an ethics review and select area of expertise that would be most useful for the ethics reviewer to have. Please select all that apply. Choose from the following:
No ethics review needed.
Yes, Discrimination / bias / fairness concerns
Yes, Privacy, security and safety
Yes, Legal compliance (e.g., GDPR, copyright, terms of use)
Yes, Potentially harmful insights, methodologies and applications
Yes, Responsible research practice (e.g., human subjects, data release)
Yes, Research integrity issues (e.g., plagiarism, dual submission)
Yes, Unprofessional behaviors (e.g., unprofessional exchange between authors and reviewers)
Yes, Other reasons (please specify below)
## Details Of Ethics Concerns
Please provide details of your concerns.
## Rating
Please provide an "overall score" for this submission. Choose from the following:
1: strong reject
3: reject, not good enough
5: marginally below the acceptance threshold
6: marginally above the acceptance threshold
8: accept, good paper
10: strong accept, should be highlighted at the conference
"""



# functions


def convert_file(filepath):
    marker_api = os.getenv("MARKER")
    qwen_api = os.getenv("DASHSCOPE_API_KEY")
    loader = PdfPaperLoader(marker_api)
    filename = filepath.split("/")[-1]
    loader.read_paper(filepath,filename)
    output = loader.convert_paper(vlapi=qwen_api,lang="Chinese")
    return output
    



def generate(paper_text, review_style):
    reviewer = Reviewer(qwen_api, "qwen-plus")
    completion = reviewer.read_paper(paper_text,style=review_style,stream=True)
    generated_text = ""
    for chunk in completion:
        data = json.loads(chunk.model_dump_json())
        current_content = data["choices"][0]["delta"].get("content", "")
        generated_text += current_content
        yield generated_text




# ui
#8C1B13 red
#4D8093 blue
#767676 med grey
#EFECE3 light grey
#DDDDDD silver below red
#FFFDFA white

title = """<h1 align="center">PaperGuardian</h1>
<div align="center">Using <a href="https://github.com/KashiwaByte/PaperGuardian" target="_blank"><code>PaperGuardian</code></a> - Built by Kashiwa</div>
"""

description = """这是一个在线演示，展示的是 PaperGuardian，这是一个论文评审系统，能够为本科毕设和学术论文生成格式评审与高质量的内容评审。
## 演示指南
1.以 PDF或word 文件形式上传你的论文。我们不会存储你的数据。用户数据仅在处理过程中临时存储。  
2.一旦你上传了文件，它将被转换为 Markdown 格式。这需要一些时间，因为系统会运行多个变换器模型来解析页面布局并提取文本和表格。详情请查看 [marker](https://github.com/VikParuchuri/marker/tree/master)。  
3.在获得论文的 Markdown 版本后，你现在可以点击 “生成评审意见”。  
4.我们目前只支持生成内容评审意见，后续将集成格式评审意见。  
5.查看评审模板，以便正确解读生成的评审意见。如果你想以不同的架构和方面生成评审意见，也可以在生成之前更改评审模板。  
6.若要获得多份评审意见，只需再次点击生成即可。  
"""



theme = gr.Theme.from_hub("hmb/amethyst")
# theme = gr.themes.Default(primary_hue="gray", secondary_hue="blue", neutral_hue="slate")
with gr.Blocks(theme=theme) as demo:
    title = gr.HTML(title)
    description = gr.Markdown(description)
    with gr.Tab("内容评审"):
        file_input = gr.File(file_types=[".pdf",".docx"], file_count="single")
        paper_text_field= gr.Textbox("上传PDF或Word文件或粘贴论文的 Markdown 格式全文。", label="Paper Text", lines=20, max_lines=20, autoscroll=False,show_copy_button=True)
        review_style =  gr.Dropdown(
                ["Formal", "Encouraging", "Sharp","Academic"], label="评审风格", info="请选择你需要的评审风格")
        # with gr.Accordion("评审模版", open=False):
        #     review_template_description = gr.Markdown("我们目前提供多种评审模版，你也可以根据需要在下方自行修改")
        #     review_template_field = gr.Textbox(label=" ",lines=20, max_lines=20, autoscroll=False, value=REVIEW_FIELDS)
        generate_button = gr.Button("生成评审意见", interactive=not paper_text_field)
        review_field = gr.Markdown("""<h1 align="center">评审意见</h1>""", label="评审意见",show_copy_button=True,container=True,show_label=True,max_height=10000)

        file_input.upload(convert_file, file_input, paper_text_field)
        paper_text_field.change(lambda text: gr.update(interactive=True) if len(text) > 200 else gr.update(interactive=False), paper_text_field, generate_button)
        generate_button.click(fn=generate, inputs=[paper_text_field, review_style], outputs=review_field)
        # generate_button.click(fn=lambda: gr.update(interactive=False), inputs=None, outputs=generate_button).then(generate, [paper_text_field, review_template_field], review_field).then(fn=lambda: gr.update(interactive=True), inputs=None, outputs=generate_button)

    with gr.Tab("格式评审"):
        format_file_input = gr.File(file_types=[".pdf",".docx"], file_count="single")
        format_paper_text_field= gr.Textbox("上传PDF", label="Paper Text", lines=20, max_lines=20, autoscroll=False,show_copy_button=True)

    demo.title = "PaperGuardian"




if __name__ == "__main__":
    demo.queue()
    demo.launch(share=True)

