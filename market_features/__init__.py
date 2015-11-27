import datetime
import json
import os
import sys
import traceback
import nose
import nose.plugins.base
from jinja2 import Environment, FileSystemLoader
from nose.plugins.base import Plugin


class MarketFeatures(Plugin):
    """
    provide summery report of executed tests listed per market feature
    """
    name = 'market-features'

    def __init__(self):
        super(MarketFeatures, self).__init__()
        self.results = {"results": []}
        self.exceptions = {'exceptions': []}
        self.starting_tests = {'timer': []}
        self.feature_time = None
        self.test_time = None

    @staticmethod
    def begin():
        print("begin")

    def help(self):
        return "provide summery report of executed tests listed per market feature"

    def startTest(self, test):
        address = test.address()
        message = test.shortDescription() if test.shortDescription() else str(address[-1]).split('.')[-1]
        self.starting_tests['timer'].append(message)
        self.feature_time = datetime.datetime.now()

    def addError(self, test, err):
        end_time = datetime.datetime.now()
        report_test_time = end_time - self.feature_time
        t = report_test_time
        milliseconds = (t.days * 24 * 60 * 60 + t.seconds) * 1000 + t.microseconds / 1000.0
        exc_type, exc_value, exc_traceback = sys.exc_info()
        t_len = traceback.format_exception(exc_type, exc_value,
                                           exc_traceback).__len__() - 2
        exception_msg = "{0} {1} {2}".format(str(exc_type.__name__), str(exc_value),
                                             str(traceback.format_exception(exc_type, exc_value,
                                                                            exc_traceback)[t_len]))

        actual = str(traceback.format_exception(exc_type, exc_value,
                                                exc_traceback)[t_len])
        actual = actual.split(",", 1)

        message = str(actual[0]).split('.')

        # message = message[0].rsplit('/', 1)[-1]
        # self.exceptions['exceptions'].append(str(exc_value))
        # self.exceptions['exceptions'].append(str(market_feature))
        # self.exceptions['exceptions'].append(str(message))
        self.exceptions['exceptions'].append(str(exception_msg))
        if isinstance(test, nose.case.Test):
            self.report_test("test failed", test, err, round(milliseconds, 2))
        else:
            self.report_test_exceptions(message, exception_msg, round(milliseconds, 2), 'test error')

    def addFailure(self, test, err):
        end_time = datetime.datetime.now()
        report_test_time = end_time - self.feature_time
        t = report_test_time
        milliseconds = (t.days * 24 * 60 * 60 + t.seconds) * 1000 + t.microseconds / 1000.0
        self.report_test("test failed", test, err, round(milliseconds, 2))

    def addSuccess(self, test, error=None):
        end_time = datetime.datetime.now()
        report_test_time = end_time - self.feature_time
        t = report_test_time
        milliseconds = (t.days * 24 * 60 * 60 + t.seconds) * 1000 + t.microseconds / 1000.0
        self.report_test("test passed", test, error, round(milliseconds, 2))

    def finalize(self, result):
        now = datetime.datetime.now()
        self.results['report_date_time'] = now.strftime("%Y-%m-%d %H:%M")
        self.results['total_number_of_market_features'] = self.__get_total_number_of_market_features()
        self.results['total_number_of_tests'] = self.__get_total_number_of_tests()
        self.results['number_of_passed_market_features'] = self.__get_number_of_passed_market_features()
        self.results['number_of_passed_tests'] = self.__get_number_of_passed_tests()
        total_no_of_fail_tests = self.__get_total_number_of_tests() - self.__get_number_of_passed_tests() - self.__get_total_number_of_errors()
        self.results['total_no_of_fail_tests'] = total_no_of_fail_tests
        self.results['total_exceptions'] = self.__get_total_number_of_errors()
        self.results['exceptions'] = self.exceptions['exceptions']
        self.results['time_summary'] = round(self.__get_total_feature_elapsed_time() / 1000, 2)

        report = self.__render_template("market_features_new_rc.html", self.results)
        with open("market_features.html", "w") as output_file:
            output_file.write(report)

    def report_test(self, pre, test, err, test_time):
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
                test = {'result': pre, 'name': str(address[1:]), 'message': message, 'err_msg': err_msg,
                        'test_time': test_time}
                result['tests'].append(test)
                break
        else:
            result = {'name': market_feature,
                      'description': self.__extract_market_feature_description(test),
                      'status': None, 'tests': [], 'feature_time': None}
            test = {'result': pre, 'name': str(address[1:]), 'message': message, 'err_msg': err_msg,
                    'test_time': test_time}
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
                    result['status'] = 'failed'
                    break
            else:
                number_of_passed_market_features += 1
        return number_of_passed_market_features

    def __get_total_number_of_errors(self):
        no_of_tests_with_errors = 0
        for result in self.results['results']:
            for test in result['tests']:
                if "error" in test['result']:
                    result['status'] = 'error'
                    no_of_tests_with_errors += 1
                    break
        return no_of_tests_with_errors

    def __get_total_feature_elapsed_time(self):
        sum_of_features_update = 0
        for result in self.results['results']:
            timings = []
            for test in result['tests']:
                timings.append(test['test_time'])
            result['feature_time'] = round(sum(timings) / 1000, 2)
            sum_of_features_update += round(sum(timings), 2)
        return sum_of_features_update

    def __get_number_of_passed_tests(self):
        number_of_passed_tests = 0
        for result in self.results['results']:
            for test in result['tests']:
                if "passed" in test['result']:
                    number_of_passed_tests += 1
        return number_of_passed_tests

    def __render_template(self, name, data):
        env = Environment(loader=FileSystemLoader(name))

        env.filters['ignore_empty_elements'] = self.__ignore_empty_elements
        templates_path = os.path.dirname(os.path.abspath(__file__))
        env = Environment(loader=FileSystemLoader(templates_path))
        template = env.get_template(name + ".jinja")

        print json.dumps(self.results, indent=True)

        return template.render(data)

    def __ignore_empty_elements(self, list):
        return filter(None, list)

    def report_test_exceptions(self, address, err_msg, test_time, error_type=None):
        market_feature = self.__extract_market_feature(address)
        message = address[0].rsplit('/', 1)[-1]
        for result in self.results['results']:
            if result['name'] == market_feature:
                test = {'result': error_type, 'name': address[0], 'message': message, 'err_msg': err_msg,
                        'test_time': test_time}
                result['tests'].append(test)
                break
        else:
            result = {'name': market_feature,
                      # 'description': self.__extract_market_feature_description(address),
                      'status': None, 'tests': [], 'feature_time': None}
            test = {'result': error_type, 'name': address[0], 'message': message, 'err_msg': err_msg,
                    'test_time': test_time}
            result['tests'].append(test)
            self.results['results'].append(result)
