import requests
import json
import os
from datetime import datetime
import csv
from time import sleep
from common import retry


class dataIter():
    def __init__(self, auth_token, requestFUNC, base_url, delay=0) -> None:
        self.page = 1
        self.auth_token = auth_token
        self.requestFUNC = requestFUNC
        self.base_url = base_url
        self.delay = delay
        pass

    def __iter__(self):
        return self

    def __next__(self):
        print(f'正在采集{self.requestFUNC.__name__}第{self.page}页')
        dataStore = self.requestFUNC(self.page, self.auth_token, self.base_url)
        sleep(self.delay)

        if dataStore == [] or dataStore is None:
            print('没有数据了，采集结束。')
            raise StopIteration
        else:
            self.page += 1
            return dataStore


@retry(tries=3, delay=5, backoff=1.5)
def company_id(page, auth_token, base_url) -> list:
    url = f"{base_url}/portal/company/get-company-list"

    payload = json.dumps({
        "page": page,
        "page_size": 50,
        "name": ""
    })
    headers = {
        'lang': 'zh',
        'accept': 'application/json, text/plain, */*',
        'Cookie': '',
        'origin': 'https://1p-portal-testk11-uat.nwplatform.com.cn',
        'referer': 'https://1p-portal-testk11-uat.nwplatform.com.cn/setting/projectManage',
        'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'auth-token': auth_token,
        'connection': 'keep-alive',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'content-type': 'application/json',
        'content-length': '35',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'accept-encoding': 'gzip, deflate, br, zstd',
        'accept-language': 'zh-CN,zh',
        'x-postman-captr': '1825884',
        'eagleeye-traceid': '6744777c1717484015405103220af3',
        'sec-ch-ua-mobile': '?0',
        'eagleeye-pappname': 'cn0ivyw0th@972842a8cc20af3',
        'eagleeye-sessionid': 'zml5OxXt0dn13blsjxOsibbzw781',
        'sec-ch-ua-platform': '"Windows"'
    }

    response = requests.request("POST", url, headers=headers, data=payload).json()
    assert response['code'] == 200
    return [[i['guid']] for i in response['data']['list']]


@retry(tries=3, delay=5, backoff=1.5)
def project_id(page, auth_token, base_url) -> list:
    url = f"{base_url}/portal/user/get-user-project-list"

    payload = json.dumps({
        "page": page,
        "page_size": 200
    })
    headers = {
        'lang': 'zh',
        'accept': 'application/json, text/plain, */*',
        'Cookie': '',
        'origin': 'https://1p-portal-testk11-uat.nwplatform.com.cn',
        'referer': 'https://1p-portal-testk11-uat.nwplatform.com.cn/',
        'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'auth-token': auth_token,
        'connection': 'keep-alive',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'content-type': 'application/json',
        'content-length': '26',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'accept-encoding': 'gzip, deflate, br, zstd',
        'accept-language': 'zh-CN,zh',
        'x-postman-captr': '338222',
        'eagleeye-traceid': '6744777c1717483965989100420af3',
        'sec-ch-ua-mobile': '?0',
        'eagleeye-pappname': 'cn0ivyw0th@972842a8cc20af3',
        'eagleeye-sessionid': 'zml5OxXt0dn13blsjxOsibbzw781',
        'sec-ch-ua-platform': '"Windows"'
    }

    response = requests.request("POST", url, headers=headers, data=payload).json()

    assert response['code'] == 200
    return [[i['guid']] for i in response['data']['list']]


# @retry(tries=3, delay=5, backoff=1.5)
# def staff_id(page, auth_token, base_url) -> list:
#     """用户id
#
#     Args:
#         page (_type_): _description_
#         auth_token (_type_): _description_
#
#     Returns:
#         list: _description_
#     """
#     url = f"{base_url}/portal/user/get-user-list"
#
#     payload = json.dumps({
#         "page": page,
#         "page_size": 200,
#         "name": "",
#         "is_show": 1,
#         "status": "*"
#     })
#     headers = {
#         'Accept': 'application/json, text/plain, */*',
#         'Accept-Language': 'zh-CN,zh',
#         'Cache-Control': 'no-cache',
#         'Connection': 'keep-alive',
#         'Origin': 'https://1p-portal-testk11-uat.nwplatform.com.cn',
#         'Pragma': 'no-cache',
#         'Referer': 'https://1p-portal-testk11-uat.nwplatform.com.cn/setting/staffStructure',
#         'Sec-Fetch-Dest': 'empty',
#         'Sec-Fetch-Mode': 'cors',
#         'Sec-Fetch-Site': 'same-origin',
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
#         'auth-token': auth_token,
#         'lang': 'zh',
#         'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
#         'sec-ch-ua-mobile': '?0',
#         'sec-ch-ua-platform': '"Windows"',
#         'Content-Type': 'application/json'
#     }
#
#     response = requests.request("POST", url, headers=headers, data=payload).json()
#
#     assert response['code'] == 200
#     return [i['guid'] for i in response['data']['list']]


