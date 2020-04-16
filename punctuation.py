from pymarc import MARCReader

# Leader - the first field in a MARC record
# Variable fields - all other fields
# variable control fields - 00X fields
# variable data fields - all other fields
# tag
# indicator positiions
# subfield codes
# data elements

# The ASCII and ANSEL punctuation marks, without a period and with €
punct = "!\"#$%&'()*+,-/:;<=>?@[\\]^_`{|}~ʹ·♭®±ʺ£°℗©♯¿€"

control_subs = ['u', 'w', 'x', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8',
                '9']

linking_entry_fields = ['760', '762', '765', '767', '770', '772', '773', '774',
                        '775','776','777','780','785','786','787']


def last_sub_data_pos(field):
    '''Get the location of the last subfield that is not a control subfield'''
    # Get the last subfield code
    last_subcode_pos = len(field.subfields) - 2
    # Cycle backwards through subfield codes until a non-control subfield is
    # found
    while True:
        if field.subfields[last_subcode_pos] in control_subs:
            last_subcode_pos = last_subcode_pos - 2
        else:
            break
    # Return the location of the data of the last subfield
    return last_subcode_pos + 1


def add_end_punct(field, sub, punctuation, exemptions=''):
    '''Add ending punctuation to every instance of a target subfield'''
    # Iterate through all the subfields in each field
    for index, subfield in enumerate(field.subfields):
        if subfield == sub:
            # Check if the subfied data ends with the desired punctuation
            data = field.subfields[index + 1]
            i = len(punctuation) * -1
            # Check the length of the data, to avoid a string indexing error
            if len(data) < len(punctuation):
                if data not in punctuation:
                    field.subfields[index + 1] = data + punctuation
            # If the data is longer than the punctuation, check if it ends
            # with the punctuation
            elif data[i] != punctuation:
                # If not, check if the data ends in one of the exemptions
                if '...' in exemptions:
                    exemptions.replace('...', '')
                    if len(data) > len('...') and data[-3] == '...':
                        ellipsis = True
                # If the data does not end in an exemption, add the
                # prescribed punctuation
                if data[-1] not in exemptions and ellipsis != True:
                    # If the data ends in part of the required punctuation,
                    # remove that part
                    while True:
                        if data[-1] in punctuation:
                            data = data[:-1]
                        else:
                            break
                    field.subfields[index + 1] = data + punctuation


def add_terminal_period(field, exemptions=''):
    '''Add a terminal period to the field'''
    # Get the last subfield data
    data = field.subfields[last_sub_data_pos(field)]
    if '...' in exemptions:
        if data[-3] == '...':
            ellipsis = True
        exemptions = exemptions.replace('...', '')
    # If the data does not end in an exemption, add the period
    if len(data) > 0 and data[-1] not in punct + "." and ellipsis != True:
        field.subfields[last_sub_data_pos] = data + "."


def add_pre_punct(field, target_sub, pre_punct, exemptions=''):
    '''Add punctuation to the end of the preceding subfield'''
    # Iterate through all the subfields in each field
    for s_index, sub in enumerate(field.subfields):
        if sub == target_sub:
            # Check if the subfied before the target sub ends with the desired
            # punctuation
            prev = field.subfields[s_index - 1]
            i = len(pre_punct) * -1
            # To avoid a string indexing error, make sure the subfield data
            # is long enough to be checked for the punctuation
            if len(prev) < len(pre_punct):
                if prev not in pre_punct:
                    field.subfields[s_index - 1] = prev + pre_punct
            # If so, check if it ends in the punctuation or an exemption
            elif prev[i] != pre_punct:
                if '...' in exemptions:
                    exemptions.replace('...', '', 1)
                    if len(prev) > len('...') and prev[-3] == '...':
                        ellipsis = True
                if prev[-1] not in exemptions and ellipsis != True:
                    # If the data ends in part of the required punctuation,
                    # remove that part
                    for j in range(1, len(pre_punct)):
                        if prev[-1] in pre_punct:
                            prev = prev[:-1]
                        else:
                            break
                    field.subfields[s_index - 1] = prev + pre_punct


def edit_242(record, index, punctuation):
    '''Mirror changes made to the 245 in every 242'''
    for field in record:
        if field.tag == '242':
            i = len(punctuation) * -1
            sub = field.subfields[index]
            next_sub = field.subfields[index+2]
            if len(sub) > len(punctuation) and sub[i] != punctuation:
                # Remove partial punctuation from end of sub
                while sub[-1] in punctuation:
                    sub = sub[:-1]
                # Remove any part of the punctuation that was entered in the
                # next sub
                while next_sub[0] in punctuation:
                    next_sub = next_sub[1:]
                sub = sub + punctuation
                field.subfields[index] = sub
                field.subfields[index+2] = next_sub


