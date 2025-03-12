# Intro
PaperGuardian is my Diploma Project, designed for Paper Format Detection and Paper Peer Review.

The project can be divided into four moduls
- **PaperLoader**: Load and preprocess papers for subsequent testing and analysis(docx,pdf)
- **FormatDetection**: Check the format of the paper according to the specified requirements
- **PeerReview**: Evaluate the content and quality of articles through multi-module collaboration and give corresponding suggestions
- **Visual**: Offer an interactive GUI (Gradio) 

To Enable stability of the code， we use ipynb to test some feat in [Folder Test](./Test) and the TestPaper are placed in [Folder TestPaper](./TestPaper/)



## Roadmaps


### PaperLoader
- [x] Docx Loader
- [ ] PDF Loader
- [ ] Grobid
- [ ] Visual Preprocess(VLM)


### FormatDetection
- [x] Normal Element Location (7/7)
- [ ] Special Element Location (5/9)
- [x] Font and Size Check (10/10)
- [ ] Rule Check (4/9)


### PeerReview
- [ ] LLM Finetune
- [ ] External Knowledage module

### Visual
- [x] Gradio GUI
- [ ] Modern Frontend GUI

![GUI1.png](https://kashiwa-pic.oss-cn-beijing.aliyuncs.com/20250312185146571.png)
![GUI2.png](https://kashiwa-pic.oss-cn-beijing.aliyuncs.com/20250312185212377.png)