@retry(tries=3, delay=5, backoff=1.5)
def role_id(page, auth_token, base_url) -> list:
    """角色id

    Args:
        page (_type_): _description_
        auth_token (_type_): _description_

    Returns:
        list: _description_
    """
    url = f"{base_url}/portal/role/permission-role-list"

    payload = json.dumps({
        "name": "",
        "code": "",
        "type": "",
        "page": page,
        "page_size": 200,
        "get_assign": 0
    })
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Pragma': 'no-cache',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'auth-token': auth_token,
        'lang': 'zh',
        'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }

    response = requests.request("POST", url, headers=headers, data=payload).json()

    assert response['code'] == 200
    return [[i['guid']] for i in response['data']['list']]


@retry(tries=3, delay=5, backoff=1.5)
def app_id(page, auth_token, base_url) -> list:
    """应用id

    Args:
        page (_type_): _description_
        auth_token (_type_): _description_

    Returns:
        list: _description_
    """
    if page == 1:
        url = f"{base_url}/portal/setting/get-application-list"

        payload = json.dumps({})
        headers = {
            'lang': 'zh',
            'accept': 'application/json, text/plain, */*',
            'origin': 'https://1p-portal-testk11-uat.nwplatform.com.cn',
            'referer': 'https://1p-portal-testk11-uat.nwplatform.com.cn/',
            'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            'auth-token': auth_token,
            'connection': 'keep-alive',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
            'content-type': 'application/json',
            'content-length': '2',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'zh-CN,zh',
            'x-postman-captr': '5987113',
            'eagleeye-traceid': '6744777c1717483965987100220af3',
            'sec-ch-ua-mobile': '?0',
            'eagleeye-pappname': 'cn0ivyw0th@972842a8cc20af3',
            'eagleeye-sessionid': 'zml5OxXt0dn13blsjxOsibbzw781',
            'sec-ch-ua-platform': '"Windows"'
        }

        response = requests.request("POST", url, headers=headers, data=payload).json()

        assert response['code'] == 200
        return [[i['guid']] for i in response['data']['list']]
    else:
        return []


# @retry(tries=3, delay=5, backoff=1.5)
def department_id(auth_token, base_url, colleter, parent_id) -> list:
    """递归收集部门id

    Args:
        page (_type_): _description_
        auth_token (_type_): _description_

    Returns:
        list: _description_
    """
    url = f"{base_url}/portal/department/get-dept-list"
    if parent_id == 0:
        payload = {
            "page": 1,
            "page_size": 200,
            "name": "",
            "is_show": 1,
            "data_source": [
                "PORTAL",
                "SAP",
                "LMS",
                "AAS"
            ],
            "parent_id": 0
        }
    else:
        payload = {
            "page": 1,
            "is_show": 1,
            "data_source": [
                "PORTAL",
                "SAP",
                "LMS",
                "AAS"
            ],
            "parent_id": parent_id
        }
    headers = {
        'lang': 'zh',
        'accept': 'application/json, text/plain, */*',
        'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'auth-token': auth_token,
        'connection': 'keep-alive',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'content-type': 'application/json',
        'content-length': '61',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'accept-encoding': 'gzip, deflate, br, zstd',
        'accept-language': 'zh-CN,zh',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }

    response = requests.request("POST", url, headers=headers, data=json.dumps(payload), timeout=60000).json()

    assert response['code'] == 200, '请求失败！'
    dpids = [i['guid'] for i in response['data']['list']]
    for id in dpids:
        if id != []:
            colleter.update(dpids)
            print(len(colleter), id)
            department_id(auth_token, base_url, colleter, parent_id=id)


