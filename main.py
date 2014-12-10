from pprint import pprint
from symbol import Symbol
from environment import Environment


def Eval(item, env):
    #pprint("Evaluating %s" % item)
    if isinstance(item, Symbol) and item.get_value() == '%env':
        pprint('>> Env: %s' % env)
        return item
    if isinstance(item, Symbol):
        return value_of_symbol(item, env)
    elif isinstance(item, list):
        return eval_list(item, env)
    else:
        #pprint(">> returning item")
        return item


def eval_list(items, env):
    #pprint("Evaluating the list: %s" % items)
    first_element = items[0]
    #pprint("First element is: %s" % first_element)

    if is_a_lambda(first_element):
        #pprint("It's a lambda: %s" % items)
        (_, vars, exp) = items
        return lambda *args: Eval(exp, Environment([v.get_value() for v in vars], args, env))

    elif is_a_binding_definition(first_element):
        (_, binding_name, expression) = items
        env[binding_name.get_value()] = Eval(expression, env)

    elif is_a_sequence(first_element):
        for expression in items[1:]:
            result = Eval(expression, env)
        return result

    else:
        pprint('Calling procedure, current items: %s' % items)
        arguments = [Eval(item, env) for item in items]
        procedure = arguments.pop(0)
        pprint('procedure: %s' % (procedure))
        pprint('arguments: %s' % (arguments))
        return procedure(*arguments)


def value_of_symbol(symbol, env):
    return Eval(env.find_symbol(symbol), env)


def is_a_lambda(element):
    return is_the_builtin_symbol(element, 'lambda')


def is_a_binding_definition(element):
    return is_the_builtin_symbol(element, '=')


def is_a_sequence(element):
    return is_the_builtin_symbol(element, 'do')


def is_the_builtin_symbol(element, symbol):
    return isinstance(element, Symbol) and element.get_value() == symbol
