from common.comm import *
from common.schema_har import SCHEMA_HAR
import json
from jsonpath_ng import parse


class HandleHar():
    def __init__(self, har_path: str):
        if har_path.endswith('.har'):
            with open(file=har_path, mode='r', encoding='utf-8') as har:
                self.har_obj = json.load(har)
                vailidata_OpenAPI(self.har_obj, SCHEMA_HAR)
        else:
            raise Exception('请输入正确的 har 文件')

    def wash_cookies(self):
        # 清洗cookies
        path_expression = parse("$.log.entries[*].request.cookies")
        matchs = path_expression.find(self.har_obj)
        for i, cookie in enumerate(matchs):
            matchs[i].full_path.update(self.har_obj, [])
        logger.info('清洗cookies完成！')

    def wash_header(self):
        # 清洗header
        clear_keys = ["sec-ch-ua-mobile", "sec-ch-ua-platform", "user-agent", "sec-ch-ua", 'referer',
                      'eagleeye-traceid',
                      'eagleeye-sessionid', 'eagleeye-pappname', 'sec-fetch-site', 'sec-fetch-mode', 'sec-fetch-dest']
        replace_keys = ["cookie", "origin", "auth-token", 'host']
        path_expression = parse("$.log.entries[*].request.headers")
        matchs = path_expression.find(self.har_obj)
        for i, header in enumerate(matchs):
            new_headers = []

            for kv in header.value:
                # 需要替换的键值对
                for r_k in replace_keys:
                    if kv["name"].lower() == r_k:
                        new_headers.append(
                            {
                                "name": kv["name"],
                                "value": "{{%s}}" % r_k
                            }
                        )
                        break
                # 需要保留的键值对
                if kv["name"].lower() in clear_keys or kv["name"].lower() in replace_keys:
                    pass
                else:
                    new_headers.append(kv)
            matchs[i].full_path.update(self.har_obj, new_headers)
        logger.info('清洗header完成！')

    def get_openapi_Dict(self):
        # 获取har的json对象，一般在操作完后获取
        return self.har_obj

    def write_har_file(self, path: str):
        # 把har dict对象写入文件
        with open(file=path, mode='w', encoding='utf-8') as f:
            json.dump(self.get_openapi_Dict(), f, indent=2)
        logger.info("保存新文件成功！路径：%s" % path)


if __name__ == '__main__':
    har_path = os.path.join(CACHE, r'har_20240705_105726.har')
    new_har_path = os.path.join(CACHE, r'har_20240705_105726_washed.har')
    har_obj = HandleHar(har_path=har_path)
    har_obj.wash_cookies()
    har_obj.wash_header()
    har_obj.write_har_file(path=new_har_path)
