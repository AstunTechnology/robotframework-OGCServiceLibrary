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
from owslib.wms import WebMapService
from RequestsLibrary import RequestsLibrary
import os
import math

__version__ = '0.1'


class OGCServiceLibrary(RequestsLibrary):

    def __init__(self):
        super(OGCServiceLibrary, self).__init__()
        self._result = 0
        self._url = ''
        self._service_type = ''
        self._ogc_version = '1.1.0'

    def set_ogc_version(self, ogc_version):
        """
        Set the ogc version (default is 1.1.0)
        use this if you wish to set to something else
        | Set ogc version | version |
        """
        self._ogc_version = ogc_version

    def connect_to_url(self, url):
        """
        Check that we can connect to a given url
        Test framework errors if failure (i.e. NOT response 200), example:
        | Connect to url | my_test_url |
        """
        RequestsLibrary.create_session(self, "URL", url)
        resp = RequestsLibrary.get(self, "URL", "/")
        if str(resp.status_code) != "200":
            raise AssertionError("url: %s Status %s Can't connect" % (url, resp.status_code))

    def set_service_url(self, url):
        """
        Set up parameters url for a service
        Only needs to be called once in the suite if the url is not changing,
        example:
        | Set service url | my_test_url |

        """
        self._url = url

    #WFS Layer methods

    def get_number_of_wfs_layers(self):
        """
        Get a count of the wfs layers for the current service url.
        Returns integer
        | ${num_layers} | Get number of layers |
        | Should Be Equal As Integers | ${num_layers} | 6 |

        """
        wfs = WebFeatureService(self._url, version=self._ogc_version)
        return len(wfs.contents)

    def check_for_wfs_layer(self, layer_name):
        """
        Checks for a layer of a given name for the current service url.
        Returns boolean
        Returns false if the layer name is not found
        | ${layer_exists} | Check for wfs layer | dentists |
        | Should be true | ${layer_exists} |

        """
        wfs = WebFeatureService(self._url, version=self._ogc_version)
        return layer_name in wfs.contents.keys()

    #WMS Layer methods

    def check_for_wms_layer(self, layer_name):
        """
        Checks for a layer of a given name for the current service url.
        Returns boolean, false if the layer name is not found
        | ${layer_exists} | Check for wms layer | ospremium |
        | Should be true | ${layer_exists} |
        """
        wms = WebMapService(self._url, version=self._ogc_version)
        return layer_name in wms.contents.keys()

    def check_advertised_wms_layers(self):
        """
        Makes a GetMap request for each layer advertised by WMS service.
        An exception is raised on failure.
        | Check advertised wms layers |
        """
        wms = WebMapService(self._url, version=self._ogc_version)
        for layer in wms.contents.values():
            wms.getmap(
                layers=[layer.name],
                srs=layer.crsOptions[0],
                bbox=layer.boundingBox[0:-1],
                size=(300, 300),
                format=wms.getOperationByName('GetMap').formatOptions[0])

    def get_wms_image_size(self, layer_name, srs, min_x, min_y, max_x, max_y):
        """
        Get the size of the png image returned for the current service url
        | set service url | ${WMS_URL} |
        | ${image_size_in_kb} | get wms image size | bathymetry | EPSG:4326 | -112 | 55 | -106 | 71 |
        | ${greater_than_5kb} | ${image_size_in_kb} > 5 |
        | Should Be True | ${greater_than_5kb} |
        returns an integer which is the size of the image in kB

        """
        wms = WebMapService(self._url, version=self._ogc_version)

        img = wms.getmap(layers=[layer_name], srs=srs,
                         bbox=(float(min_x),
                               float(min_y),
                               float(max_x),
                               float(max_y)),
                         size=(300, 300), format='image/png')

        out = open('test.png', 'wb')
        out.write(img.read())
        out.close()

        f = open('test.png', 'rb')
        size = os.path.getsize('test.png') / 1024
        f.close()

        os.remove('test.png')

        return int(math.ceil(size))

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
