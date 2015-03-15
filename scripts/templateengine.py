from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('template'))


def renderTemplate(templateName, dictionary):
	template = env.get_template(templateName)
	return template.render(dictionary)
