import ast
import web
import Pyro4
import json
import rickshaw_utils as rick
import Client

urls = ('/', 'NIQWebServer')
render = web.template.render('templates/')

app = web.application(urls, globals())

#my_form = web.form.Form(web.form.Textbox('', class_='textfield', id='textfield'))  

def populate_metadata_url_dict():
    m_url_dict = {}
    services = client.get_niq_services()
    for k, v in services.iteritems():
        try:
            niq = client.create_niq_for_service_name(k)
            session = client.create_session_for_niq(niq)
            metadata_url = niq.get_metadata_url()
            m_url_dict[k] = [session, metadata_url]
            # should there be a break here?
        except Pyro4.errors.PyroError as e:
            print "Pyro error: {0}, for service {1}".format(e,k)
    return m_url_dict

Pyro4.config.HMAC_KEY=b'BF7FFE77BFABDB26B35CABC5528EC'
client = Client.Client()
metadata_url_dict = populate_metadata_url_dict()

#def create_session(service_name):
#    niq = client.create_niq_for_service_name(service_name)
#    session = client.create_session_for_niq(niq)
#    metadata_url = niq.get_metadata_url()
#    metadata_url_dict[service_name] = [session,metadata_url]
#    return session



class NIQWebServer:
    #stanford_session = create_session('niq.uw');
    #self.ibic_session = create_session('niq.ibic');
    
    def GET(self):
        #form = my_form()
        #return render.index(form, "Query results will go here.")
        return render.index()
        
    def POST(self):
        user_data = web.input()
        if user_data.form_type == 'query_form':
            return self.process_query()
        elif user_data.form_type == "simple_time":
            return self.process_time_series()
        else:
            return
    
    def process_query(self):
        user_data = web.input()

        qid = user_data.query_num
        age = user_data.age
        sex = user_data.sex
        
        
        # issue queries and build up results table (NOTE: generation of html perhaps should be done in javascript)
        guids = []
        out_list = []
        out_list.append("<table id='result_table'><tr><th>Location</th><th>Sex</th><th>Age</th><th>Data</th><th>View</th></tr>")
        for k, v in metadata_url_dict.iteritems():
            try:
                args = {v[1]+","+sex+","+age}
                results = v[0].execute_param_query(qid,args)
                #all_results = []
                
                        #out_list.append("<tr><td>"+age+"</td><td>"+sex+"</td></tr>")
                for result in results:
                    guids.append(result.asString())
                    dc_proxy = Pyro4.Proxy(result)
                    data_uri = dc_proxy.get_uri()
                    view_url = vis_url = dc_proxy.get_uri().replace('nii.gz','html')#client.get_visualization_url)
                    out_list.append("<tr><td>"+k+"</td><td>"+dc_proxy.get_subject_info()['info']['sex']+
                                    "</td><td>"+dc_proxy.get_subject_info()['info']['age']+
                                    "</td><td><a href='"+data_uri+"'>"+data_uri+"</a>"+
                                    "</td><td><a target='_blank' href='"+view_url+"'>"+view_url+"</a></td></tr>")
                    print "workflow providers: "+str(dc_proxy.get_workflow_provider_descriptions())
            except SyntaxError as e:
                print "Syntax error: {0}, from service {1}".format(e,k)
                #all_results.append(dc_proxy.get_resource_info())
                #all_results.append(json.dumps(dc_proxy.get_resource_info()))
        out_list.append("</table>")
        
        # generate form for visualization
        out_list.append("<form id='time_series_from' action='/static/timeseries/index.html'>")
        out_list.append("<input name='dc_guids' type='hidden' value='"+''.join(json.dumps(guids).split())+"'>")
        out_list.append("<input class='button' id='vis_send_button' type='submit' value='visualize time series'/>")
        out_list.append("</form>")

        return ''.join(out_list)
    
    def process_time_series(self):
        user_data = web.input()

        guids_string = user_data.dc_guids
        guids = ast.literal_eval(guids_string)
        x = user_data.x
        y = user_data.y
        z = user_data.z
        return rick.get_timeseries_rickshaw(guids, x, y, z)
    
        
        
    
#    def get_query_metadata(self,uri):
#        user_data = web.input()
#        session = create_session('niq.uw')
#        results = session.execute_query(284)
#        all_results = []
#        for result in results:
#            dc_proxy = Pyro4.Proxy(result)
#            #all_results.append(dc_proxy.get_resource_info())
#            all_results.append(json.dumps(dc_proxy.get_resource_info()))
#        return all_results
            

if __name__ == '__main__':
    app.run()

