#!/usr/bin/env python3

import json, os
from pprint import pprint
from jinja2 import Environment, FileSystemLoader, select_autoescape

if __name__ == "__main__":

    jsn = json.load( open( "samples/jinja_data.json" ) )

    pprint( jsn )

    env = Environment( loader=FileSystemLoader('samples/'))
    template = env.get_template('jinja_template.tmpl')

    print( template.render( jsn ) )
