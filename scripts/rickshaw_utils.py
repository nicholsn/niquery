'''
Created on Sep 6, 2012

@author: detwiler
'''
import Pyro4
import json


# Boynton's 11 visually distinct colors (minus white)                    
colors = ['#111111','#0000FF','#FF0000','00FF00','#FFFF00','#FF00FF','#FF8080','#808080','#800000','#FF8000']

simple_time_cls = None

def get_color_for_index(index):
    # colors are repeated after exceeding color list size
    color_index = index % len(colors)
    return colors[color_index]

def get_timeseries_rickshaw(guids,x,y,z):
    all_series = []
    for index in range(0,len(guids)):
        guid = guids[index]
        dc_proxy = Pyro4.Proxy(guid)
        st =  get_simple_time_class(dc_proxy)() #dc_proxy.get_workflow_providers()["SimpleTime"]()
        kwargs = {'dc_uri':guid,'x':x,'y':y,'z':z}
        series_values = st.execute(**kwargs)
        
        #TODO, from what field should I pull a series name (i.e. subject_id, resource_id, ?)
        series = {'color':get_color_for_index(index),'data':transform_series(series_values)}
        all_series.append(series)
    json_series = json.dumps(all_series)
    #print json_series #for debug only
    return json_series

        

'''       
var data = [{
            "y" : 1439.3468017578125,
            "x" : 0
        }, {
            "y" : 1436.3828125,
            "x" : 1
        },
'''
            
def transform_series(series):
    transformed_series = []
    for index in range(0,len(series)):
        new_data_point = {'y':series[index],'x':index}
        transformed_series.append(new_data_point)
    return transformed_series

def get_simple_time_class(dc):
    global simple_time_cls
    if simple_time_cls is None:
        for workflow in dc.get_workflow_providers():
            cls_name = workflow.__name__
            if cls_name == 'SimpleTime':
                simple_time_cls = workflow
                return simple_time_cls
    return simple_time_cls