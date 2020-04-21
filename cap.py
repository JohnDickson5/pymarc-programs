from pymarc import MARCReader

def main():
    with open('input_mrc/input.mrc', 'rb') as fh:
        # Open the record and encode as unicode, to prevent errors
        reader = MARCReader(fh, to_unicode=True, force_utf8=True)
        count = 0
        for record in reader:
            for field in record.fields:
                if field.tag in ['006', '007']:
                    o = field.__str__()
                    if not field.data.islower():
                        field.data = field.data.lower()
                        count += 1
                if field.tag == '007':
                    print(field.data)
            # # Write the edited record to a new file
            # with open('output_mrc/006mangled.mrc', 'ab') as out:
            #     out.write(record.as_marc())
        print(count)

if __name__ == '__main__':
    main()
