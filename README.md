# cchess-brobot

二师兄借的Brobot机械臂，拿来陪大家下象棋。


## Demo

| Demo1 | Demo2 | Demo3 |
|:---------|:--------------------|:----------------|
| ![demo1](/etcs/demo1.gif)     | ![demo2](/etcs/demo3.gif) | ![demo3](/etcs/demo5.gif) |


## 目录
CCHESS-BROBOT  
│  README.md  
│  requirements.txt  
├─cchessgame  
│  │  player.py 主程序  
│  │  test.py 视觉测试  
│  └─ utils.py 引用的函数  
├─pybrobot  
│  │  brobot.py Brobot类 机械臂控制  
│  │  config.py 机械臂参数列表  
│  └─ message.py 通信协议  
├─strategy  
│  ├─binghewusi   象棋引擎-兵河五车  
│  ├─cyclone      象棋引擎-象棋旋风  
│  │  │  cyclone.exe 引擎文件  
│  │  │  cyclone_strategy.py StrategyCyclone类  
│  │  └─ test.py subprocess通信测试  
│  └─moonfish     象棋引擎-moonfish  
│      └─ moonfish_strategy.py StrategyMoonfish类  
└─vision  
    │  svm_classify.py Identify类 局面识别  
    │  svm_1.mat 棋子识别模型文件  
    │  svm_2.mat 红黑二分类模型文件  
    │  utils.py 引用的函数  
    │  camtest.py 测试_摄像头  
    │  vision_threshold.py 测试_阈值调试  
    │  test.py 测试_截取象棋棋盘  
    │  test2.py 测试_找棋子  
    │  test3.py 测试_局面识别  
    ├─2-classify 红黑棋子二分类  
    │  │  data_pre.py 提取特征制作数据集  
    │  │  final_test.py 模型测试  
    │  │  svm_test.py 训练svm模型  
    │  └─ utils.py 引用的函数  
    └─classify 棋子识别  
       │  01_circle_params.py 调整霍夫圆环检测参数  
       │  02_prepare_data.py 找圆截图准备原始数据  
       │  03_preprocess_data.py 提取特征制作数据集  
       │  04_svm_model.py 训练svm模型  
       │  05_svm_test.py 模型测试  
       └─ classify.ipynb jupyternotebook .  
       

