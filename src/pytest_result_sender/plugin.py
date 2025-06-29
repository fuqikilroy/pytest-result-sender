

import pytest
from datetime import datetime, timedelta

data={
    "passed":0,
    "failed":0
}

def pytest_runtest_logreport(report:pytest.TestReport):
    if report.when == 'call':
        # print("本次用例的执行结果",report.outcome)
        data[report.outcome] +=1


def pytest_collection_finish(session:pytest.Session):
    # print(session.items)
    data['total'] =len(session.items)
    print('用例的总数:',data['total'])

def pytest_configure():
    #配置加载完毕之后执行，所有测试用例执行前执行
    data['start_time']=datetime.now()
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






















