from flask import Flask

try:
    from rdflib_web.lod import lod
except:
    print()



app = Flask(__name__)

app.config['graph'] = my_rdflib_graph
app.register_blueprint(lod)