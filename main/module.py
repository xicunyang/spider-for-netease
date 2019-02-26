# 导入requests的包 用来网络请求
import requests
# 导入时间包
import time
# 调用js
import execjs
# 解析JSON的包
import json
# 配置项
import setting


def get_js():
    """
    读取本地JS文件
    :return:
    """
    f = open(setting.JS_PATH, 'r', encoding='UTF-8')
    line = f.readline()
    html_str = ''
    while line:
        html_str += line
        line = f.readline()
    return html_str


def get_secret_params(limit, offset):
    """
    获取秘密参数  params 和  encSecKey的公用方法
    :param limit: 每页评论数的个数
    :param offset: 个数的偏移
    :return:
    """
    js_code = get_js()
    p = execjs.compile(js_code).call('d',
                                     '{"id":%s,"lv":-1,"tv":-1,"csrf_token":"",limit:\"%s\",offset:"%s"}' % (
                                         setting.SONG_ID, limit, offset),
                                     setting.PARAMS.get("P1"), setting.PARAMS.get("P2"), setting.PARAMS.get("P3"))
    data = {
        "params": p["encText"],
        "encSecKey": p["encSecKey"]
    }
    return data


def get_request_json_obj(offset, limit):
    """
    获取请求到的json对象
    :param offset: 页面数据偏移
    :param limit: 页面数据个数
    :return:
    """
    data = get_secret_params(offset, limit)

    result_info = requests.post(
        'http://music.163.com/weapi/v1/resource/comments/R_SO_4_%s?csrf_token=' % setting.SONG_ID,
        headers=setting.HEADERS, data=data).text

    json_obj = json.loads(result_info)
    return json_obj


def write_word_to_local(word):
    """
    保存文件到本地
    :return:
    """
    with open("data/" + "comments" + setting.SONG_ID + ".txt", "a", encoding="utf-8") as f:
        # f.write(str(word) + "\n")
        f.write(str(word))
        f.close()
        # 线程休眠2秒
        time.sleep(setting.THREAD_SLEEP_TIME)
