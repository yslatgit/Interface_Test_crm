import os
import unittest
import paramunittest
from Base.BaseLog import MyLog
from Base.BaseHttp import Http
from Base.BaseData import GetUrl,GetData
from Base.BaseParams import Params
import json
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p))

url_path = PATH("../../testData/interfaceURL.xml")
data_path = PATH("../../testData/userCase.xlsx")

data = GetData(data_path,'outsideJob').get_data()
url = GetUrl(url_path,'outsideJob').get_url()

@paramunittest.parametrized(*data)
class OutsideJob(unittest.TestCase):
    def setParameters(self,case_name,method,appkey,jobID,version,msg):
        self.case_name = str(case_name)
        self.method = str(method)
        self.appkey = str(appkey)
        self.jobID = str(jobID).split(".")[0]
        self.version = str(version)
        self.msg = str(msg)

    def description(self):
        return self.case_name

    def setUp(self):
        self.req = Http("app")
        self.url = url
        self.result = None
        self.log = MyLog.get_log()
        self.logger = self.log.get_logger()
        print(self.case_name + "测试开始前准备")
        self.logger.info("*"*50)
        self.logger.info(self.case_name + "测试")

    def testoutsidejob(self):
        #拼接完整的请求接口
        self.req.set_url(self.url)
        #设置header
        header = {"cookie":""}
        self.req.set_headers(header)
        # #设置params
        # param = {'params':'{"appkey":"%s","jobID":"%s"}'%(self.appkey,self.jobID),'version':self.version}
        param = {
            "appkey":self.appkey,
            "jobID":self.jobID
        }
        param = Params.auto_params(param)
        param = json.dumps(param)
        param_1 = {
            'params':param,
            'version':self.version
        }
        self.req.set_params(param_1)
        #打印发送请求的方法
        self.logger.info("请求方法为 " + self.method)
        #请求
        self.result = self.req.get()
        #print(self.req.get().url)

    def tearDown(self):
        self.req = None
        self.logger.info("断言结果是 " + "%s" %self.checkResult())
        print("测试结束，结果已输出到Log")

    def checkResult(self):
        try:
            self.result = self.result.json()
            self.assertEqual(self.result["code"],200)
            return "Pass" + "---->" + self.msg
        except Exception as ex:
            self.logger.error(str(ex))
            return "False" + "--原因-->" + self.msg









if __name__ == '__main__':
    unittest.main()