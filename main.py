def parse(query: str) -> dict:
    first = query.split('?')
    second = first[-1].split('&')
    exit = {}
    for i in second:
        if len(i) <= 1:
            continue
        try:
            exit.update({i.split('=')[0] : i.split('=')[1]})
        except:
            continue
    return exit

if __name__ == '__main__':
    assert parse('https://example.com/path/to/page?name=ferret&color=purple') == {'name': 'ferret', 'color': 'purple'}
    assert parse('https://example.com/path/to/page?name=ferret&color=purple&') == {'name': 'ferret', 'color': 'purple'}
    assert parse('http://example.com/') == {}
    assert parse('http://example.com/?') == {}
    assert parse('http://example.com/?name=Dima') == {'name': 'Dima'}

def parse_cookie(query: str) -> dict:
    first = query.split(';')
    exit = {}
    for i in first:
        if len(i) <= 1:
            continue
        exit.update({i.split('=')[0] : str(i.split('=',1)[1])})
    return exit


if __name__ == '__main__':
    assert parse_cookie('name=Dima;') == {'name': 'Dima'}
    assert parse_cookie('') == {}
    assert parse_cookie('name=Dima;age=28;') == {'name': 'Dima', 'age': '28'}
    assert parse_cookie('name=Dima=User;age=28;') == {'name': 'Dima=User', 'age': '28'}


