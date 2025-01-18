# 西电毕设撰写规范
根据西电毕设撰写规范.docx整理而来，主要关注其中的格式要求部分，按点进行提炼，后续会翻译成匹配函数，会逐点进行格式检测

# 处理规则汇总

## 前置部分要求
- 学号：按照学校的统一编号，在右上角正确打印自己的学号，宋体，小四号，加粗。
- 题目：题目应和任务书的题目一致，黑体，三号。
- 身份信息：学院、专业、班级、学生姓名和导师姓名职称等内容，宋体，小三号，居中排列。
- 摘要：中文摘要，宋体小四号，一般以300字为宜；英文摘要，“Times News Roman”字体，小四号，内容要与中文摘要一致。摘要中不宜出现公式、非公用的符号、术语等。
- 关键词：每篇论文选取3 -5个关键词，中文为黑体小四号，英文为“Times News Roman”字体加粗，小四号。关键词排列在摘要的左下方一行，起始格式为：“关键词：”和“Key  words：”。具体的各个关键词以均匀间隔排列，之间不加任何分隔符号。

## 目录要求
- 目录：按照论文的章、节、附录等前后顺序，编写序号、名称和页码。目录页排在中英文摘要之后，主体部分必须另页右面开始，全文以右页为单页页码。

## 主体部分要求
- 章的标题：如：“摘要”、“目录”、“第一章”、“附录”等，黑体，三号，居中排列。
- 节的标题：如：“2.1  认证方案”、“9.5  小结”等，宋体，四号，居中排列。
- 正文：中文为宋体，英文为“Times News Roman”，小四号。正文中的图名和表名，宋体，五号。
- 页眉：宋体五号，居中排列。左面页眉为论文题目，右面页眉为章次和章标题。页眉底划线的宽度为0.75磅。
- 页码：宋体小五号，排在页眉行的最外侧，不加任何修饰。

## 图表类要求
- 图：包括曲线图、示意图、流程图、框图等。图序号一律用阿拉伯数字分章依序编码，如：图1.3、图2.11。每一图应有简短确切的图名，连同图序号置于图的正下方。图中坐标上标注的符号和缩略词必须与正文中一致。
- 表：包括分类项目和数据，一般要求分类项目由左至右横排，数据从上到下竖列。分类项目横排中必须标明符号或单位，竖列的数据栏中不宜出现“同上” 、“同左”等类似词语，一律填写具体的数字或文字。表序号一律用阿拉伯数字分章依序编码，如：表2.5、表10.3。每一表应有简短确切的题名，连同表序号置于表的正上方。
- 公式：正文中的公式、算式、方程式等必须编排序号，序号一律用阿拉伯数字分章依序编码，如：式(3-32)、式(6-21)。对于较长的公式，另行居中横排，只可在符号处（如：+、-、*、/、< >等）转行。公式序号标注于该式所在行（当有续行时，应标注于最后 一行）的最右边。连续性的公式在“=”处排列整齐。大于999的整数或多于三位的小数，一律用半个阿拉伯数字符的小间隔分开；小于1的数应将0置于小数点之前。
- 计量单位：单位名称和符号的书写方式一律采用国际通用符号。
- 参考文献：在学位论文中引用参考文献时，引出处右上角用方括号标注阿拉伯数字编排的序号（必须与参考文献一致）。参考文献的排列格式分为：
  - 专著类的文献：

  [序号]  作者 . 专著名称.  版本. 出版地：出版者，出版年. 参考的页码。

  - 期刊类的文献：
  
  [序号]  作者 . 文献名. 期刊名称.  年 , 月,  卷（期）. 页码

## 附录要求
- 附录格式：附录依次用大写正体A，B，C……编序号，黑体，三号。如：附录A；
- 附录信息：附录中的图、表、式、参考文献等与正文分开，用阿拉伯数字另行编序号，注意在数码前冠以附录的序码。如：图A1；表B2；式（C-3）；文献[D5]。


# 处理方式分类
格式检查环节拆解如下：
1. 定位
2. 检验

定位分为固定内容匹配和特殊内容匹配，前者比如标题，段落；后者就是学号题目等

检验分为字体字号检验和规则匹配检验，前者如宋体，四号；后者指"2.1",起始格式“关键词：”等

## 固定内容匹配
1. 目录
2. 章的标题
3. 节的标题
4. 正文
5. 页眉
6. 页码
7. 参考文献

```python
from docx import Document
import re

def analyze_document(filepath):
    doc = Document(filepath)
    result = {}

    # 定位目录
    for i, paragraph in enumerate(doc.paragraphs):
        if "目录" in paragraph.text:
            result["目录"] = i
            break

    # 定位章标题、节标题
    result["章标题"] = []
    result["节标题"] = []
    for i, paragraph in enumerate(doc.paragraphs):
        text = paragraph.text.strip()
        if re.match(r"第\d+章", text):
            result["章标题"].append(i)
        elif re.match(r"\d+\.\d+", text):
            result["节标题"].append(i)

    # 定位正文 (简化处理，需要根据实际情况修改)
    result["正文"] = list(range(len(doc.paragraphs)))  # 初始值，需要排除其他部分
    result["正文"] = list(set(result["正文"]) - set(result.get("目录", [])) - set(result.get("章标题", [])) - set(result.get("节标题", [])))

    # 定位页眉 (每个section可能都有页眉)
    result["页眉"] = []
    for section in doc.sections:
        header_text = section.header.paragraphs[0].text.strip() if section.header.paragraphs else ""
        result["页眉"].append(header_text)

    # 定位页码 (简化处理，需要根据实际情况修改)
    result["页码"] = [] # 需要更复杂的逻辑来提取页码


    # 定位参考文献 (简化处理，需要根据实际情况修改)
    for i, paragraph in enumerate(doc.paragraphs):
        if "参考文献" in paragraph.text:
            result["参考文献"] = i
            break

    return result

# 示例调用
filepath = "your_document.docx"  # 替换为你的文档路径
analysis_result = analyze_document(filepath)
print(analysis_result)
```

