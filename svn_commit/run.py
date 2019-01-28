'''
@moduleName: 
@Author: dawdler
@Date: 2019-01-17 13:58:07
@LastModifiedBy: dawdler
@LastEditTime: 2019-01-24 18:00:05
'''

#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
import time
import os
from config import setting, svn_list
_svn_url = setting['svn']
_logFile = setting['logFile']
logs = []

# 进入SVN所在目录
os.chdir(_svn_url)


# 执行npm包打包,并提交SVN


def npmInstall():
    for path in svn_list:
        _path = 'cd '+path+' & '
        # 删除dist目录
        _cmd = _path+'svn delete --force static/dist/*'
        os.system(_cmd)
        logs.append('----- 删除dist目录结束 ---------- \n')
        # 执行打包
        _path = 'cd '+(path+'/vue')+' & '
        _cmd = _path+'npm run build'
        log = '开始执行npm打包：' + path
        logs.append(log+'\n')
        os.system(_cmd)
        logs.append('----- npm打包单次循环结束 ---------- \n')
        _path = 'cd '+path+' & '
        _cmd = _path+'svn add . --force & svn delete static/dist & svn add static/dist & svn add vue/static & svn add react/src & svn delete --force static/dist/js/config.js & svn ci -m "自动打包提交"'
        os.system(_cmd)
        logs.append('----- 提交结束 ---------- \n')


# 执行svn更新
def update_svn():
    # 清空日志
    logs.clear()
    # 日志打印更新时间
    for path in svn_list:
        _cmd = 'cd '+path+' & svn update'
        log_time = time.strftime('%Y-%M-%D %H:%M:%S', time.localtime())
        log = '输出：'+path+'\ntime:'+log_time+'\n'
        logs.append(log)
        update_result = os.system(_cmd)
        # 日志输出
        if update_result == 0:
            log = '更新成功:'+path+'\n'
            npmInstall()
        else:
            log = '更新失败：'+path+'\n'

    # 循环写入日志
    with open(_logFile, 'a') as f:
        logs.append('------------- 日志写入单次循环结束 -------------- \n')
        for l in logs:
            f.write(l)

    logs.clear()


if __name__ == '__main__':
    update_svn()
