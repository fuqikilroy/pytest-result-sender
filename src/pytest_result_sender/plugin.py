

import pytest
from datetime import datetime, timedelta

from urllib3 import request

data={
    "passed":0,
    "failed":0
}

def pytest_addoption(parser):
    parser.addini(
        'send_when',
        help = "什么时候发送测试结果，every表示每次，on_fail表示只有失败时"
    )
    parser.addini(
        'api',
        help = "发往api接口地址"
    )


def pytest_runtest_logreport(report:pytest.TestReport):
    if report.when == 'call':
        # print("本次用例的执行结果",report.outcome)
        data[report.outcome] +=1


def pytest_collection_finish(session:pytest.Session):
    # print(session.items)
    data['total'] =len(session.items)
    print('用例的总数:',data['total'])

def pytest_configure(config:pytest.Config):
    #配置加载完毕之后执行，所有测试用例执行前执行
    data['start_time']=datetime.now()
    data['send_when']=config.getini("send_when")
    data['send_api']=config.getini("send_api")
    # print(f'{datetime.now()}pytest开始执行')


def pytest_unconfigure():
    # 配置加载完毕之后执行，所有测试用例执行后执行
    data['end_time']=datetime.now()

    data['duration']=data['end_time']-data['start_time']
    data['pass_ratio'] = data['passed']/data['total']*100
    data['pass_ratio'] = f"{data['pass_ratio']:.2f}%"

    # print(f'{datetime.now()}pytest结束执行')
    assert timedelta(seconds=3)>data['duration']>= timedelta(seconds=2.5)
    assert data['total']==3
    assert data['passed']==2
    assert data['failed']==1
    assert data['pass_ratio']== "66.67%"

    send_result()

def send_result():
    if data['send_when'] == 'on_fail' and data['failed'] == 0:
        return
    if not data['send_api']:
        return

    url= data['send_api'] # 动态指定api地址

#   pytest测试结果发送
    content= f"""  发送api的内容，json格式  """

    try:
        request.post(url,json={"msgtype":"markdown",
                               "markdown":{"content":content}})
    except Exception:
        pass
    data['send_done'] = 1 #测试完发送后记录






















