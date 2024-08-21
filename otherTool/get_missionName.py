def get_GiteeMission(PJ_name, needs: list):
    """
    把gitee需求 转为 自己的gitee任务
    """
    print(get_GiteeMission.__doc__.strip().center(60, '*'))
    missions = []
    missions.append('【测试】' + f'【{PJ_name}】 功能测试')
    missions.append('【测试】' + f'【{PJ_name}】 用例执行')
    missions.append('【测试】' + f'【{PJ_name}】 回归测试')
    missions.append('【测试】' + f'【{PJ_name}】 用例设计')
    missions += ['【测试】' + f"""【{PJ_name}】#{i} 功能测试""" for i in needs]

    print('\n'.join(missions))


def get_XmindMission(Model, needs: list):
    """
    把gitee需求 转为 xmind8标题
    """
    print(get_XmindMission.__doc__.strip().center(60, '*'))

    missions = [f"""{Model}#{i}""" for i in needs]
    print('\n'.join(missions))


if __name__ == '__main__':
    needs = """IJW8	IP安全围栏
IMND	部门组织架构过滤PMS来源的层级树
IMNF	PORTAL显示的人员状态字段调整
IMVB	补充旧有应用入口和权限至XigmaCloud应用中心
IMWJ	增加BU标识，方便用户知晓当前登录的BU
IMYA	E-LEASING入口应用补充至XC

""".strip().replace('	', ' ').split('\n')
    get_GiteeMission('XC-Portal 2.2.1', needs)
    get_XmindMission('Portal/2.2.1/', needs)
