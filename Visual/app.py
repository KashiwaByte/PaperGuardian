#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""
@DATE: 2025-02-27 20:05:10
@File: Visual/app.py
@IDE: vscode
@Description: 
    论文可视化启动文件
"""
import gradio as gr
# import spaces
from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer
# import torch
from threading import Thread


import traceback



metadata = {}

# # prepare LLM
# model_name = "maxidl/Llama-OpenReviewer-8B"
# model = AutoModelForCausalLM.from_pretrained(
#     model_name,
#     torch_dtype=torch.bfloat16,
#     device_map="auto"
# )
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# streamer = TextIteratorStreamer(tokenizer, skip_prompt=True, decode_kwargs=dict(skip_special_tokens=True))

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
def create_messages(review_fields, paper_text):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT_TEMPLATE.format(review_fields=review_fields)},
        {"role": "user", "content": USER_PROMPT_TEMPLATE.format(paper_text=paper_text)},
    ]
    return messages


def convert_file(filepath):
    pass

def process_file(file):
    pass


def generate(paper_text, review_template):
    pass
    # messages = create_messages(review_template, paper_text)
    # input_ids = tokenizer.apply_chat_template(
    #     messages,
    #     add_generation_prompt=True,
    #     return_tensors='pt'
    # ).to(model.device)
    # print(f"input_ids shape: {input_ids.shape}")
    # generation_kwargs = dict(input_ids=input_ids, streamer=streamer, max_new_tokens=4096, do_sample=True, temperature=0.6, top_p=0.9)
    # thread = Thread(target=model.generate, kwargs=generation_kwargs)
    # thread.start()
    # generated_text = ""
    # for new_text in streamer:
    #     generated_text += new_text
    #     yield generated_text.replace("<|eot_id|>", "")



# ui
#8C1B13 red
#4D8093 blue
#767676 med grey
#EFECE3 light grey
#DDDDDD silver below red
#FFFDFA white

title = """<h1 align="center">OpenReviewer</h1>
<div align="center">Using <a href="https://huggingface.co/maxidl/Llama-OpenReviewer-8B" target="_blank"><code>Llama-OpenReviewer-8B</code></a> - Built with Llama</div>
"""

description = """This is an online demo featuring [Llama-OpenReviewer-8B](https://huggingface.co/maxidl/Llama-OpenReviewer-8B), a large language model that generates high-quality reviews for machine learning and AI papers.
## Demo Guidelines
1. Upload you paper as a pdf file. Alternatively you can paste the full text of your paper in markdown format below. We do **not** store your data. User data is kept in ephemeral storage during processing.
2. Once you upload a pdf it will be converted to markdown. This takes some time as it runs multiple transformer models to parse the layout and extract text and tables. Checkout [marker](https://github.com/VikParuchuri/marker/tree/master) for details.
3. Having obtained a markdown version of your paper, you can now click *Generate Review*.
Take a look at the Review Template to properly interpret the generated review. You can also change the review template before generating in case you want to generate a review with a different schema and aspects.
To obtain more than one review, just generate again.
**GPU quota:** If exceeded, either sign in with your HF account or come back later. Your quota has a half-life of 2 hours.
"""

theme = gr.themes.Default(primary_hue="gray", secondary_hue="blue", neutral_hue="slate")
with gr.Blocks(theme=theme) as demo:
    title = gr.HTML(title)
    description = gr.Markdown(description)
    file_input = gr.File(file_types=[".pdf"], file_count="single")
    paper_text_field= gr.Textbox("Upload a pdf or paste the full text of your paper in markdown format here.", label="Paper Text", lines=20, max_lines=20, autoscroll=False)
    with gr.Accordion("Review Template", open=False):
        review_template_description = gr.Markdown("We use the ICLR 2025 review template by default, but you can modify the template below as you like.")
        review_template_field = gr.Textbox(label=" ",lines=20, max_lines=20, autoscroll=False, value=REVIEW_FIELDS)
    generate_button = gr.Button("Generate Review", interactive=not paper_text_field)
    file_input.upload(process_file, file_input, paper_text_field)
    paper_text_field.change(lambda text: gr.update(interactive=True) if len(text) > 200 else gr.update(interactive=False), paper_text_field, generate_button)

    review_field = gr.Markdown("\n\n\n\n\n", label="Review")
    generate_button.click(fn=lambda: gr.update(interactive=False), inputs=None, outputs=generate_button).then(generate, [paper_text_field, review_template_field], review_field).then(fn=lambda: gr.update(interactive=True), inputs=None, outputs=generate_button)

    demo.title = "OpenReviewer"




if __name__ == "__main__":
    demo.launch()

