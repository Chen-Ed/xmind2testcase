import os.path

from common.parseOpenApi import ParseOpenApi
from common.comm import *
import json


class HandleSwagger():
    def __init__(self, swagger_path: str):
        if swagger_path.endswith('.json'):
            with open(file=swagger_path, mode='r', encoding='utf-8'):
                self.openapi_obj = ParseOpenApi(file_path=swagger_path)
        else:
            raise Exception('请输入正确的swagger json文件')

    def wash_header(self):
        # 清洗请求头信息
        clearList = ["sec-ch-ua-mobile", "sec-ch-ua-platform", "user-agent", "sec-ch-ua",
                     'referer', 'eagleeye-traceid', 'eagleeye-sessionid',
                     'eagleeye-pappname', 'sec-fetch-site', 'sec-fetch-mode',
                     'sec-fetch-dest']
        replaceParametersList = [
            {
                "name": "Auth-Token",
                "in": "header",
                "description": "",
                "required": True,
                "example": "{{auth-token}}",
                "schema": {
                    "type": "string"
                }
            }, {
                "name": "Origin",
                "in": "header",
                "description": "",
                "required": False,
                "example": "{{Base_url}}",
                "schema": {
                    "type": "string"
                }
            }, {
                "name": "Cookie",
                "in": "header",
                "description": "",
                "required": False,
                "example": "{{Cookie}}",
                "schema": {
                    "type": "string"
                }
            }, {
                "name": "Host",
                "in": "header",
                "description": "",
                "required": False,
                "example": "{{host}}",
                "schema": {
                    "type": "string"
                }
            }
        ]
        filterRole = clearList + [name.get('name').lower() for name in replaceParametersList]

        def filter_ele(element: dict, role: list):
            name = element.get('name')
            in_where = element.get('in')
            return not (name.lower() in role and in_where == 'header')

        for api in self.openapi_obj.get_AllApi():
            for method_path, apiValue in api.items():
                for method, detail in apiValue.items():
                    if method.lower() not in ['get']:
                        new_parameters = [element for element in detail['parameters'] if
                                          filter_ele(element, filterRole)] + replaceParametersList
                        detail['parameters'] = new_parameters
        logger.info('清洗header完成！')

    def flowId_replaceBy_path(self):
        # 把以flowId作为key 改成以path作为key 的swagger dict.注意 同path的请求将被合并
        new_paths = {}

        for API in self.openapi_obj.get_AllApi():
            for flowId, apiDetail in API.items():
                for method, detail in apiDetail.items():
                    try:
                        path = detail.get('summary').split(' ')[1]
                        new_paths[path] = apiDetail
                    except:
                        raise Exception('summary格式错误')

        self.openapi_obj.openapi_obj['paths'] = new_paths
        logger.info('flowId_replaceBy_path Done! ')

    def get_openapi_Dict(self):
        # 获取swagger的json对象，一般在操作完后获取
        return self.openapi_obj.to_dict()

    def write_swagger_file(self, swagger_path: str):
        # 把swagger对象写入swagger文件
        with open(file=swagger_path, mode='w', encoding='utf-8') as f:
            json.dump(self.get_openapi_Dict(), f, indent=2)
        logger.info("保存新文件成功！路径：%s" % swagger_path)


if __name__ == '__main__':
    swagger_path = os.path.join(CACHE,'swagger_20240706_101757.json')
    new_swagger_path = os.path.join(CACHE,'swagger_20240706_101757_washed.json')
    swagger_obj = HandleSwagger(swagger_path=swagger_path)
    swagger_obj.wash_header()
    swagger_obj.flowId_replaceBy_path()
    swagger_obj.write_swagger_file(swagger_path=new_swagger_path)
