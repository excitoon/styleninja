import re


def parse(data):
    blocks = []
    pos = 0
    last_pos = 0
    match = None

    def save_match(new_match):
        nonlocal match
        match = new_match
        return match

    def set_type(type):
        nonlocal pos
        nonlocal last_pos
        nonlocal data
        nonlocal blocks
        begin = last_pos
        end = pos
        if begin == end:
            return
        if len(blocks) == 0 or blocks[-1]['type'] != type or blocks[-1]['type'] == 'newline':
            blocks.append({ 'type': type, 'data': data[begin:end] })
        else:
            blocks[-1]['data'] += data[begin:end]
        last_pos = pos

    def last_blocks_from(type):
        nonlocal blocks
        for idx in range(len(blocks)-1, -1, -1):
            if blocks[idx]['type'] == type:
                break
            yield blocks[idx]

    def check_only(type, generator):
        for item in generator:
            if item['type'] != type:
                return False
        return True

    while pos < len(data):
        until_end = len(data)-pos-1
        symbol = data[pos]
        next_symbol = data[pos+1] if until_end > 0 else ''
        if symbol == '#' and check_only('whitespace', last_blocks_from('newline')):
            pos += 1
            until_end = len(data)-pos-1
            next_symbol = data[pos+1] if until_end > 0 else ''
            while pos < len(data):
                symbol = data[pos]
                until_end = len(data)-pos-1
                next_symbol = data[pos+1] if until_end > 0 else ''
                if symbol == '\\' and next_symbol == '\n':
                    pos += 1
                    set_type('directive')
                    pos += 1
                    set_type('newline')
                elif symbol == '\n':
                    break
                else:
                    pos += 1
            set_type('directive')
        if symbol == ' ' or symbol == '\t' or symbol == '\r':
            pos += 1
            set_type('whitespace')
        elif symbol == '/' and next_symbol == '/':
            pos += 2
            while pos < len(data):
                symbol = data[pos]
                if symbol == '\n':
                    break
                else:
                    pos += 1
            set_type('comment')
        elif symbol == '/' and next_symbol == '*':
            pos += 2
            while pos < len(data):
                symbol = data[pos]
                until_end = len(data)-pos-1
                next_symbol = data[pos+1] if until_end > 0 else ''
                if symbol == '*' and next_symbol == '/':
                    pos += 2
                    break
                elif symbol == '\n':
                    set_type('comment')
                    pos += 1
                    set_type('newline')
                else:
                    pos += 1
            set_type('comment')
        elif symbol == '\n':
            pos += 1
            set_type('newline')
        elif save_match(re.search('^(|u8?|U|L)?"', data[pos:pos+3])) != None:
            prefix = match.group(1)
            pos += len(match.group(0))
            while pos < len(data):
                symbol = data[pos]
                if symbol == '\\' and (next_symbol == '"' or next_symbol == '\\'):
                    pos += 2
                elif symbol == '"':
                    pos += 1
                    break
                else:
                    pos += 1
            set_type('string')
        elif save_match(re.search('^(|u8?|U|L)?R"([^()\n\\ ]{0,16})\\(', data[pos:pos+21])) != None:
            prefix = match.group(1)
            delimiter = match.group(2)
            pos += len(match.group(0))
            match_end = data[pos:].find(')' + delimiter + '"')
            pos = match_end + pos if match_end != -1 else len(data)
            set_type('string')
        elif re.search('[0-9]', symbol) != None:
            pos += 1
            while pos < len(data):
                symbol = data[pos]
                if re.search('[0-9.a-zA-Z_]', symbol) == None:
                    break
                else:
                    pos += 1
            set_type('integer')
        elif re.search('[a-zA-Z_]', symbol) != None:
            pos += 1
            while pos < len(data):
                symbol = data[pos]
                if re.search('[a-zA-Z0-9_]', symbol) == None:
                    break
                else:
                    pos += 1
            set_type('name')
        else:
            pos += 1
            set_type('unknown')

    return blocks
