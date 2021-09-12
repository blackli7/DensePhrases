# 高级软件工程（UCAS）课程项目——NLP方向

课程信息：2021~2022秋季学期 中国科学院大学 计算机科学与技术学院 高级软件工程 罗铁坚教授

本次NLP方向课程项目，旨在通过前沿学术成果，帮助同学们分三步：通过接触、理解、改进领域前沿工作，深刻体会NLP模型的基础框架及应用场景。在提高软件工程能力的同时，能够触摸到人工智能算法学术界的一些门路，最后达到开阔视野，增强底蕴的目的。

#### 更新于
**\*\*\*\*\* 2021.09.12 \*\*\*\*\***

**\*\*\*\*\* by lilingwei（lilingwei20@mails.ucas.ac.cn）\*\*\*\*\***

## 目录
* [项目介绍](#项目介绍)
* [Step1 项目建立](#项目建立)
* [Step2 项目应用](#项目应用)
* [Step3 项目拓展](#项目拓展)
* [问题反馈](#问题反馈)
* [Reference](#Reference)
* [License](#License)


## 模型介绍
<em>DensePhrases</em> 是一项由Korea University和Princeton University联合完成的，基于短语级的文本匹配（召回）模型，面向于自然语言理解（下称NLP）中“开放域问答”和“阅读理解”任务。其项目[论文](https://arxiv.org/abs/2012.12624)被收录于ACL2021，你也可以直接通过其[Github项目地址](https://github.com/princeton-nlp/DensePhrases)来了解此模型，或使用其面向维基百科(2018.12.20)数据所训练的[Demo](http://densephrases.korea.ac.kr)来切身体会。

本次NLP课程项目之所以选择面向“开放域问答”任务和“阅读理解”任务，也是继承了课程以往所使用的“对话机器人”项目的特点，希望能够让同学们感受到领域知识对现实生活的影响，以及未来可能的“强AI”时代所必不可少的环节。

同时，本项目 <em>DensePhrases</em> 出自NLP大牛[陈丹琪](https://www.cs.princeton.edu/~danqic/)及其实验室之手，项目完整饱满，代码流畅规范，建议同学们能够同时好好欣赏并学习这些细节。

## Step1 项目建立
本环节希望通过指导同学们如何安装项目环境，建立简易模型Demo，并亲自测试，来感受“项目建立”这项最基础的工作。
### 1.安装环境
首先请安装好conda

（官网安装：https://www.anaconda.com ）
（博客指导：https://www.jianshu.com/p/edaa744ea47d ）

创建DensePhrases项目的conda环境，并安装好所需工具包
```bash
# Install torch with conda (remember to check your CUDA version)
conda create -n densephrases python=3.7
conda activate densephrases
conda install pytorch=1.7.1 cudatoolkit=11.0 -c pytorch

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

设置相关环境变量（建议一路‘yes’）
```bash
# Running config.sh will set the following three environment variables:
# DATA_DIR: for datasets
# SAVE_DIR: for pre-trained models or index; new models and index will also be saved here
# CACHE_DIR: for cache files from huggingface transformers
source config.sh
```

### 2.建立Sample模型
通过项目中已训练好的预训练模型`densephrases-multi` 在四篇短文语料库(`sample/articles.json`)上建立简单模型.
```bash
# generate phrase vectors
# build phrase index
# evaluate phrase retrieval
make step1
```

### 3.测试Sample模型
通过用户输入实际问题检验模型质量。
```bash
# evaluate phrase retrieval with input question
# output the answer, but write details in 'sample/step1_question_test_out.json'
make step1_test
```

## Step2 项目应用
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

### 3.模型时效更新
此部分为增强项目模型鲁棒性的另一方面————时效对齐。同2部分一样，我们具体仍将按照以下步骤进行：1）首先，要构造出准确的测试用例以反映模型的问题；2）其次，找到相应可解决数据集，对模型原始数据集进行更新，重新训练，得到专业化后的新模型；3）再次输入1）中相同测试用例，模型此次的输出能够有了不少好转。

下面是实现的一个例子：



## Step3 项目拓展
本环节将继续在前一环节上，对已有项目的简易模型Demo进行进一步的改进。这一部分更为开放，同学们可以灵活运用软件工程知识，或结合所学知识，使模型在某一维度上产生更好的效果即可，包括但不限于：准确度、召回率、速度、内容丰富度、可移植性、可扩展性、模型复现、演示Demo，甚至是项目或README逻辑改进都是被接受的，只要保证有意义即可。同样的，我们提供一下三个方向作为参考：

1.准确度：

2.模型复现：

3.演示Demo：



## 问题反馈
如遇到任何问题，可以直接询问课程老师和助教，或者联系我`(lilingwei：lilingwei20@mails.ucas.ac.cn)`，你也可以直接通过发起Github Issue发布相关问题，我会尽量及时回复。

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
