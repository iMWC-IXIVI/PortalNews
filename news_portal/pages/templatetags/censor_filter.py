from django import template


register = template.Library()

WORDS_CENSOR = ['решение', 'Kaspersky', 'Apple', 'Samsung', 'Также', 'продолжительность']


@register.filter()
def censor(string):
    some_string = ''
    for word in string.split():
        if word in WORDS_CENSOR:
            some_string += word[0] + '*' * (len(word) - 1) + ' '
        else:
            some_string += word + ' '
    return some_string.strip()