## 特殊内容匹配
1. 学号
2. 题目
3. 身份信息
4. 摘要
5. 关键词
6. 图
7. 表
8. 公式
9. 计量单位
    
```python
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

def extract_cover_info(filepath):
    doc = Document(filepath)
    cover_page = doc.paragraphs  # 假设封面页信息都在前几个段落中

    extracted_info = {}

    # 学号 (假设在第一个段落，右上角)
    try:
        extracted_info["学号"] = cover_page[0].text.split(":")[-1].strip()
        # ... (样式检查，需要根据实际情况修改) ...
    except:
        extracted_info["学号"] = "未找到"

    # 题目 (假设在第二个段落，居中，黑体三号)
    try:
        extracted_info["题目"] = cover_page[1].text.strip()
        # ... (样式检查，需要根据实际情况修改) ...
    except:
        extracted_info["题目"] = "未找到"

    # 身份信息 (假设在第三个段落，居中，小三号)
    try:
        extracted_info["身份信息"] = cover_page[2].text.strip()
        # ... (样式检查，需要根据实际情况修改) ...
    except:
        extracted_info["身份信息"] = "未找到"

    # 摘要 (假设在接下来的段落中，需要根据关键字或格式识别)
    try:
        abstract_start_index = next(i for i, p in enumerate(cover_page) if "摘要" in p.text)
        # ... (提取中文摘要和英文摘要，需要根据实际情况修改) ...
        extracted_info["中文摘要"] = "" # 需要提取
        extracted_info["英文摘要"] = "" # 需要提取
        # ... (样式检查，需要根据实际情况修改) ...
    except:
        extracted_info["中文摘要"] = "未找到"
        extracted_info["英文摘要"] = "未找到"

    # 关键词 (假设在摘要之后，需要根据关键字或格式识别)
    try:
        keywords_start_index = next(i for i, p in enumerate(cover_page) if "关键词" in p.text or "Key words" in p.text)
        # ... (提取中文关键词和英文关键词，需要根据实际情况修改) ...
        extracted_info["中文关键词"] = [] # 需要提取
        extracted_info["英文关键词"] = [] # 需要提取
        # ... (样式检查，需要根据实际情况修改) ...
    except:
        extracted_info["中文关键词"] = []
        extracted_info["英文关键词"] = []

    return extracted_info

# 示例调用
filepath = "your_document.docx"  # 替换为你的文档路径
cover_info = extract_cover_info(filepath)
print(cover_info)
```
  


## 字体字号检验
字体字号检验主要是主体部分和前置部分
1. 章的标题
2. 节的标题
3. 征文
4. 页眉
5. 页码
6. 学号
7. 题目
8. 身份信息
9. 摘要
10. 关键词

```python
style_template = {
    'student_id': {'font': '宋体', 'size': Pt(10.5), 'bold': True},  # 小四号，加粗
    'title': {'font': '黑体', 'size': Pt(18)},  # 三号，黑体
    'identity': {'font': '宋体', 'size': Pt(12), 'alignment': WD_ALIGN_PARAGRAPH.CENTER}, #小三号，居中
    'abstract_cn': {'font': '宋体', 'size': Pt(10.5)},  # 中文摘要，小四号
    'abstract_en': {'font': 'Times New Roman', 'size': Pt(10.5)},  # 英文摘要，小四号
    'keywords_cn': {'font': '黑体', 'size': Pt(10.5)},  # 中文关键词，小四号，黑体
    'keywords_en': {'font': 'Times New Roman', 'size': Pt(10.5), 'bold': True},  # 英文关键词，小四号，加粗
    'chapter_title': {'font': '黑体', 'size': Pt(18), 'alignment': WD_ALIGN_PARAGRAPH.CENTER},
    'section_title': {'font': '宋体', 'size': Pt(12), 'alignment': WD_ALIGN_PARAGRAPH.CENTER},
    'body': {'font': '宋体', 'size': Pt(10.5)},
    'english_body': {'font': 'Times New Roman', 'size': Pt(10.5)},
    'figure_caption': {'font': '宋体', 'size': Pt(11)},
    'table_caption': {'font': '宋体', 'size': Pt(11)},
    'header': {'font': '宋体', 'size': Pt(11), 'alignment': WD_ALIGN_PARAGRAPH.CENTER},
}

```

## 规则检验
规则检验主要包含图表的命名规则
1. 目录
2. 章的标题
3. 节的标题
4. 页眉
5. 图
6. 表
7. 公示
8. 计量单位
9. 参考文献