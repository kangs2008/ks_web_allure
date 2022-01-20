# -*- coding: utf-8 -*-
import pytest, time
from Common.handle_logger import logger
from Common.handle_config import ReadWriteConfFile
from Common.utils import mDate, mDateTime
from Common.handle_excel3 import excel_to_case
from pathlib import Path
from py.xml import html

@pytest.mark.optionalhook
def pytest_html_results_summary(prefix, summary, postfix):
    prefix.extend([html.p("测试人: xqc")])

@pytest.mark.optionalhook
def pytest_configure(config):
    config._metadata['测试地址'] = 'https://www.baidu.com'


# @pytest.mark.optionalhook
# def pytest_html_results_table_header(cells):
#     cells.insert(2, html.th('Description'))
#     cells.insert(3, html.th('Time', class_='sortable time', col='time'))
#     # cells.insert(1,html.th("Test_nodeid"))
#     cells.pop()
#
#
# @pytest.mark.optionalhook
# def pytest_html_results_table_row(report, cells):
#     cells.insert(2, html.td(report.description))
#     cells.insert(3, html.td(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), class_='col-time'))
#     # cells.insert(1,html.td(report.nodeid))
#     cells.pop()
#
# @pytest.mark.hookwrapper
# def pytest_runtest_makereport(item):
#     """当测试失败的时候，自动截图，展示到html报告中"""
#     pytest_html = item.config.pluginmanager.getplugin('html')
#     outcome = yield
#     report = outcome.get_result()
#     # extra = getattr(report, 'extra', [])
#     #
#     # if report.when == 'call' or report.when == "setup":
#     #     xfail = hasattr(report, 'wasxfail')
#     #     if (report.skipped and xfail) or (report.failed and not xfail):
#     #         _driver = item.funcargs['start_session']
#     #         fn = PageObject(_driver).save_capture_ob('ERROR')
#     #
#     #         extra.append(pytest_html.extras.image(fn))
#     #     report.extra = extra
#     report.description = str(item.function.__doc__)
#     report.nodeid = report.nodeid.encode('utf-8').decode('unicode_escape')




@pytest.fixture(scope="function", autouse=False)
def set_report_folder_api(request):
    """set_report_folder_api
    """
    report_dir = ReadWriteConfFile().get_option('report', 'report_dir_folder')
    logger.info('----set_report_folder_api---report_dir--------')
    if report_dir == '':
        _set_exec_ini('report', 'report_dir_folder', mDate()+'_html_api')
        _set_exec_ini('report', 'report_file_name', f'report_{mDateTime()}.html')
    yield
    _set_exec_ini('report', 'report_dir_folder', '')
    _set_exec_ini('report', 'report_file_name', '')

    _set_exec_ini('test_data', 'excel_file_path', '')
    _set_exec_ini('test_data', 'excel_file_name', '')
    _set_exec_ini('test_data', 'sheet_names', '')
    _set_exec_ini('test_data', 'sheet_rule', '')
    _set_exec_ini('test_data', 'sheet_kvconfig', '')

def _set_exec_ini(section, option, value):
    ReadWriteConfFile().add_section(section)
    ReadWriteConfFile().set_option(section, option, value)


def pytest_generate_tests(metafunc):
    """for TestCasesApi data"""
    if 'data' in metafunc.fixturenames:
        excel_file_path = metafunc.config.getoption("--path").strip()
        excel_file_name = metafunc.config.getoption("--name").strip()
        sheet_names = metafunc.config.getoption("--sheet").strip()
        sheet_rule = metafunc.config.getoption("--rule").strip()
        sheet_kvconfig = metafunc.config.getoption("--conf").strip()
        if excel_file_path.lower() != 'no_set_path':
            ReadWriteConfFile().set_option('test_data', 'excel_file_path', excel_file_path)
            ReadWriteConfFile().set_option('test_data', 'excel_file_name', excel_file_name)
            ReadWriteConfFile().set_option('test_data', 'sheet_names', sheet_names)
            ReadWriteConfFile().set_option('test_data', 'sheet_rule', sheet_rule)
            ReadWriteConfFile().set_option('test_data', 'sheet_kvconfig', sheet_kvconfig)
        else:
            ReadWriteConfFile().get_option('test_data', 'excel_file_path')
            ReadWriteConfFile().get_option('test_data', 'excel_file_name')
            ReadWriteConfFile().get_option('test_data', 'sheet_names')
            ReadWriteConfFile().get_option('test_data', 'sheet_rule')
            ReadWriteConfFile().get_option('test_data', 'sheet_kvconfig')
        if ',' in sheet_names:
             sheet_names = sheet_names.split(',')
        if ',' in sheet_kvconfig:
            sheet_kvconfig = sheet_kvconfig.split(',')
        logger.info(f'----pytest_generate_tests---{metafunc.config.getoption("--path")}--------')


        path = Path().joinpath(excel_file_path, excel_file_name)
        logger.info(f'----pytest_generate_tests---{path}--------')
        logger.info(f'----pytest_generate_tests---path2--------')
        api_data = excel_to_case(path, sheet_names, sheet_rule, sheet_kvconfig)
        logger.info('----pytest_generate_tests---api_data--------')
        metafunc.parametrize('data', api_data)
