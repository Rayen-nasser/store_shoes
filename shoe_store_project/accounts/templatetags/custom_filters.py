from django import template

register = template.Library()

@register.filter(name='tailwind_message_class')
def tailwind_message_class(message_tag):
    return {
        'debug': 'bg-gray-100 border-l-4 border-gray-500 text-gray-700 p-4',
        'info': 'bg-blue-100 border-l-4 border-blue-500 text-blue-700 p-4',
        'success': 'bg-green-100 border-l-4 border-green-500 text-green-700 p-4',
        'warning': 'bg-yellow-100 border-l-4 border-yellow-500 text-yellow-700 p-4',
        'error': 'bg-red-100 border-l-4 border-red-500 text-red-700 p-4'
    }.get(message_tag, 'bg-gray-100 border-l-4 border-gray-500 text-gray-700 p-4')


@register.filter
def up_to(value, arg):
    return range(value, arg)