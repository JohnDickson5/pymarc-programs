from pymarc import MARCReader

# The ASCII and ANSEL punctuation marks, plus the Euro sign
any_punct = ['!', '"', '#', '$', '%', '&', '\'', '(', ')', '*', '+', ',', '-',
             '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^',
             '_', '`', '{', '|', '}', '~', 'ʹ', '·', '♭', '®', '±', 'ʺ', '£',
             '°', '℗', '©', '♯', '¿', '¡' '€']

control_subs = ['u', 'w', 'x', 'z', '0', '1', '2', '3', '4', '5', '6', '7',
                '8', '9']

linking_entry_fields = ['760', '762', '765', '767', '770', '772', '773',
                        '774', '775', '776', '777', '780', '785', '786',
                        '787']


with open('output_mrc/abbrev_list.txt', 'r') as f:
    abbrev_list = f.read().split('\n')

# abbrev_list.remove('')

with open('output_mrc/not_abbrev_list.txt', 'r') as f:
    not_abbrev_list = f.read().split('\n')

# not_abbrev_list.remove('')


def append_punct(field, sub_pos, end_str, exempt=[], abbrev_exempt=False):
    """Add a string to the end of a subfield if it does not already
    end in that string or an exemption. For the 'exempt' list, include
    only strings that are always exempt for receiving the endi ng (that
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
                field.subfields[sub_pos] = ''.join([sub, end_str])

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


def add_terminal_punct(
        field, end_punct='.', exempt_subs=[], exempt_punct=[],
        abbrev_exempt=True):
    """Add punctuation to the last subfield in a field, excluding any
    control subfields
    """
    # Get the last subfield code, compensating for the subfields list
    # starting at index 0 and the final subfield's code and data being
    # indexed separately
    last_subcode_pos = len(field.subfields) - 2
    # Cycle backwards through subfield codes until subfield which is
    # neither a control subfield nor exempt is found
    while (field.subfields[last_subcode_pos] in control_subs
            or field.subfields[last_subcode_pos] in exempt_subs):
        last_subcode_pos = last_subcode_pos - 2
    # Return the location of the data of the last subfield
    last_subdata_pos = last_subcode_pos + 1
    # Check that the last_subcode_pos appears to be occupied by a code
    if (len(field.subfields[last_subcode_pos]) == 1
            and last_subcode_pos % 2 == 0):
        append_punct(field, last_subdata_pos, end_punct, exempt_punct,
                     abbrev_exempt)


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
                field.subfields[n+1] = ''.join((start_punct, data))
            # Put the separating punctuation the end of each subfield
            # except the last
            if tally < sub_count:
                append_punct(field, n+1, separate_punct)
            # Put the ending punctuation at the end of the last
            # subfield
            # TODO: add possibility of placing ending punctuation
            # before preceding punctuation of next subfield (big
            # problem with 020$q followed by 020$c)
            if tally == sub_count:
                append_punct(field, n+1, end_punct)
            # Increase the tally
            tally += tally


def last_subcode_index(field):
    # Get the last subfield code, compensating for the subfields list
    # starting at index 0 and the final subfield's code and data being
    # indexed separately
    last_subcode_pos = len(field.subfields) - 2
    # Cycle backwards through subfield codes until subfield which is
    # neither a control subfield nor exempt is found
    while (field.subfields[last_subcode_pos] in control_subs
            or field.subfields[last_subcode_pos] in exempt_subs):
        last_subcode_pos = last_subcode_pos - 2
    return last_subcode_pos


def last_subdata_index(field):
    # Return the location of the data of the last subfield
    return last_subcode_index(field) + 1


def remove_all_punct(field, subfield):
    """Remove all punctuation in a subfield"""
    for n, sub in enumerate(field.subfields):
        if sub == subfield:
            data = field.subfields[n+1]
            data = data.replace('.', '')
            for i in any_punct:
                data = data.replace(i, '')
            field.subfields[n+1] = data


def prepend_punct(field, sub_pos, pre_str):
    """Add a string to the beginning of a subfield if it does not already
    begin with that string.
    """
    # Get the subfield data
    sub = field.subfields[sub_pos]
    # Check that the subfield does not already end in the string
    if not sub.startswith(pre_str):
        while sub != '':
            if sub[0] in pre_str or sub[0] == ' ':
                sub = sub[1:]
            else:
                break
        # Edit the subfield
        field.subfields[sub_pos] = ''.join([pre_str, sub])


def del_from_end(
        field, sub_pos, del_list=any_punct, exempt=[], abbrev_exempt=False):
    """Remove a string from the end of a subfield"""
    # Get the subfield data
    sub = field.subfields[sub_pos]
    # Append a single space to the deleted list so that any trailing
    # spaces caused by deletions
    if field.tag not in ['010', '016']:
        del_list.append(' ')
    # Initiate a count as a failsafe for infinite looping
    count = 0
    # Remove the ending until it is not in the list of ends to be
    # deleted or it is in the list of exemptions
    while (sub.endswith(tuple(del_list))
            and not sub.endswith(tuple(exempt))):
        if abbrev_exempt:
            if sub.endswith(tuple(abbrev_list)):
                break
            elif sub.endwith(tuple(not_abbrev_list)):
                sub = sub[:-1]
        if count == 100:
            print("Loop trouble")
            break
        for i in del_list:
            if sub.endswith(i):
                end = ''
                for index, char in enumerate(reversed(sub)):
                    if index > 0:
                        if char == ' ' or char in any_punct:
                            end = sub[-index-1:]
                            break
                if end == '':
                    end = sub
                count += 1
                # Warn if the field ends in a period; as periods
                # ending abbreviations are sometimes treated
                # differently from other periods, it is not safe to
                # take action based on an ending period.
                if i == '.' and abbrev_exempt:
                    if end not in abbrev_list:
                        ans = ''
                        while ans != 'y' and ans != 'n':
                            print(sub)
                            ans = input("""Does this subfield end in an"""
                                         + """ abbreviation (y/n): """)
                            ans = ans.strip().lower()
                        if ans == 'y':
                            abbrev_list.append(end)
                            with open('output_mrc/abbrev_list.txt', 'a') as out:
                                try:
                                    out.write(end + '\n')
                                except UnicodeEncodeError as e:
                                    pass
                            break
                        else:
                            not_abbrev_list.append(end)
                            with open('output_mrc/not_abbrev_list.txt', 'a') as out:
                                try:
                                    out.write(end + '\n')
                                except UnicodeEncodeError as e:
                                    pass
                            sub = sub[:-len(i)]
                    else:
                        break
                else:
                    sub = sub[:-len(i)]
    # Save any changes made
    if field.subfields[sub_pos] != sub:
        # if field.tag in ['017', '018', '020']:
        #     with open('output_mrc/' + field.tag + 'c.txt', 'a') as out:
        #         try:
        #             out.write('\n'.join([field.__str__(), sub]))
        #         except UnicodeEncodeError as e:
        #             pass
        field.subfields[sub_pos] = sub
    # else:
    #     if field.tag  in ['017', '018', '020']:
    #         with open('output_mrc/' + field.tag + 'u.txt', 'a') as out:
    #             try:
    #                 out.write(field.__str__())
    #                 out.write('\n')
    #             except UnicodeEncodeError as e:
    #                 pass


def del_from_start(
        field, sub_pos, del_list=any_punct, exempt=[]):
    """Remove a string from the beginning of a subfield"""
    # Get the subfield data
    sub = field.subfields[sub_pos]
    # Append a single space to the deleted list so that any leading
    # spaces caused by deletions
    if field.tag != '010':
        del_list.append(' ')
    # Initiate a count as a failsafe for infinite looping
    count = 0
    # Remove the ending until it is not in the list of ends to be
    # deleted or it is in the list of exemptions
    while sub.startswith(tuple(del_list)):
        if count == 100:
            print("Loop trouble")
            break
        for i in del_list:
            if sub.startswith(i):
                count += 1
                sub = sub[len(i):]
    # Save any changes made
    if field.subfields[sub_pos] != sub:
        field.subfields[sub_pos] = sub


def del_pre_punct(
        field, del_list=any_punct, exempt=[], abbrev_exempt=False):
    """Omit punctuation preceding each subfield in a field"""
    for n, sub in enumerate(field.subfields):
        # Compensate for the separate storage of codes and data in the
        # subfields method, and the start of indexing with 0
        if n % 2 != 0 and n < len(field.subfields) - 1:
            del_from_end(field, n, del_list, exempt, abbrev_exempt)


def del_terminal_punct(field, punct=any_punct, exempt=[], abbrev_exempt=True):
    """Remove target punctuation from the end of a field"""
    # Compensate for indexing beginning with 0
    last_subdata_pos = len(field.subfields) - 1
    del_from_end(field, last_subdata_pos, punct, exempt, abbrev_exempt)


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
