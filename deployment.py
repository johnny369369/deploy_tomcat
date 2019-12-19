#!/usr/bin/python env
# -*- coding: utf-8 -*-
import sys,os,re
from fabric.connection import Connection
import patchwork.transfers
import patchwork.info
from fabric.transfer import *
import time,yaml,invoke,pysnooper
import xml.etree.cElementTree as ET
from patchwork.files import exists
# from fabric.decorators import runs_once
from invoke import runners

@pysnooper.snoop('logs/fab.log')
class All_params(object):
    colour_list = {
        'red': 31,
        'green': 32,
        'yellow': 33,
        'blue': 34,
        'purple_red': 35,
        'bluish_blue': 36,
        'white': 37,
    }
    @staticmethod
    def display(msg, colour='white'):
        try:
            choice = All_params.colour_list.get(colour)
            if choice:
                info = "\033[1;{};1m{}\033[0m".format(choice, msg)
                return info
            else:
                return False
        except Exception as e:
            print(e.__str__())

    @staticmethod
    def check_input(msg,result = []):
        def entry(msg):
            ret = input('请选择{},或输入q退出: '.format(msg)).strip()
            return ret
        choice = entry(msg)
        result.append(choice)
        if not choice:
           check_input(msg)
        else:
            if choice == 'q':
               sys.exit(0)
        return result[-1]

    @staticmethod
    def input_ck(data,title):
        try:
            user_input = ''
            while user_input.strip() not in data:
                for key_id in data:
                    print('\t',key_id,data[key_id])
                user_input = input(f'请选择{title},或输入q退出:').strip()
                if user_input == 'q':
                    sys.exit(1)
            return user_input.strip()
        except Exception as e:
            print(e)

try:
    with open('conf/project_list.yml', 'r', encoding='utf-8') as f:
        loadfile = yaml.load(f)
except Exception as e:
    print(All_params.display(f'Error:文件读取失败:{e.__str__()}', 'red'))

