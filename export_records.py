from pymarc import MARCReader

# The ASCII and ANSEL punctuation marks, with €
punct = ".!\"#$%&'()*+,-/:;<=>?@[\\]^_`{|}~ʹ·♭®±ʺ£°℗©♯¿€"

while True:
    field = input('Enter a field number: ')
    print(field)
    if not field.isdigit() or int(field) > 999:
        print("Not a valid MARC field!")
        continue
    else:
        break

# Change this to whatever file you want to export marc records from
with open('input_mrc/', 'rb') as fh:
    # Open the record and encode as unicode, to prevent errors
    reader = MARCReader(fh, to_unicode=True, force_utf8=True)
    for record in reader:
        if record[field]:
            with open('output_mrc/' + field + '.mrc', 'ab') as out:
                out.write(record.as_marc())
