from datetime import datetime
import re
import json
from mitmproxy import http
import logging

logger = logging.getLogger()


class SaveAsPythonRequestsPlugin:
    def __init__(self):
        self.startStr = """# -*- coding: utf8 -*-
import requests
import json
from faker import Faker
# 创建实例
faker = Faker(locale='zh_CN')

def replay():
\t# 创建一个Session实例
\tsession = requests.Session()
"""
        self.endStr = """
if __name__ == '__main__':
\treplay()
"""
        self.num = 0
        self.urlFilter = r"https://1p-portal-k11-uat.nwplatform.com.cn/portal-uat"
        # self.urlFilter = r"https://1p-portal-testk11-uat.nwplatform.com.cn/portal-uat"
        self.collecter = {}
        logger.info("运行插件 SaveAsPythonRequestsPlugin")

    def request(self, flow: http.HTTPFlow) -> None:
        if re.match(self.urlFilter, flow.request.url):
            if self.num == 0:
                self.collecter['auth-token-code'] = """\tsession.headers.update({'auth-token': '%s'})""" % dict(
                    flow.request.headers).get('auth-token')

            self.collecter[str(flow.id)] = {'name': f'request_{self.num}'}
            logger.debug(f"保存请求：{flow.request.method} {flow.request.url}")

            if flow.request.method == 'POST':
                self.collecter[str(flow.id)][
                    'request'] = (
                            f"\t{self.collecter[str(flow.id)]['name']} = session.post('{flow.request.url}', json={flow.request.text}).json()"
                            + f"\n\tprint('{self.collecter[str(flow.id)]['name']}的结果是',{self.collecter[str(flow.id)]['name']})")
            else:

                self.collecter[str(flow.id)][
                    'request'] = f"\t{self.collecter[str(flow.id)]['name']} = session.{flow.request.method.lower()}('{flow.request.url}', data={json.dumps(flow.request.text)}).json()"
            # request_code = f"\trequest_{self.num} = requests.{flow.request.method.lower()}('{flow.request.url}', headers={json.dumps(dict(flow.request.headers))}, data={json.dumps(flow.request.text)}, cookies={json.dumps(dict(flow.request.cookies))}).json()"

            self.num += 1
        logger.debug(str(self.collecter))

    def response(self, flow: http.HTTPFlow) -> None:
        if re.match(self.urlFilter, flow.request.url):
            self.collecter[str(flow.id)][
                'response'] = f"# {self.collecter[str(flow.id)]['name']}结果： {flow.response.text}"

    def done(self):
        with open(f'{datetime.now().strftime("%Y%m%d_%H%M%S")}.py', 'w', encoding='utf8') as f:
            logger.debug(f"保存文件：{f.name}")
            codes = [v2 for k1 in self.collecter.keys() if k1 != 'auth-token-code' for k2, v2 in
                     self.collecter[k1].items() if k2 in ['request', 'response']]
            result = [self.startStr, self.collecter['auth-token-code']] + codes + [self.endStr]
            f.write('\n'.join(result))


addons = [
    SaveAsPythonRequestsPlugin()
]
