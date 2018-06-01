---
layout : post
title : 【 python 基础系列 】 - python 单元测试 unittest 工具使用
category : python
date : 2018-01-18
tags : [python, unittest]
---

python 的单元测试有许多工具，如unittest、pytest、nosetest 等等，这里主要介绍下unittest 的使用。

>以下文字为转载，原文链接：[https://www.cnblogs.com/yufeihlf/p/5707929.html](https://www.cnblogs.com/yufeihlf/p/5707929.html)


unittest单元测试框架不仅可以适用于单元测试，还可以适用WEB自动化测试用例的开发与执行，该测试框架可组织执行测试用例，并且提供了丰富的断言方法，判断测试用例是否通过，最终生成测试结果。今天笔者就总结下如何使用unittest单元测试框架来进行WEB自动化测试。


## unittest模块的各个属性说明

先来聊一聊unittest模块的各个属性，所谓知己知彼方能百战百胜，了解unittest的各个属性，对于后续编写用例有很大的帮助。

**1.unittest的属性如下：**

```python
['BaseTestSuite', 'FunctionTestCase', 'SkipTest', 'TestCase', 'TestLoader', 'TestProgram', 'TestResult', 'TestSuite', 'TextTestResult', 'TextTestRunner', '_TextTestResult', '__all__', '__builtins__', '__doc__', '__file__', '__name__', '__package__', '__path__', '__unittest', 'case', 'defaultTestLoader', 'expectedFailure', 'findTestCases', 'getTestCaseNames', 'installHandler', 'loader', 'main', 'makeSuite', 'registerResult', 'removeHandler', 'removeResult', 'result', 'runner', 'signals', 'skip', 'skipIf', 'skipUnless', 'suite', 'util']
```

说明：
`unittest.TestCase`: TestCase类，所有测试用例类继承的基本类。

`unittest.main()`: 使用她可以方便的将一个单元测试模块变为可直接运行的测试脚本，main()方法使用TestLoader类来搜索所有包含在该模块中以“test”命名开头的测试方法，并自动执行他们。执行方法的默认顺序是：根据ASCII码的顺序加载测试用例，数字与字母的顺序为：0-9，A-Z，a-z。所以以A开头的测试用例方法会优先执行，以a开头会后执行。

`unittest.TestSuite()`: unittest框架的TestSuite()类是用来创建测试套件的。

`unittest.TextTextRunner()`: unittest框架的TextTextRunner()类，通过该类下面的run()方法来运行suite所组装的测试用例，入参为suite测试套件。

`unittest.defaultTestLoader()`: defaultTestLoader()类，通过该类下面的discover()方法可自动根据测试目录start_dir匹配查找测试用例文件（test*.py），并将查找到的测试用例组装到测试套件，因此可以直接通过run()方法执行discover。用法如下：
```python
discover=unittest.defaultTestLoader.discover(test_dir, pattern='test_*.py')
```

`unittest.skip()`: 装饰器，当运行用例时，有些用例可能不想执行等，可用装饰器暂时屏蔽该条测试用例。一种常见的用法就是比如说想调试某一个测试用例，想先屏蔽其他用例就可以用装饰器屏蔽。

@unittest.skip(reason): skip(reason)装饰器：无条件跳过装饰的测试，并说明跳过测试的原因。

@unittest.skipIf(reason): skipIf(condition,reason)装饰器：条件为真时，跳过装饰的测试，并说明跳过测试的原因。

@unittest.skipUnless(reason): skipUnless(condition,reason)装饰器：条件为假时，跳过装饰的测试，并说明跳过测试的原因。

@unittest.expectedFailure(): expectedFailure()测试标记为失败。

**2.TestCase类的属性如下：**
```python
['__call__', '__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_addSkip', '_baseAssertEqual', '_classSetupFailed', '_deprecate', '_diffThreshold', '_formatMessage', '_getAssertEqualityFunc', '_truncateMessage', 'addCleanup', 'addTypeEqualityFunc', 'assertAlmostEqual', 'assertAlmostEquals', 'assertDictContainsSubset', 'assertDictEqual', 'assertEqual', 'assertEquals', 'assertFalse', 'assertGreater', 'assertGreaterEqual', 'assertIn', 'assertIs', 'assertIsInstance', 'assertIsNone', 'assertIsNot', 'assertIsNotNone', 'assertItemsEqual', 'assertLess', 'assertLessEqual', 'assertListEqual', 'assertMultiLineEqual', 'assertNotAlmostEqual', 'assertNotAlmostEquals', 'assertNotEqual', 'assertNotEquals', 'assertNotIn', 'assertNotIsInstance', 'assertNotRegexpMatches', 'assertRaises', 'assertRaisesRegexp', 'assertRegexpMatches', 'assertSequenceEqual', 'assertSetEqual', 'assertTrue', 'assertTupleEqual', 'assert_', 'countTestCases', 'debug', 'defaultTestResult', 'doCleanups', 'fail', 'failIf', 'failIfAlmostEqual', 'failIfEqual', 'failUnless', 'failUnlessAlmostEqual', 'failUnlessEqual', 'failUnlessRaises', 'failureException', 'id', 'longMessage', 'maxDiff', 'run', 'setUp', 'setUpClass', 'shortDescription', 'skipTest', 'tearDown', 'tearDownClass']
```

说明：

setUp():setUp()方法用于测试用例执行前的初始化工作。如测试用例中需要访问数据库，可以在setUp中建立数据库连接并进行初始化。如测试用例需要登录web，可以先实例化浏览器。

tearDown():tearDown()方法用于测试用例执行之后的善后工作。如关闭数据库连接。关闭浏览器。

assert*():一些断言方法：在执行测试用例的过程中，最终用例是否执行通过，是通过判断测试得到的实际结果和预期结果是否相等决定的。

assertEqual(a,b，[msg='测试失败时打印的信息']):断言a和b是否相等，相等则测试用例通过。

assertNotEqual(a,b，[msg='测试失败时打印的信息']):断言a和b是否相等，不相等则测试用例通过。

assertTrue(x，[msg='测试失败时打印的信息'])：断言x是否True，是True则测试用例通过。

assertFalse(x，[msg='测试失败时打印的信息'])：断言x是否False，是False则测试用例通过。

assertIs(a,b，[msg='测试失败时打印的信息']):断言a是否是b，是则测试用例通过。

assertNotIs(a,b，[msg='测试失败时打印的信息']):断言a是否是b，不是则测试用例通过。

assertIsNone(x，[msg='测试失败时打印的信息'])：断言x是否None，是None则测试用例通过。

assertIsNotNone(x，[msg='测试失败时打印的信息'])：断言x是否None，不是None则测试用例通过。

assertIn(a,b，[msg='测试失败时打印的信息'])：断言a是否在b中，在b中则测试用例通过。

assertNotIn(a,b，[msg='测试失败时打印的信息'])：断言a是否在b中，不在b中则测试用例通过。

assertIsInstance(a,b，[msg='测试失败时打印的信息'])：断言a是是b的一个实例，是则测试用例通过。

assertNotIsInstance(a,b，[msg='测试失败时打印的信息'])：断言a是是b的一个实例，不是则测试用例通过。

**3.TestSuite类的属性如下：（组织用例时需要用到）**

```python
['__call__', '__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__', '__hash__', '__init__', '__iter__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_addClassOrModuleLevelException', '_get_previous_module', '_handleClassSetUp', '_handleModuleFixture', '_handleModuleTearDown', '_tearDownPreviousClass', '_tests', 'addTest', 'addTests', 'countTestCases', 'debug', 'run']
```

说明：

addTest(): addTest()方法是将测试用例添加到测试套件中，如下方，是将test_baidu模块下的BaiduTest类下的test_baidu测试用例添加到测试套件。

```python
suite = unittest.TestSuite()
suite.addTest(test_baidu.BaiduTest('test_baidu'))
```

**4.TextTextRunner的属性如下：（组织用例时需要用到）**

```python
['__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_makeResult', 'buffer', 'descriptions', 'failfast', 'resultclass', 'run', 'stream', 'verbosity']
```
说明：

run(): run()方法是运行测试套件的测试用例，入参为suite测试套件。

```python
runner = unittest.TextTestRunner()
runner.run(suite)
```

## 使用unittest框架编写测试用例思路

设计基本思路如下：

```python
# coding=utf-8
#1.先设置编码，utf-8可支持中英文，如上，一般放在第一行

#2.注释：包括记录创建时间，创建人，项目名称。
'''
Created on 2016-7-27
@author: Jennifer
Project:使用unittest框架编写测试用例思路
'''
#3.导入unittest模块
import unittest

#4.定义测试类，父类为unittest.TestCase。
#可继承unittest.TestCase的方法，如setUp和tearDown方法，不过此方法可以在子类重写，覆盖父类方法。
#可继承unittest.TestCase的各种断言方法。
class Test(unittest.TestCase): 
    
#5.定义setUp()方法用于测试用例执行前的初始化工作。
#注意，所有类中方法的入参为self，定义方法的变量也要“self.变量”
#注意，输入的值为字符型的需要转为int型
    def setUp(self):
        self.number=raw_input('Enter a number:')
        self.number=int(self.number)

#6.定义测试用例，以“test_”开头命名的方法
#注意，方法的入参为self
#可使用unittest.TestCase类下面的各种断言方法用于对测试结果的判断
#可定义多个测试用例
#最重要的就是该部分
    def test_case1(self):
        print self.number
        self.assertEqual(self.number,10,msg='Your input is not 10')
        
    def test_case2(self):
        print self.number
        self.assertEqual(self.number,20,msg='Your input is not 20')

    @unittest.skip('暂时跳过用例3的测试')
    def test_case3(self):
        print self.number
        self.assertEqual(self.number,30,msg='Your input is not 30')

#7.定义tearDown()方法用于测试用例执行之后的善后工作。
#注意，方法的入参为self
    def tearDown(self):
        print 'Test over'
        
#8如果直接运行该文件(__name__值为__main__),则执行以下语句，常用于测试脚本是否能够正常运行
if __name__=='__main__':
#8.1执行测试用例方案一如下：
#unittest.main()方法会搜索该模块下所有以test开头的测试用例方法，并自动执行它们。
#执行顺序是命名顺序：先执行test_case1，再执行test_case2
    unittest.main()

'''
#8.2执行测试用例方案二如下：
#8.2.1先构造测试集
#8.2.1.1实例化测试套件
    suite=unittest.TestSuite()
#8.2.1.2将测试用例加载到测试套件中。
#执行顺序是安装加载顺序：先执行test_case2，再执行test_case1
    suite.addTest(Test('test_case2'))
    suite.addTest(Test('test_case1'))
#8.2.2执行测试用例
#8.2.2.1实例化TextTestRunner类
    runner=unittest.TextTestRunner()
#8.2.2.2使用run()方法运行测试套件（即运行测试套件中的所有用例）
    runner.run(suite)
'''
    
'''
#8.3执行测试用例方案三如下：
#8.3.1构造测试集（简化了方案二中先要创建测试套件然后再依次加载测试用例）
#执行顺序同方案一：执行顺序是命名顺序：先执行test_case1，再执行test_case2
    test_dir = './'
    discover = unittest.defaultTestLoader.discover(test_dir, pattern='test_*.py')
#8.3.2执行测试用例
#8.3.2.1实例化TextTestRunner类
    runner=unittest.TextTestRunner()
#8.3.2.2使用run()方法运行测试套件（即运行测试套件中的所有用例）
    runner.run(discover)   
'''

## 使用unittest框架编写测试用例实例

**百度搜索测试用例Test Case：**
```python
# coding=utf-8
'''
Created on 2016-7-22
@author: Jennifer
Project:登录百度测试用例
'''
from selenium import webdriver
import unittest, time

class BaiduTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30) #隐性等待时间为30秒
        self.base_url = "https://www.baidu.com"
    
    def test_baidu(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_id("kw").clear()
        driver.find_element_by_id("kw").send_keys("unittest")
        driver.find_element_by_id("su").click()
        time.sleep(3)
        title=driver.title
        self.assertEqual(title, u"unittest_百度搜索") 

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
```

**有道翻译测试用例Test Case：**
```python
# coding=utf-8
'''
Created on 2016-7-22
@author: Jennifer
Project:使用有道翻译测试用例
'''
from selenium import webdriver
import unittest, time

class YoudaoTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30) #隐性等待时间为30秒
        self.base_url = "http://www.youdao.com"
    
    def test_youdao(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_id("translateContent").clear()
        driver.find_element_by_id("translateContent").send_keys(u"你好")
        driver.find_element_by_id("translateContent").submit()
        time.sleep(3)
        page_source=driver.page_source
        self.assertIn( "hello",page_source) 

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
```

**web测试用例：通过测试套件TestSuite来组装多个测试用例。**
```python
# coding=utf-8
'''
Created on 2016-7-26
@author: Jennifer
Project:编写Web测试用例
'''
import unittest
from test_case import test_baidu
from test_case import test_youdao

#构造测试集
suite = unittest.TestSuite()
suite.addTest(test_baidu.BaiduTest('test_baidu'))
suite.addTest(test_youdao.YoudaoTest('test_youdao'))

if __name__=='__main__':
    #执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)
```

测试结果：
![](/static/imgs/test_case_ret.jpg)

说明：.代表用例执行通过，两个点表示两个用例执行通过。F表示用例执行不通过。