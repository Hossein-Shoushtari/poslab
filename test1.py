

def test(x):
    liste = tuple([i for i in range(5)])
    return *liste


print(test(2))
