
def get_GiteeMission(PJ_name, needs:list):
    """
    把gitee需求 转为 自己的gitee任务
    """
    print(get_GiteeMission.__doc__.strip().center(60, '*'))
    missions = []
    missions.append(f'【{PJ_name}】 功能测试')
    missions.append(f'【{PJ_name}】 回归测试')
    missions.append(f'【{PJ_name}】 用例设计')
    missions += [f"""【{PJ_name}】 #{i} 功能测试""" for i in needs]

    print('\n'.join(missions))


def get_XmindMission(Model, needs: list):
    """
    把gitee需求 转为 xmind8标题
    """
    print(get_XmindMission.__doc__.strip().center(60, '*'))

    missions = [f"""{Model}#{i}""" for i in needs]
    print('\n'.join(missions))

if __name__ == '__main__':
    needs = """IK97	AD账号手机号码自动带出
IKPS	应用开放权限问题设置
IL0D	应用列表补充应用分类
IL8T	应用列表补充搜素功能，搜索应用名称
ILAS	应用列表补充两个HR弹窗应用迁移
ILAV	旧WordSpace需要更换接口显示内容
ILAX	角色权限配置，由于应用量较多，需要进行分区进行查看
ILEN	Cityray接入Xigma Portal
ILEO	TalentPlus接入Xigma Portal
ILGZ	【portal】修改有效邮件的校验规则支持nw-si
""".strip().replace('	',' ').split('\n')
    get_GiteeMission('XC-Portal 2.1.6', needs)
    get_XmindMission('Portal/2.1.6/', needs)