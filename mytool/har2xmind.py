from mytool.common.comm import *
from mytool.common.schema_har import *
import json
import xmind
from xmind.core.markerref import MarkerId
from urllib.parse import urlparse

def convert_har_to_xmind(har_path, xmind_output_path):
    # 读取Har JSON文件
    with open(har_path, 'r', encoding='utf-8') as file:
        har_data = json.load(file)
    vailidata_OpenAPI(har_data, SCHEMA_HAR)

    # 收集接口信息
    APIs = har_data.get('log').get('entries')

    # 初始化XMind工作簿
    # 1、如果指定的XMind文件存在，则加载，否则创建一个新的
    workbook = xmind.load("my.xmind")

    # 2、获取第一个画布（Sheet），默认新建一个XMind文件时，自动创建一个空白的画布
    sheet1 = workbook.getPrimarySheet()

    # ***** 第一个画布 *****
    sheet1.setTitle("sheet1")  # 设置画布名称

    # 获取画布的中心主题，默认创建画布时会新建一个空白中心主题
    root_topic = sheet1.getRootTopic()
    root_topic.setTitle("接口测试用例集(har)")  # 设置主题名称

    # 创建一个子主题，并设置其名称
    sub_topic1 = root_topic.addSubTopic()
    sub_topic1.setTitle("第一个接口测试用例")

    def add_note(topic, Title):
        newtopic = topic.addSubTopic()
        newtopic.setTitle(Title)
        return newtopic

    # 整理请求数据
    for api in APIs:
        req_path_param = []
        req_header = {}
        xmind_maxLenght = 2500
        path = urlparse(api.get('request').get('url')).path
        method = api.get('request').get('method').lower()
        # 提取header
        for header in api.get('request').get("headers"):
            req_header.update({header.get('name'): header.get('value')})

        req_header = json.dumps(req_header, ensure_ascii=False, indent=2)
        req_header = req_header if len(req_header) <= xmind_maxLenght else '数据过长，只显示部分字符:' + req_header[
                                                                                                        :xmind_maxLenght]

        req_body_type = api.get('request').get('postData').get('mimeType')

        req_body = api.get('request').get('postData').get('text')
        req_body = req_body if len(req_body) <= xmind_maxLenght else '数据过长，只显示部分字符:' + req_body[
                                                                                                  :xmind_maxLenght]

        response_body = api.get('response').get('content').get('text')
        response_body = response_body if len(
            response_body) <= xmind_maxLenght else '数据过长，只显示部分字符:' + response_body[:xmind_maxLenght]

        # 开始写入xmind
        sub_topic1_1 = add_note(sub_topic1, f"请求 {method} {path} 接口成功")
        # 给主题添加一个备注（case前置条件)
        # sub_topic1_1.setPlainNotes(f"请求头为:\n{req_header}")
        # 给主题添加图标(标记用例标题)
        sub_topic1_1.addMarker(MarkerId.priority1)

        # 具体步骤
        sub_topic_header = add_note(sub_topic1_1, f"请求头参数")
        add_note(sub_topic_header, f"{req_header}")
        sub_topic1_1_1 = add_note(sub_topic1_1, f"url路径参数")
        add_note(sub_topic1_1_1, f"{'空' if req_path_param == [] else req_path_param}")

        sub_topic_req_body_type = add_note(sub_topic1_1, f"请求体类型")
        add_note(sub_topic_req_body_type, f"{'空' if req_body_type == {} or req_body_type == '' else req_body_type}")

        sub_topic_req_body = add_note(sub_topic1_1, f"请求体")
        add_note(sub_topic_req_body, f"{'空' if req_body == {} or req_body == '' else req_body}")
        sub_topic1_1_3 = add_note(sub_topic1_1, "检查响应是否返回成功，系统内部响应码为200")
        add_note(sub_topic1_1_3, f"成功")
        sub_topic1_1_4 = add_note(sub_topic1_1, "接口响应成功，响应体形如")
        add_note(sub_topic1_1_4, f"{'空' if response_body == {} or response_body == '' else response_body}")

    # 4、保存（如果指定path参数，另存为该文件名）
    xmind.save(workbook, path=xmind_output_path)

    logger.info(f"导出Xmind文件：{xmind_output_path}")


# if __name__ == "__main__":
#     har_path = os.path.join(CACHE, 'har_20240706_101757_washed.har')
#     xmind_output_path = os.path.join(CACHE, 'har_20240706_101757_washed.xmind')
#     # 示例调用
#     convert_har_to_xmind(har_path, xmind_output_path)
