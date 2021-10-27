import time
from moviepy.editor import VideoFileClip
from selenium import webdriver

class AutoScripts:
    
    def __init__(self, username, password, chapter, section):
        self.chrome_driver = '.\driver\chromedriver.exe'
        self.driver = webdriver.Chrome(executable_path=self.chrome_driver)
        # 请求登陆页面
        self.driver.get('http://222.16.4.190/')

        self.chapter_list = []
        self.section_list = []
        self.chapter = chapter
        self.section = section
        self.chapter_id = 'chapter_num_' + self.chapter
        self.section_id = ''
        self.chapter_select = ""
        self.section_select = ""

        self.login(username, password)
        self.handle()
        self.collect()
        # self.to_course()
        # self.is_end()

        count = 0
        while True:
            self.to_course()
            '''
            if count >= 30:
                self.driver.quit()
                break
            count += 1
            '''

            if self.is_end():
                print(self.chapter + '.' + self.section + ' is end')
                # self.to_course()
                section_index = int(self.section)-1
                chapter_index = self.chapter_list.index(self.chapter_id)
                if section_index < len(self.section_list)-1:
                    self.section_id = self.section_list[section_index + 1]
                    self.section =  str(int(self.section) + 1)
                    section_index += 1
                else:
                    if chapter_index < len(self.chapter_list)-1:
                        self.chapter_id = self.chapter_list[chapter_index + 1]
                        self.chapter = str(int(self.chapter) + 1)
                        chapter_index += 1
                        self.section = str(1)
                        section_index = int(self.section) - 1
                        self.collect()
                        self.to_course()
                    else:
                        self.driver.quit()
                        break


    def login(self, number, password):
        student_id = self.driver.find_element_by_id('loginId')  # 通过id定位
        pwd = self.driver.find_element_by_id('passdword')  # 密码
        login_btn = self.driver.find_element_by_id('but_login')  # 登陆按钮

        student_id.send_keys(number)  # 输入学号
        pwd.send_keys(password)  # 输入密码
        login_btn.click()  # 点击登陆按钮

    # 页面跳转
    def handle(self):
        time.sleep(1)
        key = self.driver.find_element_by_css_selector(
            '[onclick="goonLeanning(\'402881da61ffbbb001621d73e1c7010d\',\'ff8080814e24bf37014e28b2b7c20004\',\'5e90843e7bc36918017bddb8023c6652\')"]')  # 找到课程
        # print(key.text)
        key.click()  # 跳转到播放视频页面
        time.sleep(1)  # 等待页面加载
        # 切换到iframe下
        frame = self.driver.find_elements_by_tag_name('iframe')[0]
        self.driver.switch_to.frame(frame)

    # 数据采集
    def collect(self):

        self.chapter_list = self.driver.find_elements_by_class_name('chapter')
        for i in range(len(self.chapter_list)):
            self.chapter_list[i] = self.chapter_list[i].get_attribute('id')
        # print(self.chapter_list)

        chapter_select = self.driver.find_element_by_id(self.chapter_id)
        chapter_select.click()
        time.sleep(1)

        self.section_list = self.driver.find_elements_by_xpath('//div[@class=\'chapter is-open\']//li[position()<last()]')
        # print(len(self.section_list))
        for i in range(len(self.section_list)):
            self.section_list[i] = self.section_list[i].get_attribute('id')
        # print(self.section_list)
        self.section_id = self.section_list[int(self.section)-1]

    # 切换视频
    def to_course(self):

        self.chapter_select = self.driver.find_element_by_id(self.chapter_id)
        self.chapter_select.click()
        time.sleep(1)

        # self.section_select = self.driver.find_element_by_id(self.section_list[int(self.section)-1])
        self.section_select = self.driver.find_element_by_id(self.section_id)
        self.section_select.click()
        time.sleep(1)

        video = self.driver.find_element_by_id('ckplayer_a1')
        video.click()
        time.sleep(1)

    # 判断当前视频是否结束
    def is_end(self):
        video = self.driver.find_element_by_id('ckplayer_a1')  # 定位视频窗口
        src = video.get_attribute('src')
        # print(src)
        duration = self.get_video_duration(src)
        # print(duration)
        # duration = 1
        time.sleep(duration)

        return True
        # self.driver.quit()

    # 获取视频时长
    @staticmethod
    def get_video_duration(filename):
        clip=VideoFileClip(filename)
        return clip.duration
