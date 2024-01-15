from dataloader.excelAZ import excelAZ
from dataloader.tool.exceltype import STT
import matplotlib.pyplot as plt
import pandas as pd

if __name__ == '__main__':
    timelable = ['报修时间', '到达现场时间', '故障排除时间']
    uselable = ['报修类型','设备系统','位置']
    meslable = ['报修描述','修复状态','报修处理情况','故障类','详细措施','设备']
    system1able = ['中航信离港系统(T1)',  'T1航显系统','T1视频监控系统','工作人员通道人脸识别系统(T1)', 'T1行李系统', 'T1桥载空调', 'T1广播系统','T1登机桥', '内通系统(T1)', 'T1综合布线系统','T1出入口控制系统','泊位引导系统(T1)', 'T1桥载电源', '有线电视系统(T1)', 'T1网络','航班查询系统(T1)', 'T1离港网络', 'T1云平台系统','机坪道口车辆识别系统(T1)', 'T1主网']
    system2lable = ['T2出入口控制系统','内通系统(T2)','T2广播系统','T2航显系统','T2视频监控系统','工作人员通道人脸识别系统(T2)','T2时钟系统','T2东交视频监控系统','有线电视系统(T2)','T2综合布线系统','T2大屏显示系统','T2网络','T2离港网络','T2网络系统']
    system2mod = ['中航信离港系统(T2)','T2出入口控制系统','内通系统(T2)','T2广播系统','T2航显系统','T2视频监控系统','工作人员通道人脸识别系统(T2)','T2时钟系统','T2网络系统','T2东交视频监控系统','有线电视系统(T2)','T2综合布线系统','T2大屏显示系统','T2网络','T2离港网络']
    # '办公自动化系统','全景视频监控系统', '精密空调','云桌面系统','无线对讲机系统,'SITA离港系统'
    print(f'系统总数{len(system2mod)}')
    excelLable = {'timelables':timelable,'uselables':uselable,'meslables':meslable}
    EA = excelAZ(r'C:\Users\ASUS\Desktop\TX0712.xlsx',excelLable)
    # 时间轴创建
    CycleList = {'第一个月':[STT(2023,10,1),STT(2023,11,1),7],'第二个月':[STT(2023,11,1),STT(2023,12,1),1]}
    EA.CycleList(CycleList)
    # print(EA.LayerCount('设备系统').keys().to_list)
    # 业务层(测试用)
    '''
    tableFilter = {'报修时间':[['g',[STT(2023,7,1)]],['l',[STT(2023,10,1)]]]}
    df_sys_qarter1 = EA.tableModify('设备系统', tableFilter)
    tableFilter = {'报修时间': [['g', [STT(2023, 10, 1)]], ['l', [STT(2024, 1, 1)]]]}
    df_sys_qarter2 = EA.tableModify('设备系统', tableFilter)
    EA.DataToOneDf([[df_sys_qarter1,df_sys_qarter2],['2023年第四季度','2024年第一季度']],axis=1)
    EA.Drawbar(title='两季度数据对比表')
    '''
    # 前N个周期
    m_nm = 6
    m_startTine = STT(2023, 10, 1)
    m_endTime = STT(2024,1, 1)
    t_UseCycles_m = [STT(2023, 7 + i, 1) for i in range(m_nm)]
    t_UseCycles_m.append(STT(2024, 1, 1))
    CycleList = {'按周': [m_startTine, m_endTime, 7]}
    t_UseCycles_w = EA.CycleList(CycleList,isReturn=True)['按周']
    CycleList = {'按天': [m_startTine, m_endTime, 1]}
    t_UseCycles_d = EA.CycleList(CycleList,isReturn=True)['按天']

    print(EA.LayerCount('设备系统'))
    print(system2mod)
    use_timeList = t_UseCycles_w
    use_tl_dfls = list()
    for i in range(len(use_timeList)-1):
        m_nt = use_timeList[i]
        m_ft = use_timeList[i+1]
        tableFilter = {'报修时间': [['g', [m_nt]], ['l', [m_ft]]],'设备系统': [['e', system2mod]]}
        use_tl_dfls.append(EA.tableModify('设备系统', tableFilter))
    EA.DataToOneDf([use_tl_dfls,[f'{i.year}年{i.month}月{i.day}日' for i in use_timeList[:-1:]]],axis=1)
    EA.Drawplot(df_lable_ex=system2mod)
