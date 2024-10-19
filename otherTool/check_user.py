# -*- coding: utf8 -*-
import csv

import requests
from faker import Faker
from datetime import datetime
from loguru import logger
from common.comm import check_status_code
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from otherTool.save_Ids import usr_info, dataIter

# 创建实例
faker = Faker(locale='zh_CN')

# 临时变量
today = datetime.date(datetime.now()).strftime('%Y%m%d')[2:]
caseName = '%s_%s_%d' % (Path(__file__).name, today, faker.random_int(min=1000, max=9999))
parent_department_id = None
user_id = None
role_id = None
app_id = None
project_id = None
company_id = None
announcement_id = None
bu_id = None
Base_url = None
department_id = None
position_id = None
# 设置日志模块
logger.add(f'{caseName}_py.log', format="{time} {level} {message}", level="DEBUG")


def save_usr_id(baseUrl, token, dirPath):
    ids = dataIter(auth_token=token, requestFUNC=usr_info, base_url=baseUrl)
    dataStore = []
    try:
        for i in ids:
            dataStore.extend(i)
            print(f"共收集用户数据{len(dataStore)}条")
    except Exception as e:
        print(f'获取数据失败！')
        logger.error(e)
    assert len(dataStore) > 0, '未获取到用户数据'
    csv_file = Path(dirPath) / f"{str(usr_info.__name__)}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(csv_file, mode='w+', newline='', encoding='utf8') as file:
        writer = csv.writer(file)
        writer.writerow([usr_info.__name__])
        for i in dataStore:
            writer.writerow(i)


