from pymarc import MARCReader

# The ASCII and ANSEL punctuation marks, without a period and with €
any_punct = "!\"#$%&'()*+,-/:;<=>?@[\\]^_`{|}~ʹ·♭®±ʺ£°℗©♯¿€"

control_subs = ['u', 'w', 'x', 'z', '0', '1', '2', '3', '4', '5', '6', '7',
                '8', '9']

linking_entry_fields = ['760', '762', '765', '767', '770', '772', '773',
                        '774', '775', '776', '777', '780', '785', '786',
                        '787']


def append_punct(field, sub_pos, end_str, exempt=[], abbrev_exempt=False):
    """Add a string to the end of a subfield if it does not already
    end in that string or an exemption. For the 'exempt' list, include
    only strings that are always exempt for receiving the ending (that
    is, do not include a period if only periods after abbreviations
    are exempt). By default, fields ending in abbreviations will
    receive the ending, but this can be disabled by changing
    abbreviations_exempt to 'True'.
    """
    # Get the subfield data
    sub = field.subfields[sub_pos]
    # Check that the subfield does not already end in the string
    if not sub.endswith(end_str):
        # Check that the subfield does not end in an exemption
        exempt_ending = False
        for exemption in exempt:
            if sub.endswith(exemption):
                exempt_ending = True
        if not exempt_ending:
            # Warn if the field ends in a period; as periods ending
            # abbreviations are sometimes treated differently from
            # other periods, it is not safe to take action based on an
            # ending period.
            if sub.endswith('.') and abbrev_exempt:
                # TODO: get user input
                print(f"Possible ending abbreviation: {sub}")
            else:
                # Remove partial punctuation or spaces from the end of
                # the subfield
                while sub != '':
                    if sub[-1] in end_str or sub[-1] in ' ':
                        sub = sub[:-1]
                    else:
                        break
                # Edit the subfield
                field.subfields[sub_pos] = ''.join(sub, end_str)


def append_to_each_sub(
        field, sub_code, end_str, exempt=[], abbrev_exempt=False):
    """Add ending punctuation to every instance of a target subfield"""
    # Iterate through all the subfields in the field. Note that
    # field.subfields is a list of subfield codes and subfield data in
    # order, with no discrimination between which list items are codes and
    # which are data, but codes should be at even-numbered positions
    # in the list and the corresponding data in the next, odd-numbered
    # position.
    for n, item in enumerate(field.subfields):
        if item == sub_code and n % 2 == 0:
            append_punct(field, n+1, end_str, exempt, abbrev_exempt)


def precede_sub(field, sub_code, end_str, exempt=[], abbrev_exempt=False):
    """Add punctuation to the end of the preceding subfield"""
    # Iterate through all the subfields in the field. See the note
    # on the .subfields method under the append_to_each_sub function
    for n, item in enumerate(field.subfields):
        if item == sub_code and n % 2 == 0:
            append_punct(field, n-1, end_str, exempt, abbrev_exempt)
            # If the punctuation was entered at the beginning of the
            # subfield instead of the end of the previous subfield,
            # remove that punctuation
            subfield_data = field.subfields[n+1]
            while subfield_data[0] in end_str or subfield[0] in ' ':
                # Remove first character
                subfield_data = subfield_data[1:]
            # If the data has changed, update the field
            if field.subfields[n+1] != subfield_data:
                field.subfields[n+1] = subfield_data


def add_pre_punct(field, target_sub, pre_punct, exempt=''):
    """Add punctuation to the end of the preceding subfield"""
    # Iterate through all the subfields in each field
    for n, sub in enumerate(field.subfields):
        if sub == target_sub:
            # Check if the subfield before the target sub ends with the
            # desired punctuation
            prev = field.subfields[n-1]
            # To avoid a string indexing error, make sure the subfield
            # data is long enough to be checked for the punctuation
            if len(prev) < len(pre_punct):
                if prev not in pre_punct:
                    field.subfields[n-1] = prev + pre_punct
            # If so, check if it ends in the punctuation or an
            # exemption
        elif not prev.endswith(pre_punct):
            ellipsis = False
            if '...' in exempt:
                exempt = exempt.replace('...', '')
                if prev.endswith('...'):
                    ellipsis = True
            if prev[-1] not in exempt and not ellipsis:
                # If the data ends in part of the required
                # punctuation, remove that part
                while prev != '':
                    if prev[-1] in pre_punct + ' ':
                        prev = prev[:-1]
                    else:
                        break
                field.subfields[n-1] = prev + pre_punct


