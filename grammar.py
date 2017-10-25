import re


def parse_raw(data):
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
        if pos == last_pos:
            return
        selection = data[last_pos:pos]
        if len(blocks) == 0 or blocks[-1]['type'] != type or type == 'newline' or type == 'unknown':
            blocks.append({ 'type': type, 'data': selection, 'pos': last_pos })
        else:
            blocks[-1]['data'] += selection
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
            pos = match_end + pos + 2 if match_end != -1 else len(data)
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

def parse_blocks(blocks):
    pos = 0
    last_pos = 0

    def parse_blocks_until(until):
        nonlocal pos
        nonlocal last_pos
        nonlocal blocks
        data = []

        open_blocks = '{[('
        close_blocks = '}])'

        while pos < len(blocks):
            block = blocks[pos]
            
            open_pos = open_blocks.find(block['data'])
            close_pos = close_blocks.find(block['data'])
            if block['type'] == 'unknown' and open_pos != -1:
                begin = pos
                pos += 1
                internal = parse_blocks_until(close_blocks[open_pos])
                data.append({ 'type': block['data'], 'data': internal, 'pos': blocks[begin]['pos'], 'end': blocks[pos-1]['pos']+1 })
            elif block['type'] == 'unknown' and block['data'] == until:
                pos += 1
                return data
            else:
                pos += 1
                data.append(block)

        return data

    return parse_blocks_until('the_very_end')