def enclose_subs(field, subcodes, start_punct, separate_punct, end_punct):
    '''Add punctuation enclosing the data in a subfield, and punctuation
    separating multiple instances of the same subfield'''
    subscount = 0
    # Count the number of target subfields
    for code in subcodes:
        subscount = subscount + field.subfields.count(code)
    # Create a tally variable to determine first, last, middle $q's
    tally = 1
    for s_index, sub in enumerate(field.subfields):
        if sub in subcodes and tally <= subscount:
            # Get the subfield data
            # Not that changing the data variable will not change
            # the actual subfield data; to do this, field.subfields
            # must be set to the new value
            data = field.subfields[s_index + 1]
            # Put the beginning punctuation at the start of the 1st subfield
            if tally == 1 and data[0] != start_punct:
                data = start_punct + data
            # Put the separating punctuation the end of each subfield except the
            # last
            i = len(separate_punct) * -1
            if tally < subscount:
                if data[i:] != separate_punct:
                    # If the data ends in part of the required punctuation,
                    # remove that part
                    for j in range(1, len(separate_punct)):
                        if data[-1] in separate_punct:
                            data = data[:-1]
                        else:
                            break
                    # Add the required punctuation
                    field.subfields[s_index + 1] = data + separate_punct
            # Put the ending punctuation at the end of the last subfield
            if tally == subscount and data[-1] != end_punct:
                field.subfields[s_index + 1] = data + end_punct
            # Increase the tally
            tally += tally


def pre_punct_245b(record, field):
    '''Adds preceding punctuation before 245 subfield b when the a'''
    i = 1
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
                if prev[-2:] not in pre_punct \
                and prev[-1] != '.':
                    varying_titles = record.get_fields('246')
                    for vt in varying_titles:
                        if vt.indicator2 == '1':
                            parallel = vt['a'].lower()
                            # For the purpose of searching,
                            # remove any punctuation at the end
                            # of the 246$a
                            while parallel[-1] in punct \
                            or parallel[-1] in ' .':
                                parallel = parallel[:-1]
                            while data[0] in ' =':
                                data = data[1:]
                            field.subfields[n+1] = data
                            if data.find(parallel) == 0:
                                # Remove any misentered
                                # preceding punctuation
                                while prev[-1] in ' =':
                                    prev = prev[:-1]
                                field.subfields[n-1] \
                                = prev + ' ='
                                edit_242(record, i-1, ' =')
                            elif data.find(parallel) > 0:
                                parallel_pos \
                                = data.find(parallel)
                    # Look for titles in added entries
                    added_entries = record.get_fields(
                        '700', '710', '711')
                    for entry in added_entries:
                        same_author = ''
                        diff_author = ''
                        if entry.tag == '700' \
                        and entry.indicator2 = '2':
                            if record['100']:
                                if record['100']['a'] \
                                == entry['a']:
                                    same_author \
                                    = entry['t'].lower()
                            elif saw['t']:
                                diff_author \
                                = entry['t'].lower()
                        if entry.tag == '710' \
                        and entry.indicator2 = '2':
                            if record['110']:
                                if record['110']['a'] \
                                == entry['a']:
                                    same_author \
                                    = entry['t'].lower()
                            elif saw['t']:
                                diff_author \
                                = entry['t'].lower()
                        if entry.tag == '711' \
                        and entry.indicator2 = '2':
                            if record['111']:
                                if record['111']['a'] \
                                == entry['a']:
                                    same_author \
                                    = entry['t'].lower()
                            elif saw['t']:
                                diff_author \
                                = entry['t'].lower()
                        if same_author:
                            while field.subfields[n+1][0] in ' ;':
                                field.subfields[n+1] \
                                = field.subfields[n+1][1:]
                            data = field.subfields[n+1].lower()
                            while same_author[-1] in punct + '.':
                                same_author = same_author[:-1]
                            if data.find(same_author) == 0:
                                while field.subfields[n-1][-1] in ' ;':
                                    field.subfields[n-1] \
                                    = field.subfields[n-1][:-1]
                                field.subfields[n-1] \
                                = field.subfields[n-1] + ' ;'
                                edit_242(record, i-1, ' ;')
                        if diff_author:
                            while field.subfields[n+1][0] in ' .':
                                field.subfields[n+1] \
                                = field.subfields[n+1][1:]
                            data = field.subfields[n+1].lower()
                            while diff_author[-1] in punct + '.':
                                diff_author = diff_author[:-1]
                            if data.find(diff_author) == 0:
                                field.subfields[n-1] \
                                = field.subfields[n-1]
                                + '.'
                                edit_242(record, i-1, '.')
                    uniform_titles = record.get_fields('730')
                    for ut in uniform_titles:
                        ut = ut['a'].lower()
                        while ut[-1] in punct or ut[-1]:
                            ut = ut[:-1]
                        while field.subfields[n+1][0] == '.':
                            field.subfields[n+1] \
                            = field.subfields[n+1][1:]
                        if data.find(ut) == 0:
                            field.subfields[n-1] \
                            = field.subfields[n-1] + "."
                            edit_242(record, i-1, '.')
            else:
                print("Short sub: " + field)


