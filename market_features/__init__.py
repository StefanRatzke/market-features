import json
import os
import sys
import traceback

import nose
from nose.plugins.base import Plugin
import nose.plugins.base
from jinja2 import Environment, FileSystemLoader


class MarketFeatures(Plugin):
    """
    provide summery report of executed tests listed per market feature
    """
    name = 'market-features'

    def __init__(self):

        super(MarketFeatures, self).__init__()
        self.results = {"results": []}
        self.exceptions = {'exceptions': []}
        self.failed_market = {'market_feature': []}

    @staticmethod
    def begin():
        print("begin")

    def help(self):
        return "provide summery report of executed tests listed per market feature"

    def addError(self, test, err, capt=None):
        exc_type, exc_value, exc_traceback = sys.exc_info()
        t_len = traceback.format_exception(exc_type, exc_value,
                                           exc_traceback).__len__() - 2
        exception_msg = "{0} {1} {2}".format(str(exc_type.__name__), str(exc_value),
                                             str(traceback.format_exception(exc_type, exc_value,
                                                                            exc_traceback)[t_len]))
        self.exceptions['exceptions'].append(str(exception_msg))
        self.report_test("test failed", test, err)

    def addFailure(self, test, err, capt=None, tb_info=None):
        self.report_test("test failed", test, err)

    def addSuccess(self, test, capt=None):
        self.report_test("test passed", test, err=None)

    def afterTest(self, test):
        print "running", test.address()

    def finalize(self, result):
        self.results['total_number_of_market_features'] = self.__get_total_number_of_market_features()
        self.results['total_number_of_tests'] = self.__get_total_number_of_tests()
        self.results['number_of_passed_market_features'] = self.__get_number_of_passed_market_features()
        self.results['number_of_passed_tests'] = self.__get_number_of_passed_tests()
        total_no_of_fail_tests = self.__get_total_number_of_tests() - self.__get_number_of_passed_tests()
        self.results['total_no_of_fail_tests'] = total_no_of_fail_tests
        self.results['total_exceptions'] = len(self.exceptions['exceptions'])
        self.results['exceptions'] = self.exceptions['exceptions']
        report = self.__render_template("market_features_new_rc.html", self.results)
        with open("market_features.html", "w") as output_file:
            output_file.write(report)

    def report_test(self, pre, test, err):
        if not isinstance(test, nose.case.Test):
            return

        err_msg = None
        if err:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            err_msg = "{0} {1} {2}".format(str(exc_type.__name__), str(exc_value),
                                           str(traceback.format_tb(exc_traceback, 3)[1]))
        address = test.address()
        message = test.shortDescription() if test.shortDescription() else str(address[-1]).split('.')[-1]
        market_feature = self.__extract_market_feature(address)
        for result in self.results['results']:
            if result['name'] == market_feature:
                test = {'result': pre, 'name': str(address[1:]), 'message': message, 'err_msg': err_msg}
                result['tests'].append(test)
                break
        else:
            result = {'name': market_feature, 'description': self.__extract_market_feature_description(test),
                      'tests': []}
            test = {'result': pre, 'name': str(address[1:]), 'message': message, 'err_msg': err_msg}
            result['tests'].append(test)
            self.results['results'].append(result)

    @staticmethod
    def __extract_market_feature_description(test):
        try:
            return sys.modules[sys.modules[test.context.__module__].__package__].__doc__
        except KeyError:
            return None

    @staticmethod
    def __extract_market_feature(address):
        path = address[0]
        snake_case_result = os.path.split(os.path.dirname(os.path.abspath(path)))[1]
        split_result = snake_case_result.split('_')
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
                    market = {'status': 'failed'}
                    name = {'name': result['name']}
                    self.failed_market['market_feature'].append(market)
                    self.failed_market['market_feature'].append(name)
                    break
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

    def __render_template(self, name, data):
        env = Environment(loader=FileSystemLoader(name))

        env.filters['ignore_empty_elements'] = self.__ignore_empty_elements
        templates_path = os.path.dirname(os.path.abspath(__file__))
        env = Environment(loader=FileSystemLoader(templates_path))
        template = env.get_template(name + ".jinja")

        print self.results['results'][1]['tests']
        print len(self.results['results'])
        # print self.results['market_feature']
        # print json.dumps(self.results, indent=True)
        print self.results['results'][0]
        return template.render(data)

    def __ignore_empty_elements(self, list):
        return filter(None, list)
