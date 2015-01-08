import os
import sys
from nose.plugins.base import Plugin
import nose.plugins.base
from jinja2 import Environment, FileSystemLoader
class MarketFeatures(Plugin):
    '''
    provide summery report of executed tests listed per market feature
    '''
    name='market-features'
    def __init__(self):
        super(MarketFeatures, self).__init__()

   
    def begin(self):
        self.results = {"results":[]}
        print("begin")
         

    def help(self):
        return "provide summery report of executed tests listed per market feature"
    
    def addError(self, test, err, capt=None):
        self.report_test("test failed", test,err)
    
    def addFailure(self, test, err, capt=None, tb_info=None):
        self.report_test("test failed", test,err)

    def addSuccess(self, test, capt=None):
        self.report_test("test passed", test)
    
    def finalize(self, result):
        self.results['total_number_of_market_features'] = self.__get_total_number_of_market_features()
        self.results['total_number_of_tests'] = self.__get_total_number_of_tests()
        self.results['number_of_passed_market_features'] = self.__get_number_of_passed_market_features()
        self.results['number_of_passed_tests'] = self.__get_number_of_passed_tests()
        report = self.__render_template("market_features.html", self.results)
        with open("market_features.html","w") as output_file:
                  output_file.write(report)
        
    def report_test(self, pre, test,err=None):
        if not isinstance(test,nose.case.Test):
            return
        
        address = test.address()
        message = test.shortDescription() if test.shortDescription() else str(address[-1]).split('.')[-1]
        market_feature = self.__extract_market_feature(address)
        for result in self.results['results']:
            if  result['name'] == market_feature:
                test = {'result': pre, 'name' : str(address[1:]), 'message' : message}
                result['tests'].append(test)
                break
        else:                 
            result = {'name':market_feature, 'description': self.__extract_market_feature_description(test), 'tests' : []}
            test = {'result': pre, 'name' : str(address[1:]), 'message' : message}
            result['tests'].append(test)
            self.results['results'].append(result)
    
    def __extract_market_feature_description(self,test):
        try :
           return    sys.modules[sys.modules[test.context.__module__].__package__].__doc__
        except KeyError:
            return None
        
    def __extract_market_feature(self, address):
        path = address[0]
        snakecase_result = os.path.split(os.path.dirname(os.path.abspath(path)))[1]
        split_result = snakecase_result.split('_')
        return ' '.join([word.capitalize() for word in split_result])
        
    def __get_total_number_of_market_features(self):
        return len(self.results['results'])
    
    def __get_total_number_of_tests(self):
        total_number_of_tests = 0
        for result in self.results['results']:
            total_number_of_tests += len(result['tests']) 
        return total_number_of_tests
    
    def __get_number_of_passed_market_features(self):
        number_of_passed_market_features = 0
        for result in self.results['results']:
            for test in result['tests']:
                if "failed" in test['result']:
                    break;
            else:
                number_of_passed_market_features += 1
        
        return number_of_passed_market_features
    
    def __get_number_of_passed_tests(self):
        number_of_passed_tests = 0
        for result in self.results['results']:
            for test in result['tests']:
                if "failed" not in test['result']:
                    number_of_passed_tests += 1 
        
        return number_of_passed_tests
    
    def __render_template(self,name, data):
        env = Environment(loader=FileSystemLoader(name))

        env.filters['ignore_empty_elements'] = self.__ignore_empty_elements
        templates_path = os.path.dirname(os.path.abspath(__file__ ))
        env = Environment(loader=FileSystemLoader(templates_path))

        template = env.get_template(name + ".jinja")
        return template.render(data)

    def __ignore_empty_elements(self,list):
        return filter(None, list)