class Fab(object):
    def __init__(self,project_name='Dnspod',svn_version=None,tomcat_version='8.0'):
        self.user = 'root'
        self.password = '123456'
        self.project_name = project_name
        self.source_path = os.getcwd() + '/project_code'
        self.local_conf_dir = os.getcwd() + '/project_conf'
        self.svn_path = loadfile[self.project_name]['svn_path']
        self.svn_version = svn_version
        self.hosts = loadfile[self.project_name]['hosts']
        self.exclude = loadfile[self.project_name]['exclude_opts']
        self.restart_cmd = loadfile[self.project_name]['restart_cmd']
        self.date = time.strftime("%Y-%m-%d %H:%M", time.localtime())
        self.tmp_dir = os.getcwd() + '/project_tmp_dir'
        self.tomcat_version = tomcat_version

        try:
            for host in self.hosts:
                self.c = Connection(self.user + '@' + host, connect_kwargs={"password":self.password},connect_timeout=5)
        except Exception as e:
            print(All_params.display(f'Error:服务器连接异常:{e.__str__()}','red'))
            exit(1)

    def check_remote_dir(self):
        try:
            self.c.run(f'umask 0022; mkdir -p /web/{self.project_name}')
            self.c.run(f'umask 0022; mkdir -p /web/backup/{self.project_name}')
        except Exception as e:
            print(All_params.display(f'Error:创建目录{self.project_name}失败:{e.__str__()}','red'))
            exit(0)
        else:
            print(All_params.display(f'Ok:创建目录{self.project_name}成功','green'))

    def backup_project_code(self):
        try:
            with self.c.run(f'cd /web/backup/{self.project_name}'):
                print(All_params.display('保留最近7天代码版本','red'))
                self.c.run(f'find /web/backup/{self.project_name} -maxdepth 1 -type d  -print0 |xargs -0  ls -dc --quoting-style=shell-always  |tail -n +7 |xargs rm -rf')
                print(All_params.display(f'代码备份到/web/backup/{self.project_name}/','red'))
                back_code = (f'{self.project_name}_{self.svn_version}')
                self.c.run(f'rsync -avz --exclude=logs --exclude=*.log /web/{self.project_name} /web/backup/{back_code}')
        except Exception as e:
            print(All_params.display(f'Error:代码备份失败:{e.__str__()}','red'))
            exit(0)
        else:
            print(All_params.display(f'代码{self.project_name}备份成功','green'))

    def svn_to_projectdir(self):
        print(All_params.display(f'开始拉取SVN版本:{self.svn_version} 项目:{self.project_name}代码到本地','yellow'))
        if not os.path.exists(f'{self.source_path}/{self.project_name}'):
           invoke.run(f'umask 0022; mkdir -p {self.source_path}/{self.project_name}')
        try:
            invoke.run(f'rm -rf {self.source_path}/{self.project_name}/*')
            invoke.run(f'/usr/bin/svn --username johnny --password 123456 export -r {self.svn_version} {self.svn_path} {self.tmp_dir}/{self.project_name} --force')
        except Exception as e:
            print(All_params.display(f'Error:项目代码:{self.project_name}代码拉取失败异常信息为:{e.__str__()}','red'))
            exit(0)
        else:
            print(All_params.display(f'项目代码:{self.project_name}拉取到本地成功','green'))
        try:
           dir_list = os.listdir(f'{self.tmp_dir}/{self.project_name}')
           if not dir_list:
              print(All_params.display(f'Error:获取项目:{self.project_name}代码为空','red'))
              sys.exit(0)
           if '.svn' in dir_list:
               dir_list.remove('.svn')
           for file in dir_list:
               if file.endswith('.war') or file.endswith('.zip'):
                  print(All_params.display(f'从SVN获取过来的是zip&war包,开始解压','yellow'))
                  try:
                      invoke.run(f'unzip -qo {self.tmp_dir}/{self.project_name}/{file} -d {self.source_path}/{self.project_name}')
                      print(All_params.display(f'文件:{file}解压成功','green'))
                      break
                  except Exception as e:
                      print(All_params.display(f'Error:文件解压失败请检查文件:{file}是否损坏:{e}'))
                      exit(0)
           if dir_list:
              invoke.run(f'chmod -R 755 {self.source_path}/{self.project_name}')
              invoke.run(f'echo project_name:{self.project_name} >> {self.source_path}/{self.project_name}/version.txt')
              invoke.run(f'echo svn_version:{self.svn_version} >> {self.source_path}/{self.project_name}/version.txt')
              invoke.run(f'echo upgrade_time:{self.date} >> {self.source_path}/{self.project_name}/version.txt')
        except Exception as e:
            print(All_params.display(f'代码拉取解压失败异常信息为:{e.__str__()}','red'))
            exit(0)

    def deploy_project(self):
        try:
          patchwork.transfers.rsync(self.c,f'{self.source_path}/{self.project_name}/',f'/web/{self.project_name}/',exclude=self.exclude,delete=True)
        except Exception as e:
            print(All_params.display(f'Error:代码同步异常:{e.__str__()}','red'))
            exit(0)
        else:
            print(All_params.display(f'Ok:项目:{self.project_name}同步到服务器:{self.hosts}成功','green'))

    def put_config_remote(self):
        print(All_params.display(f'开始更新项目:{self.project_name}配置文件','yellow'))
        conf = loadfile[self.project_name]['conf']
        try:
           for sort in range(0,len(conf)):
               if conf[sort]['dest'] == 'all':
                  print(All_params.display(f'开始推送项目:{self.project_name}配置文件到服务器:{self.hosts}'))
                  self.c.put('conf/' + self.project_name + '/' + conf[sort]['local'],conf[sort]['remote'],preserve_mode=True)
               elif conf['dest'] == str(self.hosts):
                  print(All_params.display(f'推送项目:{self.project_name}到指定服务器:{self.hosts}','yellow'))
                  self.c.put('conf/' + self.project_name + '/' + conf[sort]['local'],conf[sort]['remote'],preserve_mode=True)
        except Exception as e:
            print(All_params.display(f'Error:同步项目:{self.project_name}配置文件到服务器:{self.hosts}出错,异常信息为:{e.__str__()}','red'))
            exit(0)
        else:
            print(All_params.display(f'Ok:推送项目:{self.project_name}到服务器:{self.hosts}成功','green'))

    def restart_project(self):
        choose = All_params.check_input('y/Y是否重启')
        if choose.lower() == 'y':
            print(All_params.display(f'开始重启项目:{self.project_name}'))
            try:
               self.c.run(self.restart_cmd)
            except Exception as e:
                print(All_params.display(f'Error:项目:{self.project_name}重启异常:{e.__str__()}','red'))
                exit(0)
            else:
                print(All_params.display(f'Ok:项目:{self.project_name}重启成功','green'))
        else:
            print(All_params.display('静态资源无需重启','red'))

    def rollback_project(self):
        print(All_params.display(f'开始回滚项目:{self.project_name}到svn:{self.svn_version}版本'))
        try:
           self.svn_to_projectdir()
           self.put_config_remote()
           self.restart_project()
        except Exception as e:
           print(All_params.display(f'Error:项目:{self.project_name}代码回滚失败,异常信息为:{e.__str__()}','red'))
           exit(0)
        else:
           print(All_params.display(f'Ok:项目:{self.project_name}回滚成功','green'))

    def get_project_remote_svn_version(self):
        try:
            self.c.run(f"cat /web/{self.project_name}/version.txt | grep project_name")
            self.c.run(f"cat /web/{self.project_name}/version.txt | grep svn_version")
        except Exception as e:
            print(f'Erroe:查看项目:{self.project_name}版本异常:{e.__str__()}')

    @pysnooper.snoop('logs/fab.log')
    def deploy_jdk(self):
        print(All_params.display('>>>>开始推送Jdk到服务器','yellow'))
        if exists(self.c,'/opt/jdk1.8*') or exists(self.c,'/opt/jdk1.9*'):
           print(All_params.display('jdk1.8已经存在不用推送', 'yellow'))
        else:
            software_list = os.listdir(f'{os.getcwd()}/software_dir/')
            if not software_list:
                print(All_params.display('software目录下为空，请检查', 'yellow'))
                exit(0)
            for filename in software_list:
                if filename.startswith('jdk1.8'):
                   try:
                       self.c.put(f'software_dir/{filename}', f'/opt/{filename}', preserve_mode=True)
                   except Exception as e:
                       print(All_params.display(f'Error:Jdk上传到服务器失败:{e.__str__()}', 'red'))
                       exit(0)
                   else:
                       print(All_params.display('OK:Jdk上传到服务器成功>>>开始解压Jdk', 'green'))
                       self.c.run(f'tar -xf /opt/{filename} -C /opt/')
                       print(All_params.display('OK:Jdk解压成功','green'))
                       self.c.run(f'rm -f /opt/{filename}')

    @pysnooper.snoop('logs/fab.log')
    def deploy_tomcat(self):
        print(All_params.display('>>>>开始推送Tomcat到服务器', 'yellow'))
        software_list = os.listdir(f'{os.getcwd()}/software_dir/')
        if not software_list:
           print(All_params.display('software目录下为空，请检查','yellow'))
           exit(0)
        for filename in software_list:
            if filename.startswith('tomcat-8.0') or filename.startswith('tomcat-8.5'):
                try:
                   self.c.put('software_dir/' + filename,f'/opt/{filename}')
                except Exception as e:
                    print(All_params.display(f'Error:Tomcat上传到服务器失败:{e.__str__()}','red'))
                    exit(0)
                else:
                    print(All_params.display('OK:Tomcat上传到服务器成功','green'))
                    print(All_params.display('>>>>开始解压Jdk和Tomcat','yellow'))
                    self.c.run(f'tar -xf /opt/{filename} -C /opt/')
                finally:
                    self.c.run(f'rm -f /opt/{filename}')
                    break
        print(All_params.display('>>>>开始配置Tomcat','yellow'))
        Tomcat_port = All_params.check_input('Tomcat主端口号')
        if self.tomcat_version == '8.5':
            self.c.run(f'mv /opt/tomcat-8.5 /opt/tomcat-{self.tomcat_version}_{self.project_name}_{Tomcat_port}')
        else:
            self.c.run(f'mv /opt/tomcat-8.0 /opt/tomcat-{self.tomcat_version}_{self.project_name}_{Tomcat_port}')
        Tomcat_port = int(Tomcat_port)
        Tomcat_Sconf = ET.parse('software_dir/server.xml')
        conFile = Tomcat_Sconf.getroot()
        '''修改代码部署目录'''
        for deployPath in conFile.find('Service').find('Engine').find('Host').iter('Context'):
            deployPath.set('docBase',f'/web/{self.project_name}')
        '''修改服务端口'''
        for Zport in conFile.find("Service").iter('Connector'):
            if "HTTP" in Zport.get('protocol'):
                Zport.set('port',str(Tomcat_port))
        '''修改子端口'''
        for Sport in conFile.iter('Server'):
            port = Tomcat_port + 1
            Sport.set('port',str(port))
        '''修改子端口'''
        for Cport in conFile.find('Service').iter('Connector'):
            if 'AJP' in Cport.get('protocol'):
                port = Tomcat_port + 2
                Cport.set('port',str(port))

        Tomcat_Sconf.write('software_dir/server.xml',encoding='utf-8')
        try:
            self.c.put('software_dir/server.xml','tomcat-{}_{}_{}/conf/server.xml'.format(self.tomcat_version,self.project_name,Tomcat_port))
            self.c.put('software_dir/apr.tar.gz','/usr/local/apr.tar.gz')
            self.c.run('tar -xf /usr/local/apr.tar.gz -C /usr/local/ && rm -f /usr/local/apr.tar.gz')
            self.c.put('software_dir/catalina.sh','tomcat-{}_{}_{}/bin/catalina.sh'.format(self.tomcat_version,self.project_name,Tomcat_port))
        except Exception as e:
            print(All_params.display(f'推送Tomcat配置文件到服务器异常:{e.__str__()}','red'))
        else:
            print(All_params.display(f'推送Tomcat文件到服务器成功','green'))

    def create_project(self):
        project = All_params.check_input('你创建的项目')
        host_list = []
        hosts = All_params.check_input('你项目主机多个已逗号分隔')
        for host in hosts.split(','):
            host_list.append(host)

        svn_path = All_params.check_input('你SVN路径')
        exclude_list = input('请输入排除的文件或目录多个逗号分隔,回车为空')
        restart_str = All_params.check_input('你的重启命令').strip() or 'echo no restart'
        cond = 'y'
        all_conf = []
        while cond != 'n':
            tmp_conf = {}
            local_conf = input('请输入配置文件名,无配置文件直接回车:').strip()
            remote_conf = input(f'请输入配置文件对应服务器上的路径类似/web/{project}/:' ).strip()
            dest_conf = All_params.check_input('升级到所有服务器请输入all或输入主机 ').strip()
            tmp_conf['local'] = local_conf
            tmp_conf['remote'] = remote_conf
            tmp_conf['dest'] = dest_conf
            all_conf.append(tmp_conf)
            cond = All_params.check_input('是否继续添加(y|n)')

        project_info = {}
        project_info['info'] = project
        project_info['hosts'] = host_list
        project_info['restart_str'] = restart_str
        project_info['svn_path'] = svn_path
        project_info['conf'] = all_conf
        project_info['exclude_opts'] = exclude_list
        try:
            all_conf_yaml = {}
            with open('conf/project_list.yml','r',encoding='utf-8') as readfile:
                conf_all = yaml.load(readfile)
                for k in conf_all.keys():
                    all_conf_yaml[k] = conf_all[k]
                all_conf_yaml[project] = project_info

            with open('conf/project_list.yml', 'w') as writefile:
                yaml.dump(yaml.load(str(all_conf_yaml)), writefile, encoding='utf-8', allow_unicode=True)
        except Exception as e:
            print(All_params.display(f'Error:项目:{project}配置写入yml文件失败:{e.__str__()}','red'))
            exit(0)
        else:
            print(All_params.display(f'Ok:项目:{project}配置写入yml文件成功','green'))
        try:
            invoke.run(f'mkdir -p project_code/{project}')
            invoke.run(f'mkdir -p project_conf/{project}')
        except Exception as e:
            print(All_params.display(f'Error:创建项目:{project}代码和配置文件目录失败:{e.__str__()}','red'))
            exit(0)
        else:
            print(All_params.display(f'ok:创建项目:{project}代码目录成功','green'))
            print(All_params.display(f'ok:创建项目:{project}配置文件目录成功','green'))

    def upgrade_project(self):
        self.check_remote_dir()
        self.backup_project_code()
        self.svn_to_projectdir()
        self.deploy_project()
        self.put_config_remote()
        self.restart_project()

    def rollback(self):
        self.rollback_project()
        self.put_config_remote()
        self.restart_project()

    def create_main(self):
        self.create_project()
        self.deploy_jdk()
        self.deploy_tomcat()
        self.create_project()
        self.deploy_project()
        self.restart_cmd()

