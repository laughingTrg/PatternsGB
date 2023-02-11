from jinja2 import Template
from os.path import join

def render(template, folder='templates', **kwargs):
    f_path = join(folder, template)

    with open(f_path, encoding='utf-8') as f:
        template = Template(f.read())
    
    return template.render(**kwargs)
