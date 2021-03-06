__author__ = 'TIW'
# coding = utf-8
import telnetlib
import re
import time


### 网络设备IP
host = '218.17.209.74'
### 网络设备telnet端口
port = 60001
### 登录帐号
username = 'admin'
### 登录密码
password = 'admin@123'
### enable密码
enable_password = 'admin@123'
### enable命令
enable_command = 'en'
### Usermode提示符
usermodtag = b'>'
### Sysmode提示符
sysmodtag = b'#'
### 登录网络设备时提示输入账号的提示
login_prompt = b'Username'
### 登录网络设备时提示输入密码的提示
password_prompt = b'Password'
### 输入命令返回值未完结提示符
command_output_more_tag_prompt = b'More'
### 输入命令返回值未完结时输入的命令
command_output_more_input_command = '\n'
### 输入的命令
command_input = 'show ip arp'
### 命令返回值列表
command_output_list = []





###########################登录网络设备&输入命令并获取格式化返回值######################################
def login():
    ############################登录网络设备##################################
    ###实例化telnet对象，建立一个主机连接
    tn = telnetlib.Telnet(host, port=port, timeout=50000)
    # 开启调试，按需开启，方便判断
    #telnetsession.set_debuglevel(2)
    # 区配字符，当出现'Username'时，输入用户名
    tn.read_until(login_prompt)
    # 提示输入的用户名
    print('Input Username:', username)
    # 输入用户名
    tn.write((username + '\n').encode('utf-8'))
    # 区配字符，当出现'Password'时，输入密码
    tn.read_until(password_prompt)
    # 提示输入的密码
    print('Input Password:', password)
    # 输入密码
    tn.write((password + '\n').encode('utf-8'))
    # 如果登录Usermode成功，则出现类似>,使用UsermodTag来进行捕获
    tn.read_until(usermodtag)
    print('Get in sysmod, input command:', enable_command)
    tn.write((enable_command + "\n").encode('utf-8'))
    # 提升权限时，区配字符，当出现'Password'时，输入密码
    tn.read_until(b'Password')
    # 提示进入sysmod输入的密码
    print('Input enable password:', enable_password)
    # 输入enable密码
    tn.write((enable_password + '\n').encode('utf-8'))
    ############################登录网络设备##################################




    ############################输入命令并获取返回值##################################
    # 如果登录Sysmode成功，则出现类似#,使用SysmodTag来进行捕获
    tn.read_until(sysmodtag)
    # 提示输入的命令
    print('Input command:', command_input)
    # 输入命令
    tn.write((command_input + '\n').encode('utf-8'))
    time.sleep(0)
    print(5)
    rew = tn.read_some()

    print(rew)
    response = tn.read_until(command_output_more_tag_prompt)
    print(6)
    # 将获取命令返回值赋值给response_format
    response_format = response
    # 将response_format重新编码
    response_format = response_format.decode('utf-8')
    # 将response_format格式化
    response_format = re.sub(r'\x08', '', response_format)
    response_format = re.sub(r'--           ', '', response_format)
    response_format = re.split(r'\r\n', response_format)
    # 将多余的输入命令返回值未完结提示符删除
    for item in response_format:
        if command_output_more_tag_prompt.decode('utf-8') in item:
            response_format.remove(item)
    # 将输入命令的返回值添加到列表
    for item in response_format:
        command_output_list.append(item)


    print(7)
    # 将输入命令的返回值赋值response，如果sysmodtag在response则表示命令输出完整，否则输入命令获取完整的命令
    if sysmodtag not in response:
        n = 1
        while sysmodtag not in response:
            for i in range(1):
                # 命令返回值未完结时，输入继续输出命令获取值的命令
                tn.write(command_output_more_input_command.encode('utf-8'))
                # 获取命令返回值并赋值给response， 用response捕获命令结束提示
                response = tn.read_until(command_output_more_tag_prompt, timeout=0.5)
                # 将获取命令返回值赋值给response_format
                response_format = response
                # 将response_format重新编码
                response_format = response_format.decode('utf-8')
                # 将response_format格式化
                response_format = re.sub(r'\x08', '', response_format)
                response_format = re.sub(r'--           ', '', response_format)
                response_format = re.split(r'\r\n', response_format)
                # 将多余的输入命令返回值未完结提示符删除
                for item in response_format:
                    if command_output_more_tag_prompt.decode('utf-8') in item:
                        response_format.remove(item)
                # 将输入命令的返回值添加到列表
                for item in response_format:
                    command_output_list.append(item)
                # 提示正在获取命令返回值
                #print(response)
                print('Getting command output, please wait.',  n, 'lines command output had gotten.')
                n = n + 1
        # 获取完整的命令输出后提示完成
        print('All command output had gotten!!!')
    ############################输入命令并获取返回值##################################
    else:
        pass
    # 结束telnet

    tn.close()
    print('################################fuck################################')
    print('\n\n\n\n\n\n\n\n\n\n\n\n')


###########################登录网络设备&输入命令并获取格式化返回值######################################

login()


for item in command_output_list:
    print(item)


