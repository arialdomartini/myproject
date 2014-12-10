from symbol import Symbol


def literal(token):
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return Symbol(token)


def parse(source_code):
    return parse_ats(to_ats(tokenize(source_code)))


def parse_ats(ats):
    return ats


def to_ats(tokens):
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF')
    token = tokens.pop(0)
    if '(' == token:
        items = []
        while tokens[0] != ')':
            items.append(to_ats(tokens))
        tokens.pop(0)
        return items
    elif ')' == token:
        raise SyntaxError('unexpected )')
    else:
        return literal(token)


def tokenize(source_code):
    replacements = (
        ('(', ' ( '),
        (')', ' ) ')
    )
    expanded_code = reduce(lambda a, kv:
                           a.replace(*kv), replacements, source_code)
    return expanded_code.split()
