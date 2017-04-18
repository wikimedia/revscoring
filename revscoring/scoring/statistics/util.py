_round = round


def round(number, ndigits=0):
    if number is None:
        return None
    else:
        return int(_round((number * (10**ndigits)))) / (10**ndigits)

def tab_it_in(string, tabs=1):
    return "".join("\t" * tabs + "{0}\n".format(line)
                   for line in string.split("\n"))
