#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from owslib.wfs import WebFeatureService
from RequestsLibrary import RequestsLibrary

__version__ = '0.1'

class OGCServiceLibrary(RequestsLibrary):

    def __init__(self):
        super(OGCServiceLibrary,self).__init__()
        self._result = 0
        self._url = ''
        self._service_type = ''
        self._ogc_version = '1.1.0'

    def connect_to_url(self,url):
        """
        Check that we can connect to a given url
        Test framework errors if failure (i.e. NOT response 200), example:
        | Connect to url | my_test_url |
        """
        RequestsLibrary.create_session(self,"URL",url)
        resp = RequestsLibrary.get(self,"URL","/")
        if str(resp.status_code) != "200":
            raise AssertionError("url: %s Status %s Can't connect" % (url,resp.status_code))

    def set_service_url(self,url):
        """
        Set up parameters url for a service
        Only needs to be called once in the suite if the url is not changing, example:
        | Set service url | my_test_url |

        """
        self._url = url

    def get_number_of_wfs_layers(self):
        """
        Get a count of the layers.
        Fail if the layers returned is not equal to the  expected, example:
        | Get number of layers | expected_number_of_layers |

        """
        wfs = WebFeatureService(self._url, version=self._ogc_version)
        self._result = len(wfs.contents)

    def check_for_wfs_layer(self,layer_name):
        """
        Checks for a layer of a given name.
        Fail if the layer name is not found
        | Check for layer | my_layer_name |

        """
        wfs = WebFeatureService(self._url, version=self._ogc_version)
        self._result = layer_name in wfs.contents.keys()

    def result_should_be(self,expected=0):
        """
        Compares two values as strings, fail if not equal, example:
        | Result should be | my_expected_result |

        """
        if str(self._result) != str(expected):
            raise AssertionError("%s == %s" % (self._result, expected))

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'


