from include import AutoScripts

if __name__=='__main__':
    print('Please input your username and password')
    username = input('username: ')  # 学号
    password = input('password: ')  # 密码
    print('Please input where you want to start')
    chapter = input('chapter: ')
    section = input('section: ')

    try:
        auto = AutoScripts.AutoScripts(username, password, chapter, section)
    except:
        pass

