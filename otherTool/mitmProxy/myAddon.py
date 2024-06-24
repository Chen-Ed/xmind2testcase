from datetime import datetime
import re
import json
from mitmproxy import http
from mitmproxy import ctx


class SaveAsPythonRequestsPlugin:
    def __init__(self):
        self.startStr = """import requests
import json

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
        self.collecter = {}
        ctx.log.debug("运行插件 SaveAsPythonRequestsPlugin")

    def request(self, flow: http.HTTPFlow) -> None:
        if re.match(self.urlFilter, flow.request.url):
            self.collecter[str(flow.id)] = {'name': f'request_{self.num}'}
            if self.num == 0:
                self.collecter['auth-token-code'] = """\tsession.headers.update({'auth-token': '%s'})""" % dict(
                    flow.request.headers).get('auth-token')
            ctx.log.debug(f"保存请求：{flow.request.method} {flow.request.url}")
            self.collecter[str(flow.id)][
                'requset'] = f"\t{self.collecter[str(flow.id)]['name']} = session.{flow.request.method.lower()}('{flow.request.url}', data={json.dumps(flow.request.text)}).json()"
            # request_code = f"\trequest_{self.num} = requests.{flow.request.method.lower()}('{flow.request.url}', headers={json.dumps(dict(flow.request.headers))}, data={json.dumps(flow.request.text)}, cookies={json.dumps(dict(flow.request.cookies))}).json()"

            self.num += 1

    def response(self, flow: http.HTTPFlow) -> None:
        if re.match(self.urlFilter, flow.request.url):
            self.collecter[str(flow.id)][
                'response'] = f"# {self.collecter[str(flow.id)]['name']}结果： {flow.response.text}"

    def done(self):
        with open(f'{datetime.now().strftime("%Y%m%d_%H%M%S")}.py', 'w', encoding='utf8') as f:
            ctx.log.debug(f"保存文件：{f.name}")
            codes = [v2 for k1 in self.collecter for k2, v2 in self.collecter[k1].items() if k2 in ['request','response']]
            result = [self.startStr, self.collecter['auth-token-code']] + codes + [self.endStr]
            f.write('\n'.join(result))


addons = [
    SaveAsPythonRequestsPlugin()
]
