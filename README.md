# 💡 What is learning_assistant?
这是一个专属的知识库学习助手
# ✨ Start
##  🛠Environment
1. 安装 conda 环境
~~~bash
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm -rf ~/miniconda3/miniconda.sh
~~~
2. 初始化环境
~/miniconda3/bin/conda init bash
~/miniconda3/bin/conda init zsh
3. **新建 bash** 查看是否安装成功
![alt text](./pic/image.png)
这里看到（base）表示安装成功
4. 创建新的 conda 虚拟环境
`conda env create -f environment.yml`
进入该虚拟环境
`conda activate llm-universe`
5. 设置环境变量
目前程序仅支持智谱 API
进入 .env 文件导入你的智谱 API
## Usage
1. 导入你的知识库
将 markdown 格式的文件导入 knowledge 文件夹
2. 执行代码 learning assistant
`python3 ./src/learning_assistant.py`


# 🎉开发框架