def replay(baseUrl, token, staff_id):
    # 创建一个Session实例
    session = requests.Session()
    session.headers.update({'auth-token': token,
                            'Host': '1p-portal-k11-uat.nwplatform.com.cn',
                            'Origin': 'https://1p-portal-k11-uat.nwplatform.com.cn',
                            # 'Cookie': 'HWWAFSESID=c46587333472977fef; HWWAFSESTIME=1724147976691; _bl_uid=8bm6h0hw2nv9j867wvvqpt7iOwCC',
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0'})
    # 开始重放

    request_0 = session.post(f'{baseUrl}/portal/auth/get-password-policy', json={})
    logger.info(('request_0响应：%s' % request_0.json())[:3000])
    check_status_code(request_0, logger)
    # request_0结果： {"data":{"guid":"2ee173c2541b001ab9ed8ecf4be42a6d","bu_guid":"995f9d5b5a9111ed845000163e1754ae","bu_name":"K11","user_type":"staff","min_length":null,"contain_digit":false,"contain_letter":false,"contain_upper_letter":false,"contain_lower_letter":false,"contain_symbol":false,"enabled_rotate":false,"forced_cycle":null,"remind_cycle":null,"created_at":null,"updated_at":"2024-05-21 16:18:13"},"code":200,"msg":"success.","trace_id":null}

    request_1 = session.post(f'{baseUrl}/portal/user/get-user-data',
                             json={"staff_id": staff_id})
    logger.info(('request_1响应：%s' % request_1.json())[:3000])
    check_status_code(request_1, logger)
    # request_1结果： {"data":{"area_guid":"","account_type":"staff","fix_phone":"","department_id":null,"title":"","staff_no":"lucas_C","fix_phone_area_code":"","is_admin":0,"status":1,"user_type":"staff","position_guid":"","alias":"","email":"lucas_c@lucas.com","leader_guid":"","login_id":"","join_date":"","sex":null,"department_name":null,"position_name":null,"department_guid":"7089795e1eee4f369947653379f5b97b","avatar":"","role_name":null,"lease_project_guid":null,"phone":null,"resign_date":"","company_name":null,"name":"lucas_C","en_name":"","guid":"9d61fc7d598c459983dc2b5322c479a2","source_id":"","company_guid":"","system_status":1,"phone_area_code":"","created_at":"2024-06-03 16:40:11","updated_at":"2024-08-08 10:48:59","created_by":"system","updated_by":"system","email_address":"lucas_c@lucas.com","chinese_name":""},"code":200,"msg":"success.","trace_id":null}
    department_guid = request_1.json()['data']['department_guid']

    request_2 = session.post(f'{baseUrl}/portal/user/check-ad', json={"staff_id": staff_id})
    logger.info(('request_2响应：%s' % request_2.json())[:3000])
    check_status_code(request_2, logger)
    # request_2结果： {"data":{"is_ad":0},"code":200,"msg":"success.","trace_id":null}

    request_3 = session.post(f'{baseUrl}/portal/user/get-user-role',
                             json={"staff_id": staff_id, "role_type": "common"})
    logger.info(('request_3响应：%s' % request_3.json())[:3000])
    check_status_code(request_3, logger)
    # request_3结果： {"data":{"list":[{"role_name":"LEASE管理员","leasing_project_guid":"0","role_guid":"00e8e155f28a4524aa23070534dd2d52","lease_project_guid":"0","role_type":"common","relate_guid":"9d61fc7d598c459983dc2b5322c479a2","guid":"fb09639f0d7346a58db11ac31e784a7d","created_at":"2024-08-12 21:05:33","creator_name":"system","created_by":"system"},{"role_name":"系统管理员","leasing_project_guid":"0","role_guid":"5c9ffc5c0fd44c8f8361e13a6820452a","lease_project_guid":"0","role_type":"common","relate_guid":"9d61fc7d598c459983dc2b5322c479a2","guid":"801ebedb6b4d4078ae898322b4e617d9","created_at":"2024-08-06 11:35:44","creator_name":"system","created_by":"system"},{"role_name":"SOPI管理员","leasing_project_guid":"0","role_guid":"258b4b0e11c44773b9b0de9cb5e857c2","lease_project_guid":"0","role_type":"common","relate_guid":"9d61fc7d598c459983dc2b5322c479a2","guid":"3ef440f6f6534c449193a6d486050168","created_at":"2024-07-15 10:04:56","creator_name":"system","created_by":"system"},{"role_name":"workspace应用","leasing_project_guid":"0","role_guid":"2e0fbbf4daf6457e9f246c50aca22dd3","lease_project_guid":"0","role_type":"common","relate_guid":"9d61fc7d598c459983dc2b5322c479a2","guid":"3620a5f1f9004a5182ea2dc688eba0c0","created_at":"2024-06-26 18:29:37","creator_name":"system","created_by":"system"},{"role_name":"PMS管理员","leasing_project_guid":"0","role_guid":"289e21bd65b54468bbaeafe946897af3","lease_project_guid":"0","role_type":"common","relate_guid":"9d61fc7d598c459983dc2b5322c479a2","guid":"262a80fbb12341dcb33310f0d8bacdd0","created_at":"2024-07-11 15:20:43","creator_name":"system","created_by":"system"},{"role_name":"lucasABCD","leasing_project_guid":"0","role_guid":"2e1f54f82638433e8e152c49ad869ef1","lease_project_guid":"0","role_type":"common","relate_guid":"9d61fc7d598c459983dc2b5322c479a2","guid":"219ec33e6123466ca43bbf2fdbbc3d04","created_at":"2024-07-10 10:09:16","creator_name":"system","created_by":"system"}],"has_next":0,"count":6},"code":200,"msg":"success.","trace_id":null}

    request_4 = session.post(f'{baseUrl}/portal/user/get-user-role',
                             json={"staff_id": staff_id, "role_type": "project"})
    logger.info(('request_4响应：%s' % request_4.json())[:3000])
    check_status_code(request_4, logger)
    # request_4结果： {"data":{"list":[{"role_name":"PM PMS 管理员","leasing_project_guid":"988c11ce836a4fb986bdcf8f532ea559","role_guid":"8801381b42e947c3a0d64de624550752","lease_project_guid":"988c11ce836a4fb986bdcf8f532ea559","role_type":"project","relate_guid":"9d61fc7d598c459983dc2b5322c479a2","guid":"eb18671969eb41958ae468942ac6ceb4","created_at":"2024-07-11 15:26:48","creator_name":"system","project_city_name":"天津城区","project_name":"天津 K11","created_by":"system"},{"role_name":"Leasing管理员","leasing_project_guid":"3bfaa8ef81a8429698938a3d600ee133","role_guid":"c714777d101e48018063d372eda51b71","lease_project_guid":"3bfaa8ef81a8429698938a3d600ee133","role_type":"project","relate_guid":"9d61fc7d598c459983dc2b5322c479a2","guid":"4ea19a831dcd476ca1d3a2c1ffbdecec","created_at":"2024-07-11 10:16:26","creator_name":"system","project_city_name":"广州市","project_name":"广州 K11","created_by":"system"}],"has_next":0,"count":2},"code":200,"msg":"success.","trace_id":null}

    if department_guid:
        request_5 = session.post(f'{baseUrl}/portal/department/get-dept-parent-name',
                                 json={"department_id": department_guid})
        logger.info(('request_5响应：%s' % request_5.json())[:3000])
        check_status_code(request_5, logger)
    # request_5结果： {"data":["QA"],"code":200,"msg":"success.","trace_id":null}

    request_6 = session.post(f'{baseUrl}/portal/auth/get-token-expires', json={
        "token": token})
    logger.info(('request_6响应：%s' % request_6.json())[:3000])
    check_status_code(request_6, logger)
    # request_6结果： {"data":{"expiration_time":"2024-08-21 13:13:18"},"code":200,"msg":"success.","trace_id":null}


def process_user(user_id, error_list, baseUrl, token):
    try:
        replay(
            baseUrl=baseUrl,
            token=token,
            staff_id=user_id
        )
        return True
    except Exception as e:
        logger.error(f'检查id时出现错误 {user_id}: {e}')
        error_list.append((user_id, str(e)))
        return False


if __name__ == '__main__':
    # base_url = 'https://k11.xigmapas.com/portal-pro'
    base_url = 'https://1p-portal-k11-uat.nwplatform.com.cn/portal-uat'
    # base_url = 'https://1p-portal-testk11-uat.nwplatform.com.cn/portal-uat'
    auth_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJMdWNhcyBDaGVuIFlpbmcgRG9uZyAoTldDUykiLCJidV9ndWlkIjoiOTk1ZjlkNWI1YTkxMTFlZDg0NTAwMDE2M2UxNzU0YWUiLCJ1c2VyX3R5cGUiOiJzdGFmZiIsInVzZXJfZ3VpZCI6ImZkMzhiZjRmNDRhNDQwMzRhNjRlZDkzOTMwYThhZTdlIiwianRpIjoiNGM1YTUzYjIxODdlNGI4MzhmYjg0ZTg1YzlhZDc4MDQifQ.kChFwjv5KtqrLQSoX8YtmDVEeor9vGr3iU0sBvJ-4o0'

    error = []
    passUser = 0
    max_workers = 10

    dirPath = Path.home() / 'Desktop' / datetime.date(datetime.now()).strftime("%Y年%m月%d日")
    dirPath.mkdir(exist_ok=True)

    if cache := False:
        logger.info('清理所有数据后重新爬取数据')
        for f in dirPath.glob(f'{str(usr_info.__name__)}*.csv'):
            f.unlink()
        save_usr_id(baseUrl=base_url, token=auth_token, dirPath=dirPath)

    csv_file = [i for i in dirPath.glob(f'{str(usr_info.__name__)}*.csv')][0]

    with open(csv_file, 'r', encoding='utf-8') as csvfile:
        # 创建 csv.reader 对象
        reader = csv.reader(csvfile)
        # 忽略第一行
        next(reader)
        # 获取第二行作为列标题
        fieldnames = next(reader)
        # 创建 csv.DictReader 对象，使用第二行作为字段名
        dict_reader = csv.DictReader(csvfile, fieldnames=fieldnames)
        user_ids = [row['guid'] for row in dict_reader]
        total = len(user_ids)

        # 使用线程池处理用户
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(process_user, user_id, error, base_url, auth_token): user_id for user_id in
                       user_ids}
            for future in as_completed(futures):
                user_id = futures[future]
                result = future.result()
                if result:
                    passUser += 1
                    logger.info(f'检查进度: {passUser / len(user_ids) * 100:.2f}%')
    logger.info(f'Total errors: {len(error)}')
    logger.info(f'Errors: {error}')
