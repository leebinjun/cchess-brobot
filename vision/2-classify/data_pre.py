from utils import get_feature
import os

rootdir = r'.\vision\2-classify\data\0'
alist = os.listdir(rootdir) #列出文件夹下所有的目录与文件
# print(alist[:20])
X_data = []

for i, path in enumerate(alist):
    img_path = os.path.join(rootdir,alist[i])
    print(img_path)
    if os.path.isfile(img_path):
        fea = get_feature(img_path)
        X_data.append(fea)

lenth = len(alist)
y_data = [0]*lenth



rootdir = r'.\vision\2-classify\data\1'
alist = os.listdir(rootdir) #列出文件夹下所有的目录与文件
for i, path in enumerate(alist):
    img_path = os.path.join(rootdir,alist[i])
    print(img_path)
    
    if os.path.isfile(img_path):
        fea = get_feature(img_path)
        X_data.append(fea)

lenth = len(alist)
y_data = y_data + [1]*lenth


print(len(X_data))
print(len(y_data))