def remove_terminal_period(field):
    '''Remove the terminal period at the end of a field'''
    data = field.subfields[last_sub_data_pos(field)]
    #  TODO: some way to test for abbreviations
    if data[-1] == ".":
        if data[-3:] != "...":
            #  Print to console to check if the use of a
            #  period is appropriate
            print("Erroneous ending period for field?: " + field)


def remove_all_punct(field, subfield):
    '''Remove all punctuation in a subfield'''
    for n, sub in field.subfields:
        if sub == subfield:
            data = field.subfields[n+1]
            data = data.replace('.', '')
            for i in punct:
                data = data.replace(i, '')
            field.subfields[n+1] = data


def remove_end_punct(field, exemptions=''):
    '''Remove punctuation at the end of a field'''
    # Get last subfield indicator that is not a control subfield
    last_subcode_pos = len(field.subfields) - 2
    while last_subcode_pos > 1:
        if field.subfields[last_subcode_pos] in control_subs:
            last_subcode_pos = last_subcode_pos - 2
        else:
            break
    last_sub_data_pos = last_subcode_pos + 1
    data = field.subfields[last_sub_data_pos]
    while data != "":
        #  TODO: some way to test for abbreviations
        if data[-1] == ".":
            if data[-3:] != "...":
                #  Print to console to check if the use of a
                # period is appropriate
                print("Erroneous ending period for subfield?: " + data)
            break
        elif data[-1] in punct and data[-1] not in exemptions:
            # Change the subfield data
            field.subfields[last_sub_data_pos] = data[:-1]
            # Refresh the subfield variable for the loop
            data = field.subfields[last_sub_data_pos]
        # End loop when field does not end in prohibited
        # punctuation
        else:
            break


def remove_pre_punct(field, exemptions):
    '''Remove punctuation preceding any subfield'''
    for s_index, sub in enumerate(field.subfields):
        while sub != "":
            if sub[-1] == ".":
                if sub[-3:] != "...":
                    # Print to console to check if the use of a
                    # period is appropriate
                    print("Erroneous ending period for subfield?:" + data)
                break
            elif sub[-1] in punct and data[-1] not in exemptions:
                # Change the subfield data
                field.subfields[s_index] = data[:-1]
                # Refresh the subfield variable for the loop
                data = field.subfields[s_index]
            # End loop when field does not end in prohibited
            # punctuation
            else:
                break


def main():
    with open('hollis_marc/hollis.mrc', 'rb') as fh:
        # Open the record and encode as unicode, to prevent errors
        reader = MARCReader(fh, to_unicode=True, force_utf8=True)
        for record in reader:
            for f_index, field in enumerate(record.fields):
                list1 = ['015', '020', '024', '027', '028']
                if field.tag in list1:
                    enclose_subs(field, 'q', '(', ';', ')')
                if field.tag in list1 or field.tag in linking_entry_fields:
                    remove_end_punct(field, "-)!?")
                if field.tag == '210' or field.tag == '222':
                    enclose_subs(field, 'b', '(', '', ')')
                list2 = ['100', '600', '700', '800']
                if field.tag in list2:
                    add_terminal_period(field)
                list3 = ['210', '222', '251', '270', '340', '341', '342', '355',
                        '357', '363', '365', '366', '377', '380', '381', '382',
                        '384', '385', '386', '388', '938', '956', '987']
                if field.tag in list3:
                    remove_pre_punct(field, "!-?]}>)")
                    remove_terminal_period(field)
                if field.tag == '242':
                    remove_all_punct(field, 'y')
                    control_subs = control_subs.append('y')
                    add_terminal_period(field)
                    control_subs = control_subs.remove('y')
                if field.tag == '242' or field.tag == '245':
                    add_pre_punct(field, 'c', ' /')
                    add_pre_punct(field, 'n', '.', '...!-?')
                    # Enumerate subfields to determine if any $p follows a $n
                    for n, sub in enumerate(field.subfields):
                        if sub == 'p':
                            prev = field.subfields[n-1]
                            # If the previous subfield is n, make sure it ends
                            # in a comma
                            if field.subfields[n-2] == 'n':
                                if prev[-1] != ',':
                                    while prev[-1] in ' ,':
                                        prev = prev[:-1]
                                    prev = prev + ','
                            # Otherwise, make sure the previous subfield ends
                            # in an ellipsis, exclamation, hyphen, question
                            # mark, or period
                            else:
                                while prev[-1] = ' ':
                                    prev = prev[:-1]
                                if prev[-3] != '...' and prev[-1] != '.':
                                    # If not, add period
                                    if prev[-1] not in '!-?':
                                        prev = prev + '.'
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
                list4 = ['245', '250', '254', '255', '256', '343', '351', '352']
                if field.tag in list4:
                    add_terminal_period(field)
                if field.tag == '246':
                    remove_end_punct(field)
                if field.tag == '300':
                    add_pre_punct(field, 'b', ' :')
                if field.tag in linking_entry_fields:
                    remove_end_punct(field, "-)!?")
            # Write the edited record to a new file
            with open('test.mrc', 'ab') as out:
                out.write(record.as_marc())

if __name__ == '__main__':
    main()
