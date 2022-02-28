import pprint
import re
import subprocess
import requests

headers = {
    # 浏览器标识符
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/96.0.4664.45 Safari/537.36',
    # 防盗链
    'referer': 'https://www.bilibili.com/video/'
}


def get_response(url):
    """发送请求"""
    response = requests.get(url=url, headers=headers)
    return response


def get_cid_name(bvid):
    url = 'https://api.bilibili.com/x/player/pagelist?'
    param = {
        'bvid': bvid,
        'jsonp': 'jsonp'
    }
    response = requests.get(url=url, params=param, headers=headers).json()
    data = response['data'][0]

    cid = data['cid']
    name = data['part']
    print(cid, name)
    return cid, name


def get_session(bvid):
    """request请求后 正则表达式session"""
    url = f'https://www.bilibili.com/video/{bvid}'
    response = requests.get(url=url, headers=headers)
    # 使用正则表达式进行获取
    session = re.findall('"session":"(.*?)"', response.text)[0]
    return session


def get_video_url(bvid, cid, session):
    url = 'https://api.bilibili.com/x/player/playurl'
    params = {
        'cid': cid,
        'bvid': bvid,
        'qn': '0',
        'type': '',
        'otype': 'json',
        'fourk': '1',
        'fnver': '0',
        'fnval': '976',
        'session': session
    }
    response = requests.get(url=url, params=params, headers=headers).json()
    # json解析，五层字典取出实际url
    audio_url = response['data']['dash']['audio'][0]['baseUrl']
    video_url = response['data']['dash']['video'][0]['baseUrl']
    print("音视频链接已得到" + "音频：" + audio_url + "视频：" + video_url)
    return audio_url, video_url


def save_video(name, audio_url, video_url):
    """保存数据 r.content获取二进制内容"""
    # 请求音频数据，返回的数据二进制形式解析
    audio_content = get_response(audio_url).content
    print("开始下载" + name + "音频")
    # 保存音频文件
    with open(f"{name}.mp3", mode='wb') as af:
        af.write(audio_content)
        print(name + "音频保存完成")

    # 请求视频数据，返回的数据二进制形式解析
    video_content = get_response(video_url).content
    print("开始下载" + name + "视频")
    # 保存视频文件
    with open(f"{name}.mp4", mode='wb') as vf:
        vf.write(video_content)
        print(name + "视频保存完成")


def merge_audio_video(name):
    """音视频合并"""
    # cmd 命令
    command = f"ffmpeg.exe -i {name}.mp4 -i {name}.mp3 -acodec copy -vcodec copy A{name}.mp4"
    subprocess.run(command, shell=True)
    print(name + "视频正在执行合成命令")


if __name__ == '__main__':
    bvid = 'BV14z4y1S7s2'
    # 调用选集获取函数，信息填入三个列表
    cid, name = get_cid_name(bvid)
    # 获取session
    session = get_session(bvid)
    # 通过前文搜集到信息，寻找音视频真正的链接
    audio_url, video_url = get_video_url(bvid, cid, session)
    # # 根据音频，视频链接分别下载
    # save_video(name, audio_url, video_url)
    # # 使用ffmpeg.exe合并下载到的音视频
    # merge_audio_video(name)