def add_terminal_period(field, exempt=''):
    """Add a terminal period to the field"""
    # Get the data of the last subfield
    data = field.subfields[last_sub_data_pos(field)]
    ellipsis = False
    if '...' in exempt:
        if data.endswith('...'):
            ellipsis = True
    # If the data does not end in an exemption, add the period
    if len(data) > 0 and data[-1] not in exempt + "." and not ellipsis:
        field.subfields[last_sub_data_pos(field)] = data + "."


def edit_242(record, index, pre_punct):
    """Mirror changes in preceding punctuation made to the 245 in
    every 242
    """
    for field in record:
        if field.tag == '242':
            # Check that the subfield at the index is followed by
            # another subfield
            if len(field.subfields) >= index + 2:
                sub = field.subfields[index]
                next_sub = field.subfields[index+2]
                if not sub.endswith(prepunct):
                    # Remove partial punctuation from end of sub
                    while sub[-1] in pre_punct:
                        sub = sub[:-1]
                    # Remove any part of the punctuation that was
                    # entered in the next sub
                    while next_sub[0] in pre_punct + ' ':
                        next_sub = next_sub[1:]
                    sub = sub + punctuation
                    field.subfields[index] = sub
                    field.subfields[index+2] = next_sub


def enclose_subs(field, subcodes, start_punct, separate_punct, end_punct):
    """Add punctuation enclosing the data in a subfield, and
    punctuation separating multiple instances of the same subfield
    """
    sub_count = 0
    # Count the number of target subfields
    for code in subcodes:
        sub_count = sub_count + field.subfields.count(code)
    # Create a tally variable to determine first, last, middle $q's
    tally = 1
    for n, sub in enumerate(field.subfields):
        if sub in subcodes and tally <= sub_count:
            # Get the subfield data
            # Note that changing the data variable will not change
            # the actual subfield data; to do this, field.subfields
            # must be set to the new value
            data = field.subfields[n+1]
            # Put the beginning punctuation at the start of the 1st
            # subfield
            if tally == 1 and not data.startswith(start_punct):
                # Remove any leading partial punctuation or spaces
                while data[0] in start_punct + ' ':
                    data = data[1:]
                data = start_punct + data
            # Put the separating punctuation the end of each subfield
            # except the last
            if tally < sub_count:
                if not data.endswith(separate_punct):
                    # If the data ends in part of the required
                    # punctuation, remove that part
                    while data[-1] in separate_punct:
                        data = data[:-1]
                    # Add the required punctuation
                    field.subfields[n+1] = data + separate_punct
            # Put the ending punctuation at the end of the last
            # subfield
            if tally == sub_count and not data.endswith(end_punct):
                field.subfields[n+1] = data + end_punct
            # Increase the tally
            tally += tally


def last_sub_data_pos(field):
    """Get the location of the last subfield that is not a control
    subfield
    """
    # Get the last subfield code
    last_subcode_pos = len(field.subfields) - 2
    # Cycle backwards through subfield codes until a non-control
    # subfield is found
    while field.subfields[last_subcode_pos] in control_subs:
        last_subcode_pos = last_subcode_pos - 2
    # Return the location of the data of the last subfield
    return last_subcode_pos + 1


