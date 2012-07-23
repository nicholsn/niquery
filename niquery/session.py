"""
Created on May 4, 2012

@author: detwiler
"""
import requests
import xml.etree.ElementTree as etree
from datacontainer import DataContainer

class Session(object):
    """
    Session is really more of a query service in this context that issues "datacontainer" URIs

    similarly, should the datacontainer object issue imageservice URIs?

    and image service issue workflowservice URIs?
    """
    # http://purl.org/sig/TemplateQuery?qid=132&args=http://purl.org/sig/Query?qid=159,StudyDesign
    qiQueryURL = "http://purl.org/sig/Query"
    qiTemplateQueryURL = "http://purl.org/sig/TemplateQuery"

    def __init__(self, daemon):
        '''
        Constructor
        '''

        self.daemon = daemon


    #http://purl.org/sig/qi/Query?qid=284
    #session = Session()
    #results = session.execute_query(284)
    #print results
    #formatted_results = session.format_query_results(results)
    #print results

    def get_query_url(self):
        return self.qiQueryURL

    def get_template_query_url(self):
        return self.qiTemplateQueryURL

    def execute_query(self, qid):
        payload = {'qid':qid}
        r = requests.get(self.qiQueryURL, params=payload)
        f_results = self.format_query_results(r.text)
        return f_results

    def execute_param_query(self, qid, args):
        payload = {'qid':qid,'args':args}
        r = requests.get(self.qiTemplateQueryURL, params=payload)
        f_results = self.format_query_results(r.text)
        return f_results

    def format_query_results(self, xml):
        results = []
        xcede2_namespace = '{http://www.xcede.org/xcede-2}'
        root = etree.XML(xml)

        # create one DataContainer per resource element in the results
        resource_nodes = root.findall('.//'+xcede2_namespace+'resource')
        for resource_node in resource_nodes:

            # get acquisition id ref, subject id ref, and project id ref 
            acquisition_id = resource_node.get('acquisitionID')
            subject_id = resource_node.get('subjectID')
            project_id = resource_node.get('projectID')

            # get project info, build project dictionary
            #project_node = root.find('.//'+xcede2_namespace+'project[@ID="'+project_id+'"]')
            project_d = {'id' : project_id}

            # get subject info, build subject dictionary
            subject_node = root.find('.//' + xcede2_namespace + 'subject[@ID="' + subject_id + '"]')
            subject_sex_node = subject_node.find('./' + xcede2_namespace + 'subjectInfo/' + xcede2_namespace + 'sex')
            subject_age_node = subject_node.find('./' + xcede2_namespace + 'subjectInfo/' + xcede2_namespace + 'age')
            subject_handedness_node = subject_node.find('./' + xcede2_namespace + 'subjectInfo/' + xcede2_namespace +
                                                        'handedness')
            subject_info_d = {}
            if subject_sex_node is not None:
                subject_info_d['sex'] = subject_sex_node.text
            if subject_age_node.text is not None:
                subject_info_d['age'] = subject_age_node.text
            if subject_handedness_node is not None:
                subject_info_d['handedness'] = subject_handedness_node.text
            subject_d = {'id' : subject_id, 'info' : subject_info_d}

            # get acquisition info, build acquisition dictionary
            acquisition_node = root.find('.//' + xcede2_namespace + 'acquisition[@ID="' + acquisition_id + '"]')
            acquisition_tr_node = acquisition_node.find('./' + xcede2_namespace + 'acquisitionInfo/' +
                                                        xcede2_namespace + 'tr')
            acquisition_field_strength_node = acquisition_node.find('./' + xcede2_namespace + 'acquisitionInfo/' +
                                                                    xcede2_namespace + 'fieldStrength')
            acquisition_info_d = {}
            if acquisition_tr_node is not None:
                acquisition_info_d['tr'] = acquisition_tr_node.text
            if acquisition_field_strength_node is not None:
                acquisition_info_d['fieldStrength'] = acquisition_field_strength_node.text
            acquisition_d = {'id' : acquisition_id, 'info' : acquisition_info_d}

            # get resource info, build resource dictionary
            resource_id = resource_node.get('ID')
            resource_format = resource_node.get('format')
            resource_uri_node = resource_node.find(xcede2_namespace+'uri')
            resource_elementType_node = resource_node.find(xcede2_namespace+'elementType')
            resource_byteOrder_node = resource_node.find(xcede2_namespace+'byteOrder')
            resource_compression_node = resource_node.find(xcede2_namespace+'compression')
            resource_uri = resource_uri_node.text
            resource_info_d = {}
            if resource_elementType_node is not None:
                resource_info_d['elementType'] = resource_elementType_node.text
            if resource_byteOrder_node is not None:
                resource_info_d['byteOrder'] = resource_byteOrder_node.text
            if resource_compression_node is not None:
                resource_info_d['compression'] = resource_compression_node.text
            resource_d = {'id' : resource_id,
                          'format' : resource_format,
                          'uri' : resource_uri,
                          'info' : resource_info_d}

            # create new data container object for this resource and add to results
            data_container = DataContainer(project_d, subject_d, acquisition_d, resource_d, resource_uri)
            dc_uri = self.daemon.register(data_container)
            results.append(dc_uri)

        return results