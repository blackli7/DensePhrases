# DensePhrases Demo

<em>DensePhrases</em> 是一项由Korea University和Princeton University联合完成的，基于短语级的英文文本匹配（召回）模型，面向于NLP中“开放域问答”和“阅读理解”任务。其项目[论文](https://arxiv.org/abs/2012.12624)被收录于ACL2021，你也可以直接通过其[Github项目地址](https://github.com/princeton-nlp/DensePhrases)来了解此模型，或使用其面向维基百科(2018.12.20)数据所训练的[Demo](http://densephrases.korea.ac.kr)来切身体会。

本次项目需要GPU资源，若本地没有GPU，可使用[Google Colab](https://colab.research.google.com/)运行项目下`UCAS-DensePhrase.ipynb`脚本（推荐）

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1oAJWzpIbT45cqXOwqDD5oElL-h679PBu?usp=sharing)

<!--课程信息：2021~2022秋季学期 中国科学院大学 计算机科学与技术学院 高级软件工程 罗铁坚教授
本次NLP方向课程项目，旨在通过前沿学术成果，帮助同学们分三步：通过接触、理解、改进领域前沿工作，深刻体会NLP模型的基础框架及应用场景。在提高软件工程能力的同时，能够触摸到人工智能算法学术界的一些门路，最后达到开阔视野，增强底蕴的目的。-->

#### 更新于
**\*\*\*\*\* 2021.09.30 \*\*\*\*\***

**\*\*\*\*\* by lilingwei（lilingwei20@mails.ucas.ac.cn）\*\*\*\*\***

## 目录
* [Step0-安装环境](#安装环境)
* [Step1-项目建立](#项目建立)
* [Step2-训练Demo](#训练Demo)
* [Step3-测试Demo](#测试Demo)
* [FAQ](#FAQ)
* [问题反馈](#问题反馈)
* [Reference](#Reference)
* [License](#License)


## 安装环境

首先请安装好conda

（官网安装：https://www.anaconda.com ）

（博客指导：https://www.jianshu.com/p/edaa744ea47d ）

## 项目建立

创建DensePhrases项目的conda环境，并安装好所需工具包
```bash
# Install torch with conda (remember to check your CUDA version)
conda create -n densephrases python=3.7
conda activate densephrases
conda install pytorch=1.7.1 
conda install cudatoolkit=11.0 -c pytorch

# Install densephrases for course of UCAS
git clone https://github.com/blackli7/DensePhrases.git

# Install apex
git clone https://www.github.com/nvidia/apex.git
cd apex
python setup.py install
cd ..

# Install other toolkits
cd DensePhrases
pip install -r requirements.txt
python setup.py develop
```

设置相关环境变量
```bash
# Running config.sh will set the following three environment variables:
# DATA_DIR: for datasets
# SAVE_DIR: for pre-trained models or index; new models and index will also be saved here
# CACHE_DIR: for cache files from huggingface transformers
source config.sh
```

检查一下正确性
```bash
# Check downloads
pip list
# If yes, you can see these information on the console.
apex faiss-gpu torch transformers ...
# Check config
echo $SAVE_DIR
# If yes, you can see these information on the console.
.//outputs
```


## 训练Demo
通过项目中已训练好的预训练模型`densephrases-multi` 在简单的物理资料（`data/wiki_physics.json`，来源于English Wikipedia）上建立模型Demo.

DensePhrases所使用的训练数据必须满足以下json格式:（具体见：`sample/articles.json`）
```
{
    "data": [
        {
            "title": "America's Got Talent (season 4)",
            "paragraphs": [
                {
                    "context": " The fourth season of \"America's Got Talent\", ... Country singer Kevin Skinner was named the winner on September 16, 2009 ..."
                },
                {
                    "context": " Season four was Hasselhoff's final season as a judge. This season started broadcasting live on August 4, 2009. ..."
                },
                ...
            ]
        },
    ]
}
```
相关数据格式处理示例见：`data_process`


运行以下命令，生成模型Demo
```bash
# generate phrase vectors
# build phrase index
# evaluate phrase retrieval
# (try it more times if something goes wrong.)
make step1
```

完成后会在命令台看到如下信息：
<div align="left">
  <img alt="step1" src="https://raw.githubusercontent.com/blackli7/DensePhrases/main/pic_files/step1.jpg" width="750px">
</div>

## 测试Demo
通过命令台输入测试Demo模型。
```bash
# evaluate phrase retrieval with input question
# output the answer, but write details in 'sample/step1_question_test_out.json'
make step1_test
```

完成后会在命令台看到如下信息，按照提示输入问题文本：
<div align="left">
  <img alt="step1_test_q" src="https://raw.githubusercontent.com/blackli7/DensePhrases/main/pic_files/step1_test_q.jpg" width="750px">
</div>
输入完成后，回车，经过一段时间后模型会输出答案：
<div align="left">
  <img alt="step1_test_a" src="https://raw.githubusercontent.com/blackli7/DensePhrases/main/pic_files/step1_test_a.jpg" width="750px">
</div>

进一步地，通过运行`web_demo_django`文件夹下或者自己编写的网页演示程序来将模型封装，进行交互式的输入输出：
```bash
# move into the web directory
cd web_demo_django
# run django server
python manage.py runserver
# then open the address(http://127.0.0.1:8000/) on your browser.
```
<div align="left">
  <img alt="web_demo" src="https://raw.githubusercontent.com/blackli7/DensePhrases/main/pic_files/web_demo.jpg" width="850px">
</div>

<!--## 项目应用
本环节将在前一环节上，对已有项目的简易模型Demo进行改进，增强其鲁棒性和实用性，具体表现在针对某一领域知识能够具备不错的问答能力，或者对齐模型的实效性，具体将在以下部分阐述，课程项目仅要求在2，3部分中选一个完成。

### 1.数据集
DensePhrases所使用的训练数据必须满足以下json格式:（具体见：sample/articles.json）
```
{
    "data": [
        {
            "title": "America's Got Talent (season 4)",
            "paragraphs": [
                {
                    "context": " The fourth season of \"America's Got Talent\", ... Country singer Kevin Skinner was named the winner on September 16, 2009 ..."
                },
                {
                    "context": " Season four was Hasselhoff's final season as a judge. This season started broadcasting live on August 4, 2009. ..."
                },
                ...
            ]
        },
    ]
}
```

### 2.模型专业化
此部分为课程项目核心要求，希望同学们亲自动手，通过专业化项目模型来增强模型在某一领域的鲁棒性。具体将按照以下步骤进行：1）首先，要构造出准确的测试用例以反映模型的问题；2）其次，找到相应可解决数据集，对模型原始数据集进行更新，重新训练，得到专业化后的新模型；3）再次输入1）中相同测试用例，模型此次的输出能够有了不少好转。

下面是实现的一个例子：

1.测试用例: What is Newton's First Law?
<div align="left">
  <img alt="Newtons_pre" src="https://raw.githubusercontent.com/blackli7/DensePhrases/main/pic_files/Newtons_pre.jpg" width="450px">
</div>
-----显然，系统不明所以-----

2.更换/增强fine-tuning数据集（./sample/article.json）

3.重新训练（[step1](#项目建立)）

4.再次输入相同测试用例：What is Newton's First Law?
<div align="left">
  <img alt="Newtons_now" src="https://raw.githubusercontent.com/blackli7/DensePhrases/main/pic_files/Newtons_now.jpg" width="450px">
</div>
这一次，模型输出正确结果。

### 3.模型时效更新
此部分为增强项目模型鲁棒性的另一方面————时效对齐。同2部分一样，我们具体仍将按照以下步骤进行：1）首先，要构造出准确的测试用例以反映模型的问题；2）其次，找到相应可解决数据集，对模型原始数据集进行更新，重新训练，得到专业化后的新模型；3）再次输入1）中相同测试用例，模型此次的输出能够有了不少好转。


下面是实现的一个例子：

1.测试用例: Which team does Christiano Ronaldo play for now?
<div align="left">
  <img alt="Ronaldo_pre" src="https://raw.githubusercontent.com/blackli7/DensePhrases/main/pic_files/Ronaldo_pre.jpg" width="450px">
</div>
-----显然，这个信息是不符合实际情况的（C罗于2021.08.28回到曼联）-----

2.更换/增强fine-tuning数据集（./sample/article.json）

3.重新训练（[step1](#项目建立)）

4.再次输入相同测试用例：Which team does Christiano Ronaldo play for now?
<div align="left">
  <img alt="Ronaldo_now" src="https://raw.githubusercontent.com/blackli7/DensePhrases/main/pic_files/Ronaldo_now.jpg" width="450px">
</div>
这一次，模型输出正确结果。


## 项目拓展
本环节将继续在前一环节上，对已有项目的简易模型Demo进行进一步的改进。这一部分更为开放，同学们可以灵活运用软件工程知识，或结合所学知识，使模型在某一维度上产生更好的效果即可，包括但不限于：准确度、召回率、速度、内容丰富度、可移植性、可扩展性、模型复现、演示Demo、语言迁移等，甚至是项目或README逻辑改进都是被接受的，只要保证有意义即可。同样的，我们提供以下三个方向作为参考：

### 1.准确度：

### 2.模型复现：

### 3.演示Demo：-->

## FAQ
### 1.
Q: 在安装好conda后，使用conda安装工具时，报错PackagesNotFoundError：
<div align="left">
  <img alt="faq1" src="https://raw.githubusercontent.com/blackli7/DensePhrases/main/pic_files/faq1.jpg" width="750px">
</div>
A：尝试通过下面的命令增加下载源后再试一次：

```bash
conda config --add channels conda-forge
conda config --add channels \ https://mirrors.ustc.edu.cn/anaconda/pkgs/free/
conda config --add channels \ https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
```

### 2.
Q: git clone远程下载失败：
<div align="left">
  <img alt="faq2" src="https://raw.githubusercontent.com/blackli7/DensePhrases/main/pic_files/faq2.jpg" width="750px">
</div>
A：多试几次，或在git命令前设置连接节点 GIT_CURL_VERBOSE=0 ，例如：

```bash
GIT_CURL_VERBOSE=0 git clone https://www.github.com/nvidia/apex.git
```

## 问题反馈
如遇到任何问题，可以直接询问课程老师和助教，或者联系我(`lilingwei：lilingwei20@mails.ucas.ac.cn`)，你也可以直接通过发起Github Issue发布相关问题，我会尽量及时回复。

## Reference
Please cite the paper if you use DensePhrases in your work:
```bibtex
@inproceedings{lee2021learning,
   title={Learning Dense Representations of Phrases at Scale},
   author={Lee, Jinhyuk and Sung, Mujeen and Kang, Jaewoo and Chen, Danqi},
   booktitle={Association for Computational Linguistics (ACL)},
   year={2021}
}
```

## License
Please see LICENSE for details.

[demo]: http://densephrases.korea.ac.kr
