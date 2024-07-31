import os
from django.template import (Template, TemplateDoesNotExist,
                             TemplateSyntaxError, utils)


def get_loaders():
    from django.template.loader import _engine_list
    loaders = []
    for engine in _engine_list():
        loaders.extend(engine.engine.template_loaders)
    return loaders


def get_template_source(name):
    source = None
    for loader in get_loaders():
        if loader.__module__.startswith('dbtemplates.'):
            # Don't give a damn about dbtemplates' own loader.
            continue
        for origin in loader.get_template_sources(name):
            try:
                source = loader.get_contents(origin)
            except (NotImplementedError, TemplateDoesNotExist):
                continue
            if source:
                return source


def check_template_syntax(template):
    try:
        Template(template.content)
    except TemplateSyntaxError as e:
        return (False, e)
    return (True, None)


def update_database_template_content(instance, **kwargs):
    """
    Update database content from its respective file template
    """
    app_template_dirs = utils.get_app_template_dirs('templates')
    templatedirs = [d for d in app_template_dirs if os.path.isdir(d)]
    path = str(templatedirs[0]) + '/' + instance.name

    try:
        with open(path, encoding='utf-8') as f:
            instance.content = f.read()
            instance.save()
        print(f'''Database Template: {instance.name} Content Updated Successfully''')
    except Exception as e:
        print(f'''An Error Occured- {e}''')
