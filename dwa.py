def combine(*lists):
    temp = []
    for l in lists:
        temp += l
    return list(set(temp))

def combine(*lists):
    temp = []
    for l in lists:
        temp.extend(l)
    return list(dict.fromkeys(temp))


x = combine([1,2], [2,3,4], [4,5])
print(x)

def pretty_print(**kwargs):
    for key, value in kwargs.items():
        print(f"{key.upper()} : {value}")
        
pretty_print(color="red", size=12, bold=True)


def fancy_combine(*args, **kwargs):
    temp = []
    for l in args:
        temp.extend(l)
    
    # Usuń duplikaty jeśli unique=True
    if kwargs.get("unique", True):
        temp = list(dict.fromkeys(temp))

    # Posortuj jeśli sort=True
    if kwargs.get("sort", False):
        temp.sort()

    # Odwróć jeśli reverse=True
    if kwargs.get("reverse", False):
        temp.reverse()

    return temp
result = fancy_combine([1,2,3], [2,3,4], [5], unique=True, sort=True)
print(result)
                
    