import json, sys
import re
import allure
import jsonpath
import requests
from Common.utils import mTime
from Common.handle_logger import logger
from Common.handle_json import HandleJson
import jmespath

class Http(object):

    def __init__(self):
        self.baseurl = ''
        self.resp_json = {}
        self.relations = {}
        self._json = {}
        self.proxy = {}
        self._session = {}
        self.step_num = 0

    def create_session(self, *args):
        """
        A requests session
        :param: alias
        :return: self._session
        """
        alias = (tuple(args)[0]).strip()
        if alias == '':
            msg = f"[{mTime()}][{self.step_num}][create_session]❌ before-->The input parameter does not empty"
            allure_step_error(msg)
            return "FAIL", msg[14:]
        else:
            s = requests.Session()
            self._session[alias] = s

        allure_step(f"[{mTime()}][{self.step_num}][create_session] after-->self._session[{alias}]==>>{s}")
        allure_step(f"[{mTime()}][{self.step_num}][create_session] method return value:[{self._session}]")
        return "PASS", self._session

    def __get_alais_url(self, args):
        # if len(args) == 1:  #excel mode
            input_data = (tuple(args)[0]).strip()
            if ',' not in input_data:
                msg = f'[{mTime()}]❌ No alais, please it.'
                allure_step_error(msg)
                return "FAIL", msg[14:]
            else:
                new_input_data = input_data.split(',', 1)
                alais = (new_input_data[0]).strip()
                url = (new_input_data[1]).strip()
                try:
                    _session = self._session[alais]
                except:
                    msg = f'[{mTime()}]❌ The input alais "{alais}" incorrect, please check it. self._session{self._session}'
                    allure_step_error(msg)
                    return "FAIL", msg[14:]

            return _session, url
        # else:
        #     alais = (tuple(args)[0]).strip()
        #     try:
        #         _session = self._session[alais]
        #     except:
        #         logger.info(f'The input alais "{alais}" incorrect, please check it. self._session{self._session}')
        #         raise Exception(f'The input alais "{alais}" incorrect, please check it. self._session{self._session}')
        #     url = (tuple(args)[1]).strip()
        # return _session, url
    def __url(self, url_path):
        new_url = ''
        if (url_path is not None) and (url_path.startswith('http')):
            self.baseurl = url_path
            return self.baseurl
        else:
            if url_path != '' and url_path is not None:
                if not self.baseurl.startswith('http'):
                    msg = f"[{mTime()}]❌ The input URL '{url_path}' incorrect."
                    allure_step_error(msg)
                    return "FAIL", msg[14:]
                else:
                    if str(self.baseurl)[-1:] == '/':
                        new_url = self.baseurl + url_path
                    else:
                        new_url = self.baseurl + '/' + url_path
            else:
                if not self.baseurl.startswith('http'):
                    msg = f"[{mTime()}]❌ The input URL '{url_path}' incorrect."
                    allure_step_error(msg)
                    return "FAIL", msg[14:]
        return new_url


    def setheader(self, *args):
        """
        A requests session headers
        :param *args: alias required (excel mode)
        :return: self._session[alias].headers
        """
        try:
            # if 'headers' in kwargs.keys() and len(kwargs.keys()) != 0:  # py mode
            #     alais = (tuple(args)[0]).strip()
            #     self._session[alais].headers = kwargs['headers']
            #     logger.info(f"[{sys._getframe().f_code.co_name}]-->self._session[{alais}].headers==>>{self._session[alais].headers}")
            #     return self._session[alais].headers
            # elif 'headers' not in kwargs.keys() and len(kwargs.keys()) != 0:  # py mode
            #     logger.error(f'[{sys._getframe().f_code.co_name}]-->{kwargs.keys()} is not correct headers, please check it.')
            # else:  # excel mode
                request_key = str(tuple(args)[0]).strip()
                request_data = str(tuple(args)[1]).strip()
                if ',' not in request_key:
                    msg = f'[{mTime()}][setheader]❌ No session alias, please check it.'
                    allure_step_error(msg)
                    return "FAIL", msg[14:]
                else:
                    new_input_data = request_key.split(',', 1)
                    alias = (new_input_data[0]).strip()
                    _key = (new_input_data[1]).strip()
                    try:
                        self._session[alias].headers[_key] = request_data
                        allure_step(f"[{mTime()}][setheader]-->self._session[{alias}].headers[{_key}]==>>{request_data}")
                    except:
                        msg = f"[{mTime()}][setheader]❌ The input session alias '{alias}' incorrect, please check it. self._session{self._session}"
                        allure_step_error(msg)
                        return "FAIL", msg[14:]
                allure_step(f"[{mTime()}][setheader] method return alias '{self._session[alias].headers}'")
                return "PASS", self._session[alias].headers

        except Exception as e:
            msg = f"[{mTime()}][setheader]❌ -->self.session.headers incorrect"
            allure_step_error(msg)
            return "FAIL", msg[14:]

    def setproxy(self, *args):
        """
        A requests session proxies
        :param *args: alias required (excel mode)
        :return: self._session[alias].proxies
        """
        try:
            # if 'headers' in kwargs.keys() and len(kwargs.keys()) != 0:  # py mode
            #     alais = (tuple(args)[0]).strip()
            #     self._session[alais].headers = kwargs['headers']
            #     logger.info(f"[{sys._getframe().f_code.co_name}]-->self._session[{alais}].headers==>>{self._session[alais].headers}")
            #     return self._session[alais].headers
            # elif 'headers' not in kwargs.keys() and len(kwargs.keys()) != 0:  # py mode
            #     logger.error(f'[{sys._getframe().f_code.co_name}]-->{kwargs.keys()} is not correct headers, please check it.')
            # else:  # excel mode
            request_key = str(tuple(args)[0]).strip()
            request_data = str(tuple(args)[1]).strip()
            if ',' not in request_key:
                msg = f'[{mTime()}][setproxy]❌ No session alias, please check it.'
                allure_step_error(msg)
                return "FAIL", msg[14:]
            else:
                new_input_data = request_key.split(',', 1)
                alias = (new_input_data[0]).strip()
                _key = (new_input_data[1]).strip()
                try:
                    self._session[alias].headers[_key] = request_data
                    allure_step(f"[{mTime()}][setproxy]-->self._session[{alias}].proxies[{_key}]==>>{request_data}")
                except:
                    msg = f"[{mTime()}][setproxy]❌ The input session alias '{alias}' incorrect, please check it. self._session{self._session}"
                    allure_step_error(msg)
                    return "FAIL", msg[14:]
            allure_step(f"[{mTime()}][setproxy] method return alias '{self._session[alias].proxies}'")
            return "PASS", self._session[alias].proxies

        except Exception as e:
            msg = f"[{mTime()}][setproxy]❌ -->self.session.proxies incorrect"
            allure_step_error(msg)
            return "FAIL", msg[14:]



    def seturl(self, *args):
        request_key = str(tuple(args)[0]).strip()
        if (request_key is not None) and (request_key.startswith('http')):
            self.baseurl = request_key
            allure_step(f"[{mTime()}][{self.step_num}][seturl]-->{self.baseurl}")
        else:
            msg = f"[{mTime()}][seturl]❌ -->The input URl {self.baseurl} incorrect."
            allure_step_error(msg)
            return "FAIL", msg[14:]
        allure_step(f"[{mTime()}][seturl] method return value:{self.baseurl}")
        return "PASS", self.baseurl


    def get_api(self, *args, **kwargs):
        """
        for excel mode only (py mode prohibited use)
        :param *args: required (excel mode)
        :param **kwargs: required (py mode)
        :return: status_code/self.resp_json
        """
        __session, url = self.__get_alais_url(args)
        new_url = self.__url(url)
        if '${' in new_url:
            new_url = self.__get_relations(new_url)
        allure_step(f"[{mTime()}][{self.step_num}][get_api] before-->[URL:{new_url}],[*ARGS:{args}],[**KWARGS:{kwargs}]")
        allure_step(f"[{mTime()}][{self.step_num}][get_api] before-->__session[{__session}]")
        if self._json:
            kwargs['params'] = self._json
            allure_step(f"[{mTime()}][get_api] before-->kwargs[params]<==>self._json==>>[{self._json}]")
        kwargs['timeout'] = 1
        try:
            res = __session.get(new_url, **kwargs)
        except Exception as e:
            allure_step_error(f"[{mTime()}][get_api]❌ WARNING: {e}]")
            self._json = {}
            self.resp_json = {}
            return "FAIL", e
        else:
            try:
                resp = res.json()
                code = res.status_code
                allure_step(f"[{mTime()}][get_api] after-->[Response.status_code==>>{code}]")
                allure_step(f"[{mTime()}][get_api] after-->[Response.json()==>>{resp}]")
            except Exception as msg:
                allure_step_error(f"[{mTime()}][get_api]❌ WARNING: {msg}]")
                code = res.status_code
                resp = res.text
                allure_step(f"[{mTime()}][get_api] after-->[Response.status_code==>>{code}]")
                allure_step(f"[{mTime()}][get_api] after-->[Response.text==>>\n{resp}]")
            else:
                self._json = {}
                self.resp_json = resp
                allure_step(f"[{mTime()}][get_api] method return alias:[{code}/{resp}]")
                return "PASS", (code, resp)

    def post_api(self, *args, **kwargs):
        """
        for excel mode only (py mode prohibited use)
        :param *args: required (excel mode)
        :param **kwargs: required (py mode)
        :return: status_code/self.resp_json
        """
        __session, url = self.__get_alais_url(args)
        new_url = self.__url(url)
        if '${' in new_url:
            new_url = self.__get_relations(new_url)
        allure_step(f"[{mTime()}][post_api] before-->[URL:{new_url}],[*ARGS:{args}],[**KWARGS:{kwargs}]")
        allure_step(f"[{mTime()}][post_api] before-->__session[{__session}]")
        if self._json:
            kwargs['json'] = self._json
            allure_step(f"[{mTime()}][post_api] before-->kwargs[json]<==>self._json==>>[{self._json}]")
        kwargs['timeout'] = 1
        try:
            res = __session.post(new_url, **kwargs)
        except Exception as e:
            allure_step_error(f"[{mTime()}][post_api]❌ WARNING: {e}]")
            self._json = {}
            self.resp_json = {}

            return "FAIL", e
        else:
            try:
                resp = res.json()
                code = res.status_code
                allure_step(f"[{mTime()}][post_api] after-->[Response.status_code==>>{code}]")
                allure_step(f"[{mTime()}][post_api] after-->[Response.json()==>>{resp}]")
            except Exception as msg:
                allure_step_error(f"[{mTime()}][post_api]❌ WARNING: {msg}]")
                code = res.status_code
                resp = res.text
                allure_step(f"warning: {msg}")
                allure_step(f"[{mTime()}][post_api] after-->[Response.status_code==>>{code}]")
                allure_step(f"[{mTime()}][post_api] after-->[Response.text==>>\n{resp}]")
            else:
                self._json = {}
                self.resp_json = resp
                allure_step(f"[{mTime()}][post_api] method return alias:[{code}/{resp}]")
                return "PASS", (code, resp)

    def savejson(self, *args, **kwargs):
        """
        for get_api/post_api params/data/json (if py mode, json={'p': 'p1'})
        if tuple(args)[0] == '', tuple(args)[1] required dict
        if tuple(args)[0] != '', tuple(args)[1] any
        :param *args: required (excel mode)
        :param **kwargs: required (py mode)
        :return: dict/self._json
        """
        # if 'json' in kwargs.keys() and len(kwargs.keys()) != 0:  # py mode
        #     self._json.update(kwargs['json'])
        #     logger.info(f"[{sys._getframe().f_code.co_name}]-->self._json.update(kwargs['json'])==>>{self._json}")
        #     return self._json
        # elif 'data' in kwargs.keys() and len(kwargs.keys()) != 0:  # py mode
        #     self._json.update(kwargs['data'])
        #     logger.info(f"[{sys._getframe().f_code.co_name}]-->self._json.update(kwargs['data'])==>>{self._json}")
        #     return self._json
        # elif 'params' in kwargs.keys() and len(kwargs.keys()) != 0:  # py mode
        #     self._json.update(kwargs['params'])
        #     logger.info(f"[{sys._getframe().f_code.co_name}]-->self._json.update(kwargs['params'])==>>{self._json}")
        #     return self._json
        # elif 'params' not in kwargs.keys() and 'data' not in kwargs.keys() and 'json' not in kwargs.keys() and len(kwargs.keys()) != 0:  # py mode
        #     logger.error(f"[{sys._getframe().f_code.co_name}]-->{kwargs.keys()} is not corrrect parameters, please check it. [params/data/json]")
        # else:  # excel mode
        _dict = {}
        try:
            input_data = (tuple(args)[0]).strip()
            request_data = str(tuple(args)[1])
            allure_step(f"[{mTime()}][savejson] before-->[*ARGS:{args}],[**KWARGS:{kwargs}]")
            if (request_data.strip().startswith('{') and request_data.strip().endswith('}')) or (request_data.strip().startswith('[') and request_data.strip().endswith(']')):
                _vlue = request_data.strip().replace('\'', '"').replace('\n', '').replace('\r', '').replace('\t', '')
                _vluen = self.__get_relations(_vlue)
                try:
                    _dict = json.loads(str(_vluen))
                except Exception as e:
                    msg = f"[{mTime()}][savejson]❌ convert dict error"
                    allure_step_error(msg)
                    return "FAIL", msg[14:]
                if input_data == '':
                    self._json = _dict
                else:
                    self._json[input_data] = _dict
                allure_step(f"[{mTime()}][savejson] after-->self._json==>>[{self._json}]")
                allure_step(f"[{mTime()}][savejson] method return value:[{self._json}]")
                return "PASS", _dict
            else:
                _valuen = self.__get_relations(request_data)
                self._json[input_data] = _valuen
                allure_step(f"[{mTime()}][savejson] after-->self._json[{input_data}]==>>[{_valuen}]")
                allure_step(f"[{mTime()}][savejson] method return value:[{_valuen}]")
                return "PASS", {f"{input_data}": f"{_valuen}"}
        except Exception as e:
            msg = f"[{mTime()}][savejson]❌ convert dict error."
            allure_step_error(msg)
            return "FAIL", msg[14:]

    def save2dict(self, *args, **kwargs):
        """
        get vlaue from self.resp_json to self.relations[key]=value
        1. to self.relations['xcode']=10001 from self.resp_json['a']['b']
        2. to self.relations['xcode']=10001 if args contains '=' e.g. =10001
        """
        try:
            request_key = (tuple(args)[0]).strip()
            request_data = str(tuple(args)[1])
            allure_step(f"[{mTime()}][save2dict] before-->[*ARGS:{args}],[**KWARGS:{kwargs}]")
            if request_data.startswith('='):
                request_data_value = self.__get_relations(request_data[1:])
                self.relations[request_key] = request_data_value
            else:  # get data from self.resp_json
                request_data_path, end = self.__abs(request_data)
                if jsonpath.jsonpath(self.resp_json, f"$..{end}") is False:
                    msg = f"[{mTime()}][save2dict] The input path '{end}' not in self.resp_josn, please check it. self.resp_json:\n{self.resp_json}"
                    allure_step_error(msg)
                    return "FAIL", msg[14:]
                else:
                    request_data_value = eval(str(self.resp_json) + str(request_data_path))
                    self.relations[request_key] = request_data_value

            allure_step(f"[{mTime()}][save2dict] after-->self.relations[{request_key}]==>>[{self.relations[request_key]}]")
            allure_step(f"[{mTime()}][save2dict] method return value:[{request_data_value}]")
            return "PASS", {f"{request_key}": f"{request_data_value}"}
        except Exception as e:
            msg = f"[{mTime()}][save2dict]❌ save dict error.."
            allure_step_error(msg)
            return "FAIL", msg[14:]

    def put_api(self):
        pass
    def delete_api(self):
        pass

    def __abs(self, datan):
        """ for savejson """
        dataL = datan.split(',')
        tmp = ''
        for one in dataL:
            if one.strip().isdigit():
                tmp = tmp + f"[{one.strip()}]"
            else:
                tmp = tmp + f"['{one.strip()}']"
        allure_step(f"[{mTime()}]----------数据预处理after:--__abs(datan)>>{datan}>>{tmp}--")
        return tmp, dataL[-1:][0]






    def __get_relations(self, param):
        pattern = r'[$][{](.*?)[}]'
        if param is None or param == '':
            return ''
        else:
            for key in self.relations.keys():
                res = re.findall(pattern, param)
                if res:
                    for r in res:
                        if r == key:
                            param = param.replace('${' + key + '}', str(self.relations[key]))
                            allure_step(f"[{mTime()}]----------数据预处理after:--self.relations[{key}]>>{self.relations[key]}--")
            return param

    def assertInJson(self, *args):
        """
        get value through jsonpath(self.resp_json, f'$..{json_path}')
        WARNING: get jsonpath value maybe not unipue
        :param json_path:
        :param expect_value:
        """
        input_data = (tuple(args)[0]).strip()
        request_data = tuple(args)[1]
        allure_step(f"[{mTime()}][assertInJson] before--> self.resp_json==>>{self.resp_json}")
        allure_step(f"[{mTime()}][assertInJson] before--> request_data(expect)==>>{request_data}")
        res = jsonpath.jsonpath(self.resp_json, f'$..{input_data}')  # 找不到是结果是 False

        allure_step(f"[{mTime()}][assertInJson] ACTUAL_VALUE:[{res}]")
        allure_step(f"[{mTime()}][assertInJson] EXPECT_VALUE:[{request_data}]")
        try:
            if isinstance(res, list) and len(res) == 1:
                assert request_data == res[0]
            elif isinstance(res, list) and len(res) > 1:
                assert request_data in res
            else:
                assert request_data == res
        except AssertionError as e:
            msg = f"[{mTime()}][assertInJson]❌ "
            allure_step_error(msg + "FAIL")
            # allure_step_error(f"[{mTime()}][assertInJson]❌ FAIL")
            return "FAIL", f' ACTUAL_VALUE :[{res}]' + f' EXPECT_VALUE :[{request_data}]'
        else:
            allure_step(f"[{mTime()}] PASS")
            return 'PASS', f'ACTUAL_VALUE :{res}' + f'<>EXPECT_VALUE :{request_data}'

    def assertAbsPath(self, *args):
        """
        get value from self.resp_json[absolute_path_value] tp compare
        {"a": [{"b": "b1"}, {"c": "c1"}]}
        assertAbsPath(self, 'a[0].b', 'b1')
        doc: https://jmespath.org/
        :param abs_path:
        :param expect_value:
        """
        abs_path = (tuple(args)[0]).strip()
        request_data = tuple(args)[1]
        allure_step(f"[{mTime()}][assertAbsPath] before-->self.resp_json==>>{self.resp_json}")
        allure_step(f"[{mTime()}][assertAbsPath] before-->request_data(expect)==>>{request_data}")

        search_value = jmespath.search(abs_path, self.resp_json)
        allure_step(f"[{mTime()}][assertAbsPath] :[{search_value}]")
        allure_step(f"[{mTime()}][assertAbsPath] EXPECT_VALUE:[{request_data}]")
        try:
            assert search_value == request_data
        except AssertionError as e:
            msg = f"[{mTime()}][assertAbsPath]❌ "
            allure_step_error(msg + "FAIL")
            # allure_step_error(f"[{mTime()}][assertAbsPath]❌ FAIL")
            return "FAIL", f'ACTUAL_VALUE :[{search_value}]' + f'<>EXPECT_VALUE :[{request_data}]'
        else:
            allure_step(f"[{mTime()}][assertAbsPath] PASS")
            return 'PASS', f'ACTUAL_VALUE :{search_value}' + f'<>EXPECT_VALUE :{request_data}'

    def assertResp2Json(self, *args):
        """
        compare expect_dict and self.resp_json
        assertResp2Json(self, z, {"a": [{"b": "b1"}, {"c": "c1"}]})
        :param expect_dict: dict only
        """
        expect_json = str(tuple(args)[1])
        allure_step(f"[{mTime()}][assertResp2Json] before-->self.resp_json==>>{self.resp_json}")
        allure_step(f"[{mTime()}][assertResp2Json] before-->request_data(expect)==>>{expect_json}")
        if expect_json.startswith('{') or expect_json.startswith('['):
            _value = str(expect_json).strip().replace('\'', '"').replace('\n', '').replace('\r', '').replace('\t', '')
            _valuen = self.__get_relations(_value)
            try:
                _dict = json.loads(str(_valuen))
            except Exception as e:
                msg = f"[{mTime()}][assertResp2Json]❌ after--> convert request_data to dict error.{expect_json}"
                allure_step_error(msg)
                allure_step_error(f"[{mTime()}][assertResp2Json]❌ FAIL")
                return "FAIL", msg[14:]
        else:
            msg = f"[{mTime()}][assertResp2Json]❌ The input request_data '{expect_json}' incorrect, should be dict string."
            allure_step_error(msg)
            return "FAIL", msg[14:]
        error_count = HandleJson().json_assert(self.resp_json, _dict)
        allure_step(f"[{mTime()}][assertResp2Json] ACTUAL_VALUE:[{self.resp_json}]")
        allure_step(f"[{mTime()}][assertResp2Json] EXPECT_VALUE:[{_dict}]")
        try:
            assert error_count == 0
        except AssertionError as e:
            msg = f"[{mTime()}][assertResp2Json]❌ "
            allure_step_error(msg + "FAIL")
            # allure_step_error(f"[{mTime()}][assertResp2Json]❌ FAIL")
            return "FAIL", f'ACTUAL_VALUE :{self.resp_json}' + f'<>EXPECT_VALUE :{_dict}'
        else:
            allure_step(f"[{mTime()}][assertResp2Json] PASS")
            return 'PASS', f'ACTUAL_VALUE :{self.resp_json}' + f'<>EXPECT_VALUE :{_dict}'

    def assertMatch2Json(self, *args, **kwargs):
        """
        match dict/str from self.resp_json to compare
        self.resp_json = {"a": [{"b": "b1"}, {"c": "c1"}]}
        assertMatch2Json(self, 'a[0]', '{"b": "b1"}')
        doc: https://jmespath.org/
        :param part_path: get value from self.resp_json[part_path]
        :param expect_value: dict/str
        """
        part_path = str(tuple(args)[0]).strip()
        expect_json = str(tuple(args)[1])
        allure_step(f"[{mTime()}][assertMatch2Json] before-->self.resp_json==>>{self.resp_json}")
        allure_step(f"[{mTime()}][assertMatch2Json] before-->request_data(expect)==>>{expect_json}")
        search_value = jmespath.search(part_path, self.resp_json)
        allure_step(f"[{mTime()}][assertMatch2Json] after-->self.resp_json.{part_path}==>>{search_value}")
        if expect_json.strip().startswith('{') or expect_json.strip().startswith('['):
            _value = expect_json.strip().replace('\'', '"').replace('\n', '').replace('\r', '').replace('\t', '')
            _valuen = self.__get_relations(_value)
            try:
                _dict = json.loads(str(_valuen))
            except Exception as e:
                msg = f"[{mTime()}][assertMatch2Json]❌ after--> convert request_data to dict error.{expect_json}"
                allure_step_error(msg)
                return "FAIL", msg[14:]

            error_count = HandleJson().json_assert(search_value, _dict)
            allure_step(f"[{mTime()}][assertMatch2Json] ACTUAL_VALUE:[{self.resp_json}]")
            allure_step(f"[{mTime()}][assertMatch2Json] EXPECT_VALUE:[{_dict}]")
            try:
                assert error_count == 0
            except AssertionError as e:
                msg = f"[{mTime()}][assertMatch2Json]❌ "
                allure_step_error(msg + "FAIL")
                # allure_step_error(f"[{mTime()}][assertMatch2Json]❌ FAIL")
                return "FAIL", msg[14:] + f' ACTUAL_VALUE :{self.resp_json}' + f'<>EXPECT_VALUE :{_dict}'
            else:
                allure_step(f"[{mTime()}][assertMatch2Json] PASS")
                return 'PASS', f'ACTUAL_VALUE :{self.resp_json}' + f'<>EXPECT_VALUE :{_dict}'
        else:  # should be str value, not dict
            _valuen = self.__get_relations(expect_json)

            allure_step(f"[{mTime()}][assertMatch2Json] ACTUAL_VALUE:[{self.resp_json}]")
            allure_step(f"[{mTime()}][assertMatch2Json] EXPECT_VALUE:[{_valuen}]")
            try:
                assert search_value == _valuen
            except AssertionError as e:
                msg = f"[{mTime()}][assertMatch2Json]❌ "
                allure_step_error(msg + "FAIL")
                return "FAIL", f'ACTUAL_VALUE :{search_value}' + f'<>EXPECT_VALUE :{_valuen}'
            else:
                allure_step(f"[{mTime()}][assertMatch2Json] PASS")
                return 'PASS', f'ACTUAL_VALUE :{search_value}' + f'<>EXPECT_VALUE :{_valuen}'

def allure_step(value):
    with allure.step(value):
        logger.info(value[14:])

def allure_step_error(value):
    with allure.step(value):
        logger.info(value[14:])

if __name__ == '__main__':
    pass
