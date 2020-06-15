import os
import json
import re
import time


# 读取json文件
def readJson(fileName):
    f = open(fileName, encoding='utf-8')
    setting = json.load(f)

    if 'PartName' in setting:
        if setting['PartName'] is None:
            title = setting['Title']
        else:
            title = setting['Title'] + '  ' + setting['PartName']
    else:
        title = setting['title'] + '  ' + setting['page_data']['part']
    return title


# 获取文件列表
def getFileList(file_dir):
    # 定义三个列表
    Title = []
    VideoPath = []
    AudioPath = []
    # 遍历文件目录
    for root, dirs, files in os.walk(file_dir):
        if ('entry.json' in files):
            Tname = str(root) + '\\entry.json'
            Tname = readJson(Tname)
            Title.append(Tname)
            path = str(root) + '\\' + str(dirs[0])
            if os.path.exists(path + '\\0.blv'):
                Vpath = path + '\\0.blv'
                Apath = path + '\\0.blv'
                VideoPath.append(Vpath)
                AudioPath.append(Apath)
            elif os.path.exists(path + '\\video.m4s') and os.path.exists(path + '\\audio.m4s'):
                Vpath = path + '\\video.m4s'
                Apath = path + '\\audio.m4s'
                VideoPath.append(Vpath)
                AudioPath.append(Apath)
            else:
                print('错误，未找到缓存文件，可能未缓存完成，路径为：' + str(root))
                os.system("pause");
        infofile = '/0'
        movfile = '/0'
        for file in files:
            if '.info' in file[-5:]:
                infofile = str(root) + '\\' + file
            if ('.flv' in file[-4:]):
                movfile = str(root) + '\\' + file
            if ('.mp4' in file[-4:]):
                movfile = str(root) + '\\' + file

        if (infofile is not '/0') and (movfile is not '/0'):
            Tname = readJson(infofile)
            Title.append(Tname)
            VideoPath.append(movfile)
            AudioPath.append(movfile)

        elif (infofile is not '/0') or (movfile is not '/0'):
            print(str(root) + '\\')
            os.system("pause");

    return [Title, VideoPath, AudioPath]


# 输出mp4文件
def getMP4(title, video_path, audio_path):
    # 生成输出目录
    if not os.path.exists("./output"):
        os.mkdir("./output")
    # 循环生成MP4文件
    print(title)
    for n, i in enumerate(title):
        # 规范文件名
        cop = re.compile('[\\\\/:*?\"<>|]')  # 匹配不是中文、大小写、数字的其他字符
        reName = i
        reName = cop.sub('', reName)  # 将标题中匹配到的字符替换成空字符
        print(reName)
        # 开始生成MP4文件
        if not os.path.exists("./output/" + reName + ".mp4"):
            print("ffmpeg -i " + video_path[title.index(i)] + " -i " + audio_path[
                title.index(i)] + " -codec copy ./output/" + str(n) + ".mp4")
            os.system(
                "ffmpeg -i " + video_path[title.index(i)] + " -i " + audio_path[
                    title.index(i)] + " -codec copy ./output/" + str(n) + ".mp4")
            os.rename("./output/" + str(n) + ".mp4", "./output/" + reName + ".mp4")
            print("正在合成...")
            print("标题：" + i)
            print("视频源：" + video_path[title.index(i)])
            print("音频源：" + audio_path[title.index(i)])


print("欢迎使用批量合成M4S工具")
fileDir = str(input("请输入含M4S文件的目录:"))
f = getFileList(fileDir)
getMP4(f[0], f[1], f[2])
print("合成完毕")