@retry(tries=3, delay=5, backoff=1.5)
def usr_info(page, auth_token, base_url) -> list:
    """用户id

    Args:
        page (_type_): _description_
        auth_token (_type_): _description_

    Returns:
        list: _description_
    """
    url = f"{base_url}/portal/user/get-user-list"

    payload = json.dumps(
        {
            "page": page,
            "page_size": 200,
            "name": "",
            "is_show": 1,
            "status": "*",
            "data_source": [
                "PORTAL",
                "SAP",
                "LMS",
                "AAS"
            ]
        }
    )
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        # 'Origin': 'https://1p-portal-testk11-uat.nwplatform.com.cn',
        'Pragma': 'no-cache',
        # 'Referer': 'https://1p-portal-testk11-uat.nwplatform.com.cn/setting/staffStructure',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'auth-token': auth_token,
        'lang': 'zh',
        'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload).json()

    assert response['code'] == 200 , f'response.code!=200 请求失败！\n response={response}'
    res = [[i['guid'], i['email'], i['phone'], i['status'], i.get('system_status'), i.get('resign_state'), i['name'],
            i['en_name'], i['chinese_name'], i['department_guid']] for i in response['data']['list']]
    if page == 1:
        res.insert(0, ['guid', 'email', 'phone', 'status', 'system_status', 'resign_state', 'name', 'en_name',
                       'chinese_name', 'department_guid'])
    return res


# 获取公司、角色、应用、项目ID、用户数据
if __name__ == '__main__':
    # base_url = 'https://k11.xigmapas.com/portal-pro'
    base_url = 'https://1p-portal-k11-uat.nwplatform.com.cn/portal-uat'
    # base_url = 'https://1p-portal-testk11-uat.nwplatform.com.cn/portal-uat'
    auth_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJsdWNhc19BIiwiYnVfZ3VpZCI6Ijk5NWY5ZDViNWE5MTExZWQ4NDUwMDAxNjNlMTc1NGFlIiwidXNlcl90eXBlIjoic3RhZmYiLCJ1c2VyX2d1aWQiOiJlNzVlMzNmNDQxOTc0ZWY5OTVhNzQzNTgxNmI2ZGNlOCIsImp0aSI6IjEyYjVhNzMzNGRkYzQ0YzJiYmZmZmE0NTdkZGQyMjkxIn0.uL61COH1u4_PHaLargrA3DsvuIwXSXJY6FL7Bb5L4Fo'

    dirName = datetime.date(datetime.now()).strftime("%Y年%m月%d日")
    dirPath = os.path.join(f'C:/Users/te_chenyingdong/Desktop', dirName)
    if os.path.exists(dirPath) is False:
        os.mkdir(dirPath)
    for f in [company_id,project_id,role_id,app_id]:
    # for f in [usr_info]:
        ids = dataIter(auth_token, usr_info, base_url)
        dataStore = []
        try:
            for i in ids:
                dataStore.extend(i)
                print(f"共收集用户数据{len(dataStore)}条")
        except:
            print(f'获取数据失败！')
            pass
        finally:
            fileName = str(f.__name__) + datetime.now().strftime('%Y%m%d_%H%M%S') + '.csv'
            csv_file = os.path.join(dirPath, fileName)
            with open(csv_file, mode='w+', newline='', encoding='utf8') as file:
                writer = csv.writer(file)
                writer.writerow([f.__name__])
                for i in dataStore:
                    writer.writerow(i)

    # 获取部门ID
    # dataStore = set()
    # # for i in ['5f459906889b47dba5a9eb8e4c0238fb','2f4dfea40a4946baadef452fec0ee7e6']:
    # #     department_id(auth_token=auth_token,base_url=base_url,colleter=dataStore,parent_id=i)
    # department_id(auth_token=auth_token, base_url=base_url, colleter=dataStore, parent_id=0)
    # print(len(dataStore))
    # fileName = str(department_id.__name__) + datetime.now().strftime('%Y%m%d_%H%M%S') + '.csv'
    # csv_file = os.path.join(dirPath, fileName)
    # with open(csv_file, mode='w+', newline='') as file:
    #     writer = csv.writer(file)
    #     writer.writerow([department_id.__name__])
    #     for i in dataStore:
    #         writer.writerow([i])
