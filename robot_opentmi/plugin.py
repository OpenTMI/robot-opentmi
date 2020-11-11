"""
Robot Listener for collecting results and upload to OpenTMI
"""
# native modules
import datetime
import os
import uuid
import mimetypes
import multiprocessing
# 3rd party modules
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
from joblib import Parallel, delayed
from opentmi_client import OpenTmiClient
from opentmi_client.api import Result, File, Dut, Provider
# app modules
from . import __robot_info__


# pylint: disable=too-many-instance-attributes
class PythonListener:
    """ Listener class """
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self, host='localhost', token=None, port=None, store_logs=False):
        """
        Listener constructor
        :param host: OpenTMI host uri.
        :param token: OpenTMI access token.
        """
        self._host = f'{host}:{port}' if port else host
        self._client = None
        self._token = token
        self._results = list()
        self._uploaded_success = 0
        self._uploaded_failed = 0
        self._store_logs = store_logs
        self._variables = dict()
        self._metadata = dict()

    # robot hooks

    # pylint: disable=unused-argument
    def start_suite(self, data, result):
        """ Called when a test suite starts. """
        logger.debug('start_suite')
        if len(result.metadata) > 0 and not self._metadata:
            self._metadata = result.metadata
        variables = BuiltIn().get_variables(no_decoration=True)
        if len(variables) > 0 and not self._variables:
            self._variables = variables

    def start_test(self, data, result):
        """ Called when a test case starts. """

    # pylint: disable=too-many-statements,too-many-branches
    def end_test(self, data, _result):
        """ Called when a test case ends. """
        logger.debug('end_test')

        result = Result(tcid=data.name)
        result.campaign = os.environ.get('JOB_NAME', data.parent.longname)
        if _result.message:
            result.execution.note = _result.message
        result.execution.duration = float(_result.elapsedtime)
        result.execution.environment.framework.name = __robot_info__.project_name
        result.execution.environment.framework.version = __robot_info__.version
        result.execution.sut.commit_id = os.environ.get('GIT_COMMIT', "")
        result.execution.sut.branch = os.environ.get('GIT_BRANCH', "")
        result.job.id = os.environ.get('BUILD_TAG', str(uuid.uuid1()))
        try:
            result.execution.verdict = _result.status.lower()
        except Exception as error:  # pylint: disable=broad-except
            logger.warn(error)
            result.execution.verdict = 'inconclusive'

        profiling = dict(
            suite=dict(
                duration=_result.parent.elapsedtime,
                numtests=_result.parent.test_count
            ),
            generated_at=datetime.datetime.now().isoformat(),
        )
        if _result.tags:
            profiling['tags'] = []
        for tag in _result.tags:
            profiling['tags'].append(tag)
        result.execution.profiling = profiling

        for key in self._variables:
            value = self._variables[key]
            if ['LOG_FILE', 'OUTPUT_FILE', 'REPORT_FILE'].__contains__(key):
                if not self._store_logs:
                    logger.debug('Ignore logs')
                    continue
                if not os.path.exists(value):
                    logger.debug(f"{key} file {value} not exists")
                    continue
                file_stats = os.stat(value)
                if file_stats.st_size / (1024 * 1024) > 1.0:
                    logger.debug('avoid uploading huge log files')
                    continue
                file = File()
                file.mime_type = mimetypes.guess_type(value)[0]
                file.name = os.path.basename(value)
                fobj = open(value, "r")
                data = fobj.read()
                fobj.close()
                file.set_data(data)
                continue

        dut = None
        for key in self._metadata:
            value = self._metadata[key]

            # Dut
            if key.startswith('DUT') and not dut:
                dut = Dut()
                dut.type = 'hw'
                result.execution.append_dut(dut)
            if key == 'DUT_TYPE':
                dut.type = value
            if key == 'DUT_SERIAL_NUMBER':
                dut.serial_number = value
            # elif key == 'DUT_PLATFORM':
            #   dut.platform = value
            elif key == 'DUT_VERSION':
                dut.ver = value
            elif key == 'DUT_VENDOR':
                dut.vendor = value
            elif key == 'DUT_MODEL':
                dut.model = value
            elif key == 'DUT_PROVIDER':
                dut.provider = Provider()
                dut.provider.name = value

            # Sut
            elif key == 'SUT_COMPONENT':
                result.execution.sut.append_cut(value)
            elif key == 'SUT_FEATURE':
                result.execution.sut.append_fut(value)
            elif key == 'SUT_COMMIT_ID':
                result.execution.sut.commit_id = value
            elif key == 'SUT_BRANCH':
                result.execution.sut.branch = value

        self._results.append(result)

    def end_suite(self, data, result):
        """ Called when a test suite ends. """

    def close(self):
        """ Called when the whole test execution ends. """
        self._upload_results()

    # Private methods

    def _upload_results(self):
        try:
            # pylint: disable=expression-not-assigned
            [logger.debug(result) for result in self._results]

            self._client = OpenTmiClient(self._host, logger=logger)

            # Login to OpenTMI
            if self._token:
                self._client.login_with_access_token(self._token)
            num_cores = multiprocessing.cpu_count()

            # upload results parallel
            Parallel(n_jobs=num_cores, backend='threading') \
                (delayed(self._upload_result)(result) for result in self._results)

        except Exception as error:  # pylint: disable=broad-except
            logger.error(error)
        else:
            print(f'Uploaded {self._uploaded_success} results to opentmi. ({self._uploaded_failed} failed)')

    def _upload_result(self, result: Result):
        try:
            response = self._client.post_result(result)
            if not response.get('tcRef'):
                self._create_testcase(result)
            self._uploaded_success += 1
        except Exception as error:  # pylint: disable=broad-except
            logger.warn(error)
            self._uploaded_failed += 1

    def _create_testcase(self, result):
        """ create new testcase for DB """
        # @todo