def pre_punct_245b(record, field):
    """Adds preceding punctuation before 245 subfield b when it is
    possible to determine that it begins with a parallel title or
    title of another work contained in the resource
    """
    i = 0
    dict245 = {}
    for n, sub in enumerate(field.subfields):
        subs242 = 'abchnp'
        if sub in 'subs242' or field.subfields[n-1] in subs242:
            dict245[i] = sub
            i += i
        if sub == 'b':
            data = field.subfields[n+1] # Data in subfield b
            prev = field.subfields[n-1] # The previous subfield
            # Before checking for punctuation, check that the
            # subfield is long enough to contain it, in order
            # to avoid index errors
            if len(prev) > 2:
                pre_punct = [' :', ' =', ' ;']
                if (prev[-2:] not in pre_punct \
                        and not prev.endswith('.'):
                    varying_titles = record.get_fields('246')
                    for vt in varying_titles:
                        if vt.indicator2 == '1':
                            parallel = vt['a'].lower()
                            # For the purpose of searching,
                            # remove any punctuation at the end
                            # of the 246$a
                            while (parallel[-1] in punct
                                    or parallel[-1] in ' .'):
                                parallel = parallel[:-1]
                            while data[0] in ' =':
                                data = data[1:]
                            # If any change was made, update the field
                            if data != field.subfields[n+1]:
                                field.subfields[n+1] = data
                            if data.lower().find(parallel) == 0:
                                # Remove any misentered
                                # preceding punctuation
                                while prev[-1] in ' =':
                                    prev = prev[:-1]
                                field.subfields[n-1] = prev + ' ='
                                edit_242(record, i-1, ' =')
                            elif data.lower().find(parallel) > 0:
                                parallel_pos = data.lower().find(parallel)
                    # Look for titles in added entries
                    added_entries = record.get_fields('700', '710', '711')
                    for entry in added_entries:
                        same_author = ''
                        diff_author = ''
                        if entry.tag == '700' and entry.indicator2 == '2':
                            if record['100']:
                                if record['100']['a'] == entry['a']:
                                    same_author = entry['t'].lower()
                            elif saw['t']:
                                diff_author = entry['t'].lower()
                        if entry.tag == '710' and entry.indicator2 == '2':
                            if record['110']:
                                if record['110']['a'] == entry['a']:
                                    same_author = entry['t'].lower()
                            elif saw['t']:
                                diff_author = entry['t'].lower()
                        if entry.tag == '711' and entry.indicator2 == '2':
                            if record['111']:
                                if record['111']['a'] == entry['a']:
                                    same_author = entry['t'].lower()
                            elif saw['t']:
                                diff_author = entry['t'].lower()
                        if same_author:
                            while data[0] in ' ;':
                                data = data[1:]
                            if data != field.subfields[n+1]:
                                field.subfields[n+1] = data
                            while same_author[-1] in punct + '.':
                                same_author = same_author[:-1]
                            if data.lower().find(same_author) == 0:
                                while prev[-1] in ' ;':
                                    prev = prev[:-1]
                                field.subfields[n-1] = prev + ' ;'
                                edit_242(record, i-1, ' ;')
                        if diff_author:
                            while data[0] in ' .':
                                data = data[1:]
                            if field.subfields[n+1] != data:
                                field.subfields[n+1] = data
                            while diff_author[-1] in punct + '.':
                                diff_author = diff_author[:-1]
                            if data.lower().find(diff_author) == 0:
                                while prev[-1] in ' .':
                                    prev = prev[:-1]
                                field.subfields[n-1] = prev + '.'
                                edit_242(record, i-1, '.')
                    uniform_titles = record.get_fields('730')
                    for ut in uniform_titles:
                        ut = ut['a'].lower()
                        while ut[-1] in punct or ut[-1]:
                            ut = ut[:-1]
                        while data[0] == '.':
                            data = data[1:]
                        if field.subfields[n+1] != data:
                            field.subfields[n+1] = data
                        if data.lower().find(ut) == 0:
                            field.subfields[n-1] = prev[n-1] + "."
                            edit_242(record, i-1, '.')
            else:
                print("Short sub: " + field)


def remove_all_punct(field, subfield):
    """Remove all punctuation in a subfield"""
    for n, sub in enumerate(field.subfields):
        if sub == subfield:
            data = field.subfields[n+1]
            data = data.replace('.', '')
            for i in punct:
                data = data.replace(i, '')
            field.subfields[n+1] = data


#  Unsure if the following functuation has any use
# def remove_end_punct(field, target_sub, punctuation, exempt=''):
#     """Remove ending punctuation to every instance of a target
#     subfield
#     """
#     # Iterate through all the subfields in each field
#     for n, subfield in enumerate(field.subfields):
#         if subfield == target_sub:
#             # Check if the subfield data ends with the desired punctuation
#             data = field.subfields[n + 1]
#             i = len(punctuation) * -1
#             # Check the length of the data, to avoid a string indexing error
#             if len(data) < len(punctuation):
#                 if data not in punctuation:
#                     field.subfields[n + 1] = data + punctuation
#             # If the data is longer than the punctuation, check if it ends
#             # with the punctuation
#             elif data[i:] != punctuation:
#                 # If not, check if the data ends in one of the exempt
#                 ellipsis = False
#                 if '...' in exempt:
#                     exempt.replace('...', '')
#                     if len(data) > len('...') and data[-3] == '...':
#                         ellipsis = True
#                 # If the data does not end in an exemption, add the
#                 # prescribed punctuation
#                 if data[-1] not in exempt and not ellipsis:
#                     # If the data ends in part of the required punctuation,
#                     # remove that part
#                     while True:
#                         if data[-1] in punctuation:
#                             data = data[:-1]
#                         else:
#                             break
#                     field.subfields[index + 1] = data + punctuation


def remove_pre_punct(field, exempt=''):
    """Remove punctuation preceding any subfield"""
    for n, sub in enumerate(field.subfields):
        # Check that the subfield is not the last
        if n < len(field.subfields) - 1:
            # Loop until all non-exempt ending punctuation is removed
            while sub != '':
                if sub.endswith('...'):
                    if '...' in exempt:
                        break
                    else:
                        sub = sub[:-3]
                # As periods following abbreviations are always
                # permitted (I think?), do not remove ending periods
                elif sub.endswith('.'):
                    print('Ends with abbreviation?: ' + sub)
                    break
                 # Remove non-exempt punctuation
             elif sub[-1] in punct + ' ' and sub[-1] not in exempt:
                    sub = sub[:-1]
                else:
                    break
            # Update subfield if changes where made
            if sub != field.subfields[n]:
                field.subfields[n] = sub


def remove_terminal_period(field):
    """Remove the terminal period at the end of a field"""
    data = field.subfields[last_sub_data_pos(field)]
    #  TODO: some way to test for abbreviations
    if data.endswith('.'):
        if not data.endswith('...'):
            #  Print to console to check if the use of a
            #  period is appropriate
            print("Erroneous ending period for field?: " + field.__str__())


def remove_terminal_punct(field, exempt=''):
    """Remove punctuation at the end of a field"""
    data = field.subfields[last_sub_data_pos(field)]
    while data != '':
        #  TODO: some way to test for abbreviations
        if data.endswith('...'):
            if '...' in exempt:
                break
            else:
                data = data[:-3]
        # As periods following abbreviations are always
        # permitted (I think?), do not remove ending periods
        elif data.endswith('.'):
            print('Ends with abbreviation?: ' + field.__str__)
            break
        elif data[-1] in punct + ' ' and data[-1] not in exempt:
            # Change the subfield data
            data = data[:-1]
        # End loop when field does not end in prohibited
        # punctuation
        else:
            break
    # Update the field if any characters where removed
    if data != field.subfields[last_sub_data_pos(field)]:
        field.subfields[last_sub_data_pos(field)] = data


def main():
    with open('input_mrc/242.mrc', 'rb') as fh:
        # Open the record and encode as unicode, to prevent errors
        reader = MARCReader(fh, to_unicode=True, force_utf8=True)
        for record in reader:
            for f_index, field in enumerate(record.fields):
                list1 = ['015', '020', '024', '027', '028']
                if field.tag in list1:
                    enclose_subs(field, 'q', '(', ';', ')')
                if field.tag in list1 or field.tag in linking_entry_fields:
                    remove_terminal_punct(field, "-)!?")
                if field.tag == '210' or field.tag == '222':
                    enclose_subs(field, 'b', '(', '', ')')
                list2 = ['100', '600', '700', '800']
                if field.tag in list2:
                    add_terminal_period(field)
                list3 = ['210', '222', '251', '270', '340', '341', '342',
                         '355', '357', '363', '365', '366', '377', '380',
                         '381', '382', '384', '385', '386', '388', '938',
                         '956', '987']
                if field.tag in list3:
                    remove_pre_punct(field, "!-?]}>)")
                    remove_terminal_period(field)
                if field.tag == '242':
                    remove_all_punct(field, 'y')
                    control_subs.append('y')
                    add_terminal_period(field)
                    control_subs.remove('y')
                if field.tag == '242' or field.tag == '245':
                    add_pre_punct(field, 'c', ' /')
                    add_pre_punct(field, 'n', '.', '...!-?')
                    # Enumerate subfields to determine if any $p
                    # follows a $n
                    for n, sub in enumerate(field.subfields):
                        if sub == 'p':
                            prev = field.subfields[n-1]
                            while prev.endswith(' '):
                                prev = prev[:-1]
                            # If the previous subfield is n, make sure
                            # it ends in a comma
                            if field.subfields[n-2] == 'n':
                                if not prev.endswith(','):
                                    prev = prev + ','
                            # Otherwise, make sure the previous
                            # subfield ends in an ellipsis,
                            # exclamation, hyphen, question mark, or
                            # period
                            elif prev[-1] not in '.!-?':
                                # If not, add period
                                prev = prev + '.'
                            # Update the subfield if it has been changed
                            if field.subfields[n-1] != prev:
                                field.subfields[n-1] = prev
                if field.tag == '245':
                    add_pre_punct(field, 'f', ',')
                    enclose_subs(field, 'g', '(', '', ')')
                    if field['a']:
                        add_pre_punct(field, 'k', ' :')
                    # subfield p following a subfield n vs. not
                    add_pre_punct(field, 's', '.', '...!-?')
                    pre_punct_245b(record, field)
                list4 = ['245', '250', '254', '255', '256', '343', '351',
                         '352']
                if field.tag in list4:
                    add_terminal_period(field)
                if field.tag == '246':
                    remove_terminal_punct(field)
                if field.tag == '300':
                    add_pre_punct(field, 'b', ' :')
                if field.tag in linking_entry_fields:
                    remove_terminal_punct(field, "-)!?")
            # Write the edited record to a new file
            with open('output_mrc/242.mrc', 'ab') as out:
                out.write(record.as_marc())

if __name__ == '__main__':
    main()
