import module
import setting

if __name__ == '__main__':
    # 开始页
    start_page = setting.START_PAGE
    # 结束页
    end_page = setting.END_PAGE + 1
    # 开始获取数据
    for i in range(start_page, end_page):
        offset = i * setting.PAGE_OFFSET
        jsonObj = module.get_request_json_obj(offset, setting.PAGE_LIMIT)
        commentList = jsonObj["comments"]
        # 一页的数据作为一个字符串
        comments = ""
        for comment in commentList:
            # 将每页的子数据进行叠加 以换行作为结束
            commentStr = comment["user"]["nickname"] + "---" + comment["content"] + "---" + str(comment["time"]) + "\n"
            comments += commentStr
        # 写入本地
        module.write_word_to_local(comments)
        print("共%s页,已完成%s页" % (end_page - 1, str(i + 1)))
