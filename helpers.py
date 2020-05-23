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


# Create lists of terms that have previously been determined to be or
# to not be abbreviations, removing any blank entries
with open('output_mrc/abbrev_list.txt', 'r') as f:
    abbrev_list = f.read().split('\n')
while '' in abbrev_list: abbrev_list.remove('')
with open('output_mrc/not_abbrev_list.txt', 'r') as f:
    not_abbrev_list = f.read().split('\n')
while '' in not_abbrev_list: not_abbrev_list.remove('')


def add_terminal_punct(field, end_punct='.', exempt_subs=[], exempt_punct=[],
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
        end_quote = False
        exempt_ending = False
        for exemption in exempt:
            if sub.endswith(exemption):
                # If the sub ends in a quotation mark, make sure the
                # character is acceptable
                if exemption == '"':
                    end_quote = True
                    sub = sub[:-1]
                else:
                    exempt_ending = True
                    break
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
                if end_quote:
                    field.subfields[sub_pos] = ''.join([sub, end_str, '"'])
                else:
                    field.subfields[sub_pos] = ''.join([sub, end_str])


def current_sub(field, sub_pos):
    """Returns the subcode of subfield data"""
    if sub_pos % 2 == 0 or 0 > sub_pos =< last_subdata_index(f):
        return None
    sub_code = f.subfields[sub_pos-1]
    if len(sub_code) != 1:
        return None
    return sub_code


def del_from_end(field, sub_pos=None, del_list=any_punct, exempt=[],
                 abbrev_exempt=False):
    """Remove a string from the end of a subfield"""
    # If a subfield position was not provided, edit the final subfield
    if sub_pos == None:
        sub_pos = last_subdata_index(field)
    # Get the subfield data
    sub = field.subfields[sub_pos]
    # Initiate a count as a failsafe for infinite looping
    count = 0
    # Remove the ending until it is not in the list of ends to be
    # deleted or it is in the list of exemptions
    while (sub.endswith(tuple(del_list))
            and not sub.endswith(tuple(exempt))):
        if abbrev_exempt:
            if sub.endswith(tuple(abbrev_list)):
                break
            elif sub.endswith(tuple(not_abbrev_list)):
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
        field.subfields[sub_pos] = sub


def del_from_start(field, sub_pos, del_list=any_punct, exempt=[]):
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


def del_pre_punct(field, subfields=[], del_list=any_punct, exempt=[],
                  abbrev_exempt=False):
    """Omit punctuation preceding each subfield in a field"""
    if subfields:
        for n, sub in enumerate(field.subfields):
            # If a subfield is in the subfields list, remove the
            # preceding punctuation
            if sub in subfields and n % 2 == 0:
                del_from_end(field, n-1, del_list, exempt, abbrev_exempt)
    else:
        for n, sub in enumerate(field.subfields):
            # Compensate for the separate storage of codes and data in the
            # subfields method, and the start of indexing with 0
            if n % 2 != 0 and n < len(field.subfields) - 1:
                del_from_end(field, n, del_list, exempt, abbrev_exempt)


def del_terminal_punct(field, punct=any_punct, exempt=[], abbrev_exempt=True):
    """Remove target punctuation from the end of a field"""
    # Compensate for indexing beginning with 0
    last_subdata_pos = last_subdata_index(field)
    del_from_end(field, last_subdata_pos, punct, exempt, abbrev_exempt)


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


def last_subcode(field):
    # Return the subfield code of the last subfield
    return field.subfields[last_subcode_index(field)]


def last_subcode_index(field, ignore_control_subs=True):
    # Costruct a list of control subfields based on the field tag
    control_subs = []
    if ignore_control_subs == True:
        if field.tag in ['031', '370', '381', '505', '506', '510', '514',
                         '520', '530', '538', '540', '542', '545', '552',
                         '555', '561', '563', '852', '856', '880', '883',
                         '884', '901', '902', '903', '904', '905', '906',
                         '907', '945', '946', '947', '948', '949', '956']:
            control_subs.append('u')
        if field.tag in ['760', '762', '765', '767', '770', '772', '773',
                         '774', '775', '776', '777', '780', '785', '786',
                         '787', '800', '810', '811', '830', '880', '885',
                         '896', '897', '898', '899', '901', '902', '903',
                         '904', '905', '906', '907', '945', '946', '947',
                         '948', '949']:
            control_subs.append('w')
        if field.tag in ['534', '700', '710', '711', '730', '760', '762',
                         '765', '767', '770', '772', '773', '774', '775',
                         '776', '777', '780', '785', '786', '787', '790',
                         '791', '792', '793', '796', '797', '798', '799',
                         '800', '810', '811', '830', '880', '896', '897',
                         '898', '899', '901', '902', '903', '904', '905',
                         '906', '907', '945', '946', '947', '948', '949']:
            control_subs.append('x')
        if field.tag in ['534', '556', '581', '765', '767', '770', '772',
                         '773', '774', '775', '776', '777', '780', '785',
                         '786', '787', '880', '901', '902', '903', '904',
                         '905', '906', '907', '945', '946', '947', '948',
                         '949']:
            control_subs.append('z')
        if field.tag in ['033', '034', '043', '050', '052', '055', '060',
                         '070', '080', '084', '085', '086', '100', '110',
                         '111', '130', '240', '251', '257', '336', '337',
                         '338', '340', '344', '345', '346', '347', '348',
                         '370', '377', '380', '381', '382', '385', '386',
                         '388', '518', '567', '600', '610', '611', '630',
                         '647', '648', '650', '651', '654', '655', '656',
                         '657', '662', '700', '710', '711', '730', '751',
                         '752', '753', '754', '758', '790', '791', '792',
                         '793', '796', '797', '798', '799', '800', '810',
                         '811', '830', '880', '883', '885', '896', '897',
                         '898', '899', '901', '902', '903', '904', '905',
                         '906', '907', '945', '946', '947', '948', '949']:
            control_subs.append('0')
        if field.tag in ['033', '034', '043', '050', '052', '055', '060',
                         '070', '080', '084', '085', '086', '100', '110',
                         '111', '130', '240', '251', '257', '336', '337',
                         '338', '340', '344', '345', '346', '347', '348',
                         '370', '377', '380', '381', '382', '385', '386',
                         '388', '518', '567', '600', '610', '611', '630',
                         '647', '648', '650', '651', '654', '655', '656',
                         '657', '662', '690', '691', '696', '697', '698',
                         '699', '700', '710', '711', '730', '751', '752',
                         '753', '754', '758', '790', '791', '792', '793',
                         '796', '797', '798', '799', '800', '810', '811',
                         '830', '880', '883', '885', '896', '897', '898',
                         '899', '901', '902', '903', '904', '905', '906',
                         '907', '945', '946', '947', '948', '949']:
            control_subs.append('1')
        if field.tag in ['015', '017', '022', '024', '026', '031', '033',
                         '034', '041', '043', '044', '046', '047', '048',
                         '052', '055', '072', '080', '082', '083', '084',
                         '086', '100', '110', '111', '130', '210', '240',
                         '251', '257', '336', '337', '338', '340', '341',
                         '342', '344', '345', '346', '347', '365', '366',
                         '370', '377', '380', '381', '382', '383', '385',
                         '386', '388', '506', '518', '520', '524', '540',
                         '583', '600', '610', '611', '630', '647', '648',
                         '650', '651', '654', '655', '656', '657', '658',
                         '662', '690', '691', '695', '696', '697', '698',
                         '699', '700', '710', '711', '730', '751', '752',
                         '754', '758', '790', '791', '792', '793', '796',
                         '797', '798', '799', '800', '810', '811', '830',
                         '852', '856', '880', '885', '887', '891', '896',
                         '897', '898', '899', '901', '902', '903', '904',
                         '905', '906', '907', '945', '946', '947', '948',
                         '949']:
            control_subs.append('2')
        if field.tag in ['033', '034', '037', '050', '250', '251', '260',
                         '264', '300', '336', '337', '338', '340', '341',
                         '344', '345', '346', '347', '351', '377', '380',
                         '381', '383', '384', '385', '386', '388', '490',
                         '500', '506', '510', '518', '520', '521', '524',
                         '530', '533', '534', '535', '538', '540', '541',
                         '542', '544', '546', '555', '561', '562', '563',
                         '565', '581', '583', '584', '585', '586', '590',
                         '600', '610', '611', '630', '647', '648', '650',
                         '651', '654', '655', '656', '657', '690', '691',
                         '696', '697', '698', '699', '700', '710', '711',
                         '730', '751', '758', '773', '790', '791', '792',
                         '793', '796', '797', '798', '799', '800', '810',
                         '811', '830', '851', '852', '856', '880', '891',
                         '896', '897', '898', '899', '901', '902', '903',
                         '904', '905', '906', '907', '945', '946', '947',
                         '948', '949']:
            control_subs.append('3')
        if field.tag in ['100', '110', '111', '270', '386', '600', '610',
                         '611', '630', '650', '651', '654', '662', '696',
                         '697', '698', '699', '700', '710', '711', '720',
                         '730', '751', '758', '760', '762', '765', '767',
                         '770', '772', '773', '774', '775', '776', '777',
                         '780', '785', '786', '787', '790', '791', '792',
                         '796', '797', '798', '800', '810', '811', '880',
                         '896', '897', '898', '901', '902', '903', '904',
                         '905', '906', '907', '945', '946', '947', '948',
                         '949']:
            control_subs.append('4')
        if field.tag in ['026', '037', '246', '500', '501', '506', '526',
                         '533', '538', '540', '541', '561', '562', '563',
                         '583', '584', '585', '588', '655', '700', '710',
                         '711', '730', '740', '758', '790', '791', '792',
                         '793', '796', '797', '798', '799', '800', '810',
                         '811', '830', '880', '885', '896', '897', '898',
                         '899', '901', '902', '903', '904', '905', '906',
                         '907', '945', '946', '947', '948', '949']:
            control_subs.append('5')
        if field.tag in ['013', '015', '017', '018', '020', '022', '024',
                         '026', '027', '028', '030', '031', '032', '033',
                         '034', '035', '036', '037', '040', '041', '043',
                         '044', '045', '046', '050', '052', '055', '072',
                         '080', '082', '083', '084', '085', '086', '088',
                         '100', '110', '111', '130', '210', '222', '240',
                         '242', '243', '245', '246', '247', '250', '251',
                         '254', '255', '256', '257', '258', '260', '263',
                         '264', '270', '300', '306', '307', '310', '321',
                         '336', '337', '338', '340', '341', '342', '343',
                         '344', '345', '346', '347', '348', '351', '352',
                         '355', '357', '362', '363', '365', '366', '370',
                         '377', '380', '381', '382', '383', '384', '385',
                         '386', '388', '490', '500', '501', '502', '504',
                         '505', '506', '507', '508', '510', '511', '513',
                         '514', '515', '516', '518', '520', '521', '522',
                         '524', '525', '526', '530', '532', '533', '534',
                         '535', '536', '538', '540', '541', '542', '544',
                         '545', '546', '547', '550', '552', '555', '556',
                         '561', '562', '563', '565', '567', '580', '581',
                         '583', '584', '585', '586', '588', '590', '599',
                         '600', '610', '611', '630', '647', '648', '650',
                         '651', '653', '654', '655', '656', '657', '658',
                         '662', '690', '691', '696', '697', '698', '699',
                         '700', '710', '711', '720', '730', '740', '751',
                         '752', '753', '754', '758', '760', '762', '765',
                         '767', '770', '772', '773', '774', '775', '776',
                         '777', '780', '785', '786', '787', '790', '791',
                         '792', '793', '796', '797', '798', '799', '800',
                         '810', '811', '830', '851', '852', '853', '854',
                         '855', '856', '863', '864', '865', '866', '867',
                         '868', '880', '882', '886', '896', '897', '898',
                         '899', '901', '902', '903', '904', '905', '906',
                         '907', '945', '946', '947', '948', '949', '956']:
            control_subs.append('6')
        if field.tag in ['533', '760', '762', '765', '767', '770', '772',
                         '773', '774', '775', '776', '777', '780', '785',
                         '786', '787', '800', '810', '811', '830', '856',
                         '880', '896', '897', '898', '899', '901', '902',
                         '903', '904', '905', '906', '907', '945', '946',
                         '947', '948', '949']:
            control_subs.append('7')
        if field.tag in ['010', '013', '015', '016', '017', '018', '020',
                         '022', '024', '025', '026', '027', '028', '030',
                         '031', '032', '033', '034', '035', '036', '037',
                         '040', '041', '043', '044', '045', '046', '047',
                         '048', '050', '051', '052', '055', '060', '061',
                         '070', '071', '072', '074', '080', '082', '083',
                         '084', '085', '086', '088', '100', '110', '111',
                         '130', '210', '222', '240', '242', '243', '245',
                         '246', '247', '250', '251', '254', '255', '256',
                         '257', '258', '260', '263', '264', '270', '300',
                         '306', '307', '310', '321', '336', '337', '338',
                         '340', '341', '342', '343', '344', '345', '346',
                         '347', '348', '351', '352', '355', '357', '362',
                         '363', '365', '366', '370', '377', '380', '381',
                         '382', '383', '384', '385', '386', '388', '490',
                         '500', '501', '502', '504', '505', '506', '507',
                         '508', '510', '511', '513', '514', '515', '516',
                         '518', '520', '521', '522', '524', '525', '526',
                         '530', '532', '533', '534', '535', '536', '538',
                         '540', '541', '542', '544', '545', '546', '547',
                         '550', '552', '555', '556', '561', '562', '563',
                         '565', '567', '580', '581', '583', '584', '585',
                         '586', '588', '590', '599', '600', '610', '611',
                         '630', '647', '648', '650', '651', '653', '654',
                         '655', '656', '657', '658', '662', '690', '691',
                         '696', '697', '698', '699', '700', '710', '711',
                         '720', '730', '740', '751', '752', '753', '754',
                         '758', '760', '762', '765', '767', '770', '772',
                         '773', '774', '775', '776', '777', '780', '785',
                         '786', '787', '790', '791', '792', '793', '796',
                         '797', '798', '799', '800', '810', '811', '830',
                         '850', '852', '856', '880', '882', '883', '886',
                         '891', '896', '897', '898', '899', '901', '902',
                         '903', '904', '905', '906', '907', '945', '946',
                         '947', '948', '949']:
            control_subs.append('8')
        if field.tag in ['690', '691', '696', '697', '698', '699', '796',
                         '797', '798', '799', '880', '896', '897', '898',
                         '899', '901', '902', '903', '904', '905', '906',
                         '907', '945', '946', '947', '948', '949']:
            control_subs.append('9')
    # Get the index of the last subfield code, compensating for
    # indexing starting at 0 and for codes and data being indexed
    # separately
    # Iterate in reverse through the subfields list, until reaching an
    # item which is neither subfield data or a control subfield code
    for index, code in reversed(list(enumerate(field.subfields))):
        if index % 2 == 0 and code not in control_subs:
            last_subcode_pos = index
            break
    return last_subcode_pos


def last_subdata_index(field):
    # Return the location of the data of the last subfield
    return last_subcode_index(field) + 1


def next_sub(field, sub_pos):
    """Returns the subcode of the next subfield"""
    if sub_pos % 2 == 0 or sub_pos =< last_subdata_index(f) - 2:
        return None
    sub_code = f.subfields[sub_pos+1]
    if len(sub_code) != 1:
        return None
    return sub_code


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


def prev_sub(field, sub_pos):
    """Returns the subcode of the previous subfield"""
    if sub_pos % 2 == 0 or 3 =< sub_pos =< last_subdata_index(f):
        return None
    sub_code = f.subfields[sub_pos-3]
    if len(sub_code) != 1:
        return None
    return sub_code


def remove_punct(field, subfields=[], punct=any_punct):
    """Remove all punctuation in field or subfield"""
    if subfields:
        for n, sub in enumerate(field.subfields):
            # Only edit subfields found in the subfield list
            if sub in subfields and n % 2 == 0:
                data = field.subfields[n+1]
                for i in punct:
                    data = data.replace(i, '')
                field.subfields[n+1] = data
    else:
        for n, sub in enumerate(field.subfields):
            # Edit all subfield data, leaving codes alone
            if n % 2 != 0:
                data = field.subfields[n]
                for i in punct:
                    data = data.replace(i, '')
                field.subfields[n] = data
