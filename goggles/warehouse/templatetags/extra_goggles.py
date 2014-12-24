from django import template

register = template.Library()


def chunks(s, n):
    """Produce `n`-character chunks from `s`."""
    for start in range(0, len(s), n):
        yield s[start:start+n]


def force_new_line(value, size):
    if not value:
        return value

    result = []
    lines = value.splitlines()
    for line in lines:
        if len(line) > size:
            result.extend(chunks(line, size))
        else:
            result.append(line)
    return '\n'.join(result)

register.filter('force_new_line', force_new_line)
