from jinja2 import FileSystemLoader
from jinja2.environment import Environment

def render(template, folder="templates", **kwargs):
    env = Environment()

    env.loader = FileSystemLoader(folder)

    template = env.get_template(template)
    
    return template.render(**kwargs)
