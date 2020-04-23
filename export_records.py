from pymarc import MARCReader

# The ASCII and ANSEL punctuation marks, with €
punct = ".!\"#$%&'()*+,-/:;<=>?@[\\]^_`{|}~ʹ·♭®±ʺ£°℗©♯¿€"

while True:
    field = input('Enter a field number: ')
    if not field.isdigit() or int(field) > 999:
        print("Not a valid MARC field!")
        continue
    else:
        break

field_list = ['015', '020', '024', '027', '028', '210', '222']

count = 0

# Change this to whatever file you want to export marc records from
with open('input_mrc/input.mrc', 'rb') as fh:
    # Open the record and encode as unicode, to prevent errors
    reader = MARCReader(fh, to_unicode=True, force_utf8=True)
    try:
        for record in reader:
            if record[field]:
                with open('output_mrc/' + field + '.mrc', 'ab') as out:
                    try:
                        out.write(record.as_marc())
                        count += 1
                    except UnicodeDecodeError as e:
                        print(e)
    except:
        pass

print(f"{count} fields with this subfield.")
