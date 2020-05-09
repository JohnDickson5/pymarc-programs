from pymarc import MARCReader
from helpers import *
from collections import Counter

any_punct = ['!', '"', '#', '$', '%', '&', '\'', '(', ')', '*', '+', ',', '-',
             '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^',
             '_', '`', '{', '|', '}', '~', 'ʹ', '·', '♭', '®', '±', 'ʺ', '£',
             '°', '℗', '©', '♯', '¿', '¡' '€']

control_subs = ['u', 'w', 'x', 'z', '0', '1', '2', '3', '4', '5', '6', '7',
                '8', '9']

c = Counter()

field_dict = {}



for i in range(1, 1000):
    field_dict[f'{i:03}'] = Counter()


with open('input_mrc/input.mrc', 'rb') as fh:
    # Open the record and encode as unicode, to prevent errors
    reader = MARCReader(fh, to_unicode=True, force_utf8=True)
    try:
        for record in reader:
            for field in record.fields:
                if not field.is_control_field():
                    last_subcode_pos = len(field.subfields) - 2
                    try:
                        # Cycle backwards through subfield codes until subfield which is
                        # neither a control subfield nor exempt is found
                        while (field.subfields[last_subcode_pos] in control_subs
                                and last_subcode_pos > 0):
                            last_subcode_pos = last_subcode_pos - 2
                        # Return the location of the data of the last subfield
                        last_subdata_pos = last_subcode_pos + 1
                        # Check that the last_subcode_pos appears to be occupied by a code
                        if (len(field.subfields[last_subcode_pos]) == 1
                                and last_subcode_pos % 2 == 0):
                            last_chr = field.subfields[last_subdata_pos][-1:]
                    except IndexError:
                        pass
                    field_dict[field.tag][last_chr] += 1
    except UnicodeDecodeError:
        pass


for key in field_dict:
    if field_dict[key]:
        with open('output_mrc/chrcounts.txt', 'a', encoding="utf-8") as out:
            for c in field_dict[key]:
                if key and c and field_dict[key][c]:
                    line = (str(key)
                            + '\t' + str(c) + '\t' + str(field_dict[key][c])
                            + '\n')
                    try:
                        out.write(line)
                    except UnicodeEncodeError as e:
                        print(e)
                else:
                    print(f'key: {key}')
                    print(f'c: {c}')
                    print(f'field_dict[key][c]: {field_dict[key][c]}')
