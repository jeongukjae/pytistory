# -*- coding:utf8 -*-
import os
import unittest

from selenium import webdriver

from pytistory import PyTistory
from pytistory.exceptions import NoSpecifiedBlogError, ParsingError

class TestPost(unittest.TestCase):
    def setUp(self):
        self.pytistory = PyTistory()
        self.pytistory.configure()

        self.tistory_id = os.environ.get('PYTISTORY_TISTORY_ID')
        self.tistory_password = os.environ.get('PYTISTORY_TISTORY_PASSWORD')

        self.driver = webdriver.Chrome()

    def test001_최근_게시글_목록(self):
        data = self.pytistory.post.list(blog_name='test-blog-5532')
        self.assertEqual('1', data['item']['page'])

    def test002_최근_게시글_목록_블로그_비_명시(self):
        self.assertRaises(NoSpecifiedBlogError, self.pytistory.post.list)

    def test003_블로그_없을_때(self):
        self.assertRaises(ParsingError, self.pytistory.post.list,\
            blog_name='test-blog-5555-not-found')

    def test004_블로그_글_작성_수정(self):
        response = self.pytistory.post.write('테스트 포스팅', blog_name='test-blog-5532',\
            visibility=2, content='글 내용', tag=['가나다', '라마바'])
        post_id = response['postId']

        post_response = self.pytistory.post.read(post_id, blog_name='test-blog-5532')
        self.assertIn('글 내용', post_response['item']['content'])
        self.assertIn('테스트 포스팅', post_response['item']['title'])
        self.assertIn('가나다', post_response['item']['tags']['tag'])

        response = self.pytistory.post.modify('테스트 포스팅 - 수정', post_id, blog_name='test-blog-5532',\
            visibility=2, content='글 내용 - 수정', tag=['가나다', '라마바', '수정'])
        post_id = response['postId']

        post_response = self.pytistory.post.read(post_id, blog_name='test-blog-5532')
        self.assertIn('수정', post_response['item']['content'])
        self.assertIn('수정', post_response['item']['title'])
        self.assertIn('수정', post_response['item']['tags']['tag'])

        # post 삭제
        self.driver.get('https://tistory.com/auth/login')
        self.driver.find_element_by_name('loginId').send_keys(self.tistory_id)
        self.driver.find_element_by_name('password').send_keys(self.tistory_password)
        self.driver.find_element_by_xpath('//*[@id="authForm"]/fieldset/div/button').click()

        if self.driver.current_url.split('?')[0].endswith('outdated'):
            self.driver.find_element_by_xpath('//*[@id="passwordChangeForm"]/fieldset/div/a').click()
        
        self.driver.get('http://test-blog-5532.tistory.com/{0}'.format(post_id))
        self.driver.find_element_by_xpath('//*[@id="mArticle"]/div/div[1]/span/span[2]/a[3]').click()
        self.driver.switch_to.alert.accept()
    
    def test005_파일_첨부_후_게시(self):
        image_response = self.pytistory.post.attach('tests/test_image.png', blog_name='test-blog-5532')
        response = self.pytistory.post.write('테스트 포스팅', blog_name='test-blog-5532',\
            visibility=2, content='글 내용 {}'.format(image_response['replacer']),\
            tag=['가나다', '라마바'])
        post_response = self.pytistory.post.read(response['postId'], blog_name='test-blog-5532')
        self.assertIn('img', post_response['item']['content'])

        # post 삭제
        self.driver.get('https://tistory.com/auth/login')
        self.driver.find_element_by_name('loginId').send_keys(self.tistory_id)
        self.driver.find_element_by_name('password').send_keys(self.tistory_password)
        self.driver.find_element_by_xpath('//*[@id="authForm"]/fieldset/div/button').click()

        if self.driver.current_url.split('?')[0].endswith('outdated'):
            self.driver.find_element_by_xpath('//*[@id="passwordChangeForm"]/fieldset/div/a').click()
        
        self.driver.get('http://test-blog-5532.tistory.com/{0}'.format(response['postId']))
        self.driver.find_element_by_xpath('//*[@id="mArticle"]/div/div[1]/span/span[2]/a[3]').click()
        self.driver.switch_to.alert.accept()

    def test006_블로그_글_삭제(self):
        # 사전 협의가 안되어 있어서 삭제가 안되는게 정상이다.
        self.assertRaises(ParsingError, self.pytistory.post.delete, 1, blog_name='test-blog-5532')

    def tearDown(self):
        self.driver.quit()