@pysnooper.snoop('logs/fab.log')
class Main(object):
    def __init__(self):
        pass

    @staticmethod
    def project_list():
       try:
          for pro_list in loadfile.keys():
              print(All_params.display(f'\t\t{pro_list}','yellow'))
       except Exception as e:
            print(f'获取项目列表异常:{e.__str__()}')
            exit(0)

    @staticmethod
    def menu():
        while True:
            print(All_params.display(f'\t请选择你的操作:', 'yellow'))
            menu_dict = {'1':'升级工程','2':'代码回滚','3':'服务版本','4':'重启服务','5':'新建项目'}
            menu_list = All_params.input_ck(menu_dict,'操作序号')
            if int(menu_list) == 1:
               Main.project_list()
               projectname = All_params.check_input('你的项目')
               svn_version = All_params.check_input('你的SVN版本')
               Fab(project_name=projectname,svn_version=svn_version).upgrade_project()
            elif int(menu_list) == 2:
               Main.project_list()
               projectname = All_params.check_input('回滚你的项目')
               svn_version = All_params.check_input('回滚你的SVN版本')
               Fab(project_name=projectname, svn_version=svn_version).rollback()
            elif int(menu_list) == 3:
               Main.project_list()
               projectname = All_params.check_input('你的项目')
               Fab(project_name=projectname).get_project_remote_svn_version()
            elif int(menu_list) == 4:
               Main.project_list()
               projectname = All_params.check_input('重启的项目')
               Fab(project_name=projectname).restart_project()
            elif int(menu_list) == 5:
                new_project_ops = {'1':'命令行新增','2':'文本新增'}
                result_ops = All_params.input_ck(new_project_ops,'操作序号')
                if int(result_ops) == 1:
                   tomcat_version = All_params.check_input('Tonmcat版本8/8.5,jdk默认为8')
                   Fab(tomcat_version=tomcat_version).create_main()
                elif int(result_ops) == 2:
                   os.system('vim conf/project_list.yml')

if __name__ == '__main__':
    f = Fab()
    # f.deploy_jdk()
    f.deploy_tomcat()
    # main = Main()
    # main.menu()
    '''
        check_remote_dir()         ---检查远程目录
        backup_project_code()      ---备份代码
        snv_to_projectdir()        ---拉取SVN代码
        deploy_project()           ---同步代码
        project_config()           ---同步配置文件
        restart_project()          ---重启服务
    '''
    # stat = Fab(project_name='b79_web_front',svn_version='6')
    # stat.diff_code()