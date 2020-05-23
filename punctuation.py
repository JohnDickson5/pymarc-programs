from pymarc import MARCReader
from helpers import *

# The ASCII and ANSEL punctuation marks, plus the Euro sign and a space
any_punct = ['!', '"', '#', '$', '%', '&', '\'', '(', ')', '*', '+', ',', '-',
             '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^',
             '_', '`', '{', '|', '}', '~', 'ʹ', '·', '♭', '®', '±', 'ʺ', '£',
             '°', '℗', '©', '♯', '¿', '¡', '€', ' ']

undefined_fields = [
    '011', '021', '023', '039', '053', '054', '056', '057', '058', '059',
    '062', '063', '064', '065', '067', '068', '069', '073', '075', '076',
    '077', '078', '079', '081', '087', '089', '091', '093', '094', '095',
    '097', '101', '102', '103', '104', '105', '106', '107', '108', '109',
    '112', '113', '114', '115', '116', '117', '118', '119', '120', '121',
    '122', '123', '124', '125', '126', '127', '128', '129', '131', '132',
    '133', '134', '135', '136', '137', '138', '139', '140', '141', '142',
    '143', '144', '145', '146', '147', '148', '149', '150', '151', '152',
    '153', '154', '155', '156', '157', '158', '159', '160', '161', '162',
    '163', '164', '165', '166', '167', '168', '169', '170', '171', '172',
    '173', '174', '175', '176', '177', '178', '179', '180', '181', '182',
    '183', '184', '185', '186', '187', '188', '189', '190', '191', '192',
    '193', '194', '195', '196', '197', '198', '199', '200', '201', '202',
    '203', '204', '205', '206', '207', '208', '209', '211', '212', '213',
    '214', '215', '216', '217', '218', '219', '220', '221', '223', '224',
    '225', '226', '227', '228', '229', '230', '231', '232', '233', '234',
    '235', '236', '237', '238', '239', '241', '244', '248', '249', '252',
    '253', '259', '265', '266', '267', '268', '269', '271', '272', '273',
    '274', '275', '276', '277', '278', '279', '280', '281', '282', '283',
    '284', '285', '286', '287', '288', '289', '290', '291', '292', '293',
    '294', '295', '296', '297', '298', '299', '301', '302', '303', '304',
    '305', '308', '309', '311', '312', '313', '314', '315', '316', '317',
    '318', '319', '320', '322', '323', '324', '325', '326', '327', '328',
    '329', '330', '331', '332', '333', '334', '335', '339', '349', '350',
    '353', '354', '356', '358', '359', '360', '361', '364', '367', '368',
    '369', '371', '372', '373', '374', '375', '376', '378', '379', '387',
    '389', '390', '391', '392', '393', '394', '395', '396', '397', '398',
    '399', '401', '402', '403', '404', '405', '406', '407', '408', '409',
    '412', '413', '414', '415', '416', '417', '418', '419', '420', '421',
    '422', '423', '424', '425', '426', '427', '428', '429', '430', '431',
    '432', '433', '434', '435', '436', '437', '438', '439', '441', '442',
    '443', '444', '445', '446', '447', '448', '449', '450', '451', '452',
    '453', '454', '455', '456', '457', '458', '459', '460', '461', '462',
    '463', '464', '465', '466', '467', '468', '469', '470', '471', '472',
    '473', '474', '475', '476', '477', '478', '479', '480', '481', '482',
    '483', '484', '485', '486', '487', '488', '489', '491', '492', '493',
    '494', '495', '496', '497', '498', '499', '503', '509', '512', '517',
    '519', '523', '527', '528', '529', '531', '537', '543', '548', '549',
    '551', '553', '554', '557', '558', '559', '560', '564', '566', '568',
    '569', '570', '571', '572', '573', '574', '575', '576', '577', '578',
    '579', '582', '587', '589', '601', '602', '603', '604', '605', '606',
    '607', '608', '609', '612', '613', '614', '615', '616', '617', '618',
    '619', '620', '621', '622', '623', '624', '625', '626', '627', '628',
    '629', '631', '632', '633', '634', '635', '636', '637', '638', '639',
    '640', '641', '642', '643', '644', '645', '646', '649', '652', '659',
    '660', '661', '663', '664', '665', '666', '667', '668', '669', '670',
    '671', '672', '673', '674', '675', '676', '677', '678', '679', '680',
    '681', '682', '683', '684', '685', '686', '687', '689', '692', '693',
    '694', '701', '702', '703', '704', '705', '706', '707', '708', '709',
    '712', '713', '714', '715', '716', '717', '718', '719', '721', '722',
    '723', '724', '725', '726', '727', '728', '729', '731', '732', '733',
    '734', '735', '736', '737', '738', '739', '741', '742', '743', '744',
    '745', '746', '747', '748', '749', '750', '755', '756', '757', '759',
    '761', '763', '764', '766', '768', '769', '771', '778', '779', '781',
    '782', '783', '784', '788', '789', '794', '795', '801', '802', '803',
    '804', '805', '806', '807', '808', '809', '812', '813', '814', '815',
    '816', '817', '818', '819', '820', '821', '822', '823', '824', '825',
    '826', '827', '828', '829', '831', '832', '833', '834', '835', '836',
    '837', '838', '839', '840', '846', '847', '848', '849', '857', '858',
    '859', '860', '861', '862', '869', '870', '871', '872', '873', '874',
    '875', '879', '881', '888', '889', '890', '892', '893', '894', '895',
    '908', '909', '912', '913', '914', '915', '916', '917', '918', '919',
    '920', '921', '922', '923', '924', '925', '926', '927', '928', '929',
    '931', '932', '933', '934', '935', '937', '939', '940', '941', '942',
    '943', '944', '950', '951', '952', '953', '954', '955', '957', '958',
    '959', '960', '961', '962', '963', '964', '965', '966', '967', '968',
    '969', '970', '971', '972', '973', '974', '975', '976', '977', '978',
    '979', '984', '985', '986', '988', '989', '991', '992', '993', '995',
    '996', '997', '998', '999'
    ]

# This list keeps track of every field without LC or OCLC punctuation
# instructions
no_instructions = [
    '013', '014', '016', '027', '029', '031', '038', '040', '041', '042',
    '043'
    ]


linking_entry_fields = ['760', '762', '765', '767', '770', '772', '773',
                        '774', '775', '776', '777', '780', '785', '786',
                        '787']


def punctuate(f):
    """Adds the punctuation to a field. Seperated from main() to
    reduce indentation."""
    # Move past control fields, undefined fields, LC/CONSER
    # fields, or fields without punctuation instructions.
    if (f.is_control_field() or f.tag in undefined_fields
            or f.tag in ['012'] or f.tag in no_instructions):
        continue
    # Introductory relationship subfields should end in a
    # colon.
    try:
        if f.subfields[0] == 'i':
            append_punct(f, 1, ':')
    except IndexError:
        print(f)
    # Remove any ending punctuation without removing
    # significant spaces.
    if f.tag in ['010']:
        del_from_end(f, exempt = [' '], abbrev_exempt = False)
    if f.tag in ['015']:
        # Field does not end with a mark of punctuation
        # unless ending in an abbreviation or data ending
        # with a mark of punctuation
        del_from_end(f, exempt = ['...', '-', ')', '!', '?'],
                     abbrev_exempt = True)
        for n, sub in enumerate(f.subfields):
            # Remove parentheses enclosing subfield a
            if sub in ['a', 'z'] and n % 2 == 0:
                del_from_start(f, n+1, del_list = ['('])
                del_from_end(f, n+1, del_list = [')'])
            # Enclose subfields q in parentheses
            if sub == 'q' and n % 2 == 0:
                if n == 0 or f.subfields[n-2] != 'q':
                    prepend_punct(f, n+1, '(')
                if (last_subcode_index(f) == n
                        or f.subfields[n+2] != 'q'):
                    append_punct(f, n+1, ')')
                else:
                    append_punct(f, n+1, ' ;')
    if f.tag in ['017', '018']:
        # Field does not end with a mark of punctuation
        # unless ending in an abbreviation or data ending
        # with a mark of punctuation.
        del_from_end(f, exempt = ['?', '!', '-'],
                     abbrev_exempt = True)
    if f.tag in ['020', '024']:
        # Field does not end with a mark of punctuation
        # unless ending in an abbreviation or data ending
        # with a mark of punctuation.
        del_from_end(f, exempt = ['...', '-', ')', '!', '?'],
                     abbrev_exempt = True)
        for n, sub in enumerate(f.subfields):
            end_punct = ''
            if n % 2 != 0 and current_sub(f, n) == 'q':
                # Begin qualifying data with a parenthesis.
                if n == 1 or prev_sub(f, n) != 'q':
                    prepend_punct(f, n, '(')
                # Separate subfields q with space-
                # semicolon.
                if (n == last_subdata_index(f)
                        or next_sub(f, n) != 'q'):
                    end_punct = ''.join([end_punct, ')'])
                elif next_sub(f, n) == 'q':
                        end_punct = ''.join([end_punct, ' ;'])
            # Precede subfield c with space-colon.
            if (n < last_subdata_index(f)
                    and next_sub(f, n) == 'c'):
                end_punct = ''.join([end_punct, ' :'])
            # Add any necessary ending punctuation.
            if end_punct:
                append_punct(f, n, end_punct)
    if f.tag in ['022']:
        # Field does not end with a period.
        del_from_end(f, del_list = ['.'])
    if f.tag in ['025']:
        #  Field does not end in a mark of punctuation
        del_from_end(f)
        # Field does not include spaces
        remove_punct(f, subfields = ['a'], punct = [' ', '(', ')'])
    if f.tag in ['027', '028']:
        # Field does not end with a mark of punctuation
        # unless ending in an abbreviation or data ending
        # with a mark of punctuation.
        del_from_end(f, exempt = ['...', '-', ')', '!', '?'],
                     abbrev_exempt = True)
        for n, sub in enumerate(f.subfields):
            end_punct = ''
            if n % 2 != 0 and current_sub(f, n) == 'q':
                # Begin qualifying data with a parenthesis.
                if n == 1 or prev_sub(f, n) != 'q':
                    prepend_punct(f, n, '(')
                # Separate subfields q with space-
                # semicolon.
                if (n == last_subdata_index(f)
                        or next_sub(f, n) != 'q'):
                    end_punct = ''.join([end_punct, ')'])
                elif next_sub(f, n) == 'q':
                        end_punct = ''.join([end_punct, ' ;'])
            # Add any necessary ending punctuation.
            if end_punct:
                append_punct(f, n, end_punct)
    # Hyphens and spaces are not carried in the record.
    if f.tag in ['030']:
        remove_punct(f, subfields = ['a'], punct = [' ', '-'])
    # Hyphens are not carried in the MARC record.
    if f.tag in ['032']:
        remove_punct(f, subfields = ['a'], punct = ['-'])
    # Omit decimal point that usually precedes cutter.
    if f.tag in ['033']:
        for n, sub in enumerate(f.subfields):
            if n % 2 == 0 and sub == 'c':
                del_from_start(f, n+1, del_list = ['.'])
    #  Field does not end in a mark of punctuation
    if f.tag in ['034']:
        del_from_end(f)
    # No space occurs between the parenthetical MARC code
    # and the first character position of the control
    # number.
    if f.tag in ['035']:
        for n, sub in enumerate(f.subfields):
            if sub == 'a' and n % 2 == 0:
                data = next_sub(f, n).replace(') ', ')')
                next_sub(f, n) = data
    # Field ends with a mark of punctuation
    if f.tag in ['036']:
        append_punct(f, last_subdata_index(f), '.',
                     exempt = ['-', ')', '!', '?'])
    if f.tag in ['037']:
        # SubFields does not end with a mark of punctuation
        # unless ending in an abbreviation or data ending
        # with a mark of punctuation.
        for n, sub in enumerate(f.subfields):
            if n % 2 != 0:
                del_from_end(f, n, exempt = ['?', '!', '-', ')'],
                             abbrev_exempt = True)
    # Trailing hyphens are carried in the MARC record
    if f.tag in ['043']:
        for n, sub in enumerate(f.subfields):
            if n % 2 == 0 and sub == 'a':
                while len(next_sub(f, n)) < 7:
                    next_sub(f, n) = next_sub(f, n) + '-'
    # For 2-character codes, the trailing blank is omitted.
    if f.tag in ['044']:
        for n, sub in enumerate(f.subfields):
            if n % 2 == 0 and sub in ['a', 'b', 'c']:
                data = next_sub(f, n)
                if len(data) == 3 and data[2] == ' ':
                    next_sub(f, n) = data[:2]
    # Hyphens are the only marks of punctuation used.
    if f.tag in ['045']:
        punct = any_punct
        punct.remove('-')
        remove_punct(f, punct = punct)
    # Dates should not be padded with zeros
    if f.tag in ['046']:
        for n, sub in enumerate(f.subfields):
            if current_sub(f, n) in ['b', 'c', 'd', 'e']:
                while sub[0] == '0':
                    sub = sub[1:]
    if f.tag in ['100']:
        for n, sub in enumerate(f.subfields):
            end_punct = ''
            exempt = ['"']
            # Enclose subfield in parentheses.
            if n % 2 != 0 and current_sub(f, n) in ['q']:
                prepend_punct(f, n, '(')
                end_punct = ''.join([end_punct, ')'])
            # Do not add punctuation to open dates.
            elif current_sub(f, n) in ['d']:
                exempt.append('-')
            if n < last_subdata_index(f) and n % 2 != 0:
                # Precede subfields with comma.
                if next_sub(f, n) in ['d', 'e', 'j']:
                    end_punct = ''.join([end_punct, ','])
                # Precede subfields with period.
                elif next_sub(f, n) in ['f', 'k', 'l', 'n', 't']:
                    end_punct = ''.join([end_punct, '.'])
                # Precede with period unless following a
                # number
                elif next_sub(f, n) in ['p']:
                    if current_sub(f, n) == 'n':
                        end_punct = ''.join([end_punct, ','])
                    else:
                        end_punct = ''.join([end_punct, '.'])
                # Enclose additions to the name of a family
                # in a single set of parentheses,
                # separating each addition by a space-colon.
                elif next_sub(f, n) == 'g':
                    # If the term 'family' is part of
                    # qualifying information, precede it
                    # with a left parenthesis.
                    if current_sub(f, n) == 'a':
                        if 'family' in sub:
                            if '(family' not in sub:
                                sub.replace('family', '(family')
                                f.subfields[n] = sub
                            end_punct = ''.join([end_punct, ' :'])
                    elif current_sub(f, n) == 'g':
                        end_punct = ''.join([end_punct, ' :'])
                # Do not precede with any punctuation
                elif next_sub(f, n) == 'u':
                    for i in end_punct: exempt.append(i)
                    del_from_end(f, n, exempt = exempt,
                                 abbrev_exempt = True)
                # Do not precede subfield with a period if
                # the previous subfield ends in a comma.
                if next_sub(f, n) == 'n':
                    exempt = [',']
            # End field with terminal punctuation
            if n == last_subdata_index(f):
                term_punct = tuple(['.', '-', ')', '!', '?'])
                if (not sub.endswith(term_punct)
                        and not end_punct.endswith(term_punct)):
                    end_punct = ''.join([end_punct, '.'])
            # Add any necessary ending punctuation.
            if end_punct:
                append_punct(f, n, end_punct, exempt = exempt)
    if f.tag in ['110']:
        for n, sub in enumerate(f.subfields):
            end_punct = ''
            exempt = ['"']
            if n % 2 != 0 and current_sub(f, n) in ['c', 'd', 'g']:
                # Separate c subfields with space-semicolon
                if (current_sub(f, n) == 'c'
                        and next_sub(f, n) == 'c'):
                    end_punct = ';'
                # Close qualifying subfields off from following
                # subfields
                elif (n == last_subdata_index(f)
                        or next_sub(f, n) not in ['c', 'd',
                                                    'g', 'n']):
                    end_punct = ')'
                # Separate subfields with space-colon.
                else:
                    end_punct = ' :')
                # Close qualifying subfields off from preceding
                # subfields
                if (n < 3
                        or prev_sub(f, n) not in ['c', 'd',
                                                    'g', 'n']):
                    start_punct = '('
            # Check for use of subfield n as part/section
            elif current_sub(f, n) == 'n':
                if (prev_sub(f, n) not in ['k', 't']
                        and next_sub(f,n) != 'p'):
                    start_punct = '('
                if next_sub(f, n) in ['c', 'd', 'g']:
                    end_punct = ' :'
                elif next_sub(f, n) == 'p':
                    end_punct = ','
                elif next_sub(f, n)=='n':
                    end_punct = '.''
            if n < last_subdata_index(f) and n % 2 != 0:
                # Precede subfields with period.
                if next_sub(f, n) in ['b', 'f', 'k', 'l', 't']:
                    end_punct = ''.join([end_punct, '.'])
                # Precede relator with comma.
                elif next_sub(f, n) in ['e']:
                    end_punct = ''.join([end_punct, ','])
                # Precede part/section with period.
                elif next_sub(f, n) in ['n']:
                    if current_sub(f, n) in ['k', 't']:
                        end_punct = '.'
                # Do not precede with punctuation
                elif next_sub(f, n) == 'u':
                    for i in end_punct: exempt.append(i)
                    del_from_end(f, n, exempt = exempt,
                                 abbrev_exempt = True)
            # End field with terminal punctuation
            if n == last_subdata_index(f):
                term_punct = tuple(['.', '-', ')', '!', '?'])
                if (not sub.endswith(term_punct)
                        and not end_punct.endswith(term_punct)):
                    end_punct = ''.join([end_punct, '.'])
            # Add any necessary ending punctuation.
            if end_punct:
                append_punct(f, n, end_punct, exempt = exempt)
    if f.tag == '111':
        if current_sub(f, n) in ['c', 'd', 'g']:
            # Separate c subfields with space-semicolon
            if (current_sub(f, n) == 'c'
                    and next_sub(f, n) == 'c'):
                end_punct = ';'
            # Close qualifying subfields off from following
            # subfields
            elif next_sub(f, n) not in ['c', 'd', 'g', 'n']):
                end_punct = ')'
            # Separate subfields with space-colon.
            else:
                end_punct = ' :')
            # Close qualifying subfields off from preceding
            # subfields
            if prev_sub(f, n) not in ['c', 'd', 'g', 'n']):
                start_punct = '('
        # Check for use of subfield n as part/section
        elif current_sub(f, n) == 'n':
            if (prev_sub(f, n) not in ['k', 't']
                    and next_sub(f,n) != 'p'):
                start_punct = '('
            if next_sub(f, n) in ['c', 'd', 'g']:
                end_punct = ' :'
            elif next_sub(f, n) == 'p':
                end_punct = ','
            elif next_sub(f, n)=='n':
                end_punct = '.'
        # Precede subfields with period.
        if next_sub(f, n) in ['e', 'f', 'k', 'l', 'q', 't']:
            end_punct = ''.join([end_punct, '.'])
        elif next_sub(f, n) in ['g', 'j']:
            end_punct = ''.join([end_punct, ','])
        # Do not precede with punctuation
        elif next_sub(f, n) == 'u':
            for i in end_punct: exempt.append(i)
            del_from_end(f, n, exempt = exempt,
                         abbrev_exempt = True)
        # End field with terminal punctuation
        if n == last_subdata_index(f):
            term_punct = tuple(['.', '-', ')', '!', '?'])
            if (not sub.endswith(term_punct)
                    and not end_punct.endswith(term_punct)):
                end_punct = ''.join([end_punct, '.'])
        # Add any necessary ending punctuation.
        if end_punct:
            append_punct(f, n, end_punct, exempt = exempt)
    if f.tag == '130':
        for n, sub in enumerate(f.subfields):
            end_punct = ''
            exempt = ['"']
            # Enclose treaty dates in parentheses.
            if current_sub(f, n) == 'd':
                prepend_punct(f, n, '(')
                end_punct = ')'
            # Precede subfields with period.
            if next_sub(f, n) in ['f', 'g', 'h', 'k', 'l', 't']:
                end_punct = ''.join([end_punct, '.'])
            # Precede subfields with comma.
            elif next_sub(f, n) in ['m', 'r']:
                end_punct = ''.join([end_punct, ','])
            # Choose punctuation to precede subfield n
            # using context to guess how it is being used.
            elif next_sub(f, n) == ['n']:
                exempt.append(',')
                exempt.append('.')
                if f.subfields[n+1][0] != '(':
                    if current_sub(f, n) in ['a', 'd', 'k', 'n']:
                        end_punct = ''.join([end_punct, '.'])
                    elif current_sub(f, n) in ['m', 'p', 't']:
                        end_punct = ''.join([end_punct, ','])
            elif next_sub(f, n) == 'o':
                end_punct = ''.join([end_punct, ';'])
            # Preceding punctuation of subfield p is based
            # the subfield before it.
            elif next_sub(f, n) == 'p':
                if current_sub(f, n) == 'n':
                    end_punct = ''.join([end_punct, ','])
                else:
                    end_punct = ''.join([end_punct, '.'])
            elif next_sub(f, n) == 's':
                if f.subfields[n+1][0] != '(':
                    end_punct = ''.join([end_punct, '.'])
            # End field with terminal punctuation
            if n == last_subdata_index(f):
                term_punct = tuple(['.', '-', ')', '!', '?'])
                if (not sub.endswith(term_punct)
                        and not end_punct.endswith(term_punct)):
                    end_punct = ''.join([end_punct, '.'])
            # Add any necessary ending punctuation.
            if end_punct:
                append_punct(f, n, end_punct, exempt = exempt)
    if f.tag == '245':
        varying_title_fields == record.get_fields('246')
        added_entries = record.get_fields('700', '710', '711')
        uniform_titles = record.get_fields('730')
        for n, sub in enumerate(f.subfields):
            end_punct = ''
            exempt = []
            if next_sub(f, n) == 'b':
                next_data = f.subfields[n+2]
                # If preceding punctuation has been entered at the
                # beginning of the subfield b data, take that as
                # conclusive evidence of the nature of the data.
                for i in ['=', ';', ':']:
                    if next_data[0] == i:
                        f.subfields[n+2] = next_data[1:]
                        end_punct = ''.join([end_punct, i])
                # Otherwise, look to other title fields for evidence.
                if not end_punct:
                    # Search for each 246 parallel title in the 245.
                    for vtf in varying_title_fields:
                        if vtf.indicator2 == '1':
                            parallel = vtf['a'].lower()
                            # Remove any ending punctuation in search
                            # string.
                            while parallel[-1] in any_punct:
                                parallel = parallel[:-1]
                            # If the parallel title begins the 245b,
                            # precede the subfield with ' ='.
                            if next_data.lower().find(parallel) == 0:
                                end_punct = ''.join([end_punct, ' ='])
                if not end_punct:
                    # Search for added entry titles in the 245.
                    for entry in added_entries:
                        same_author = ''
                        diff_author = ''
                        if entry.indicator2 == '2' and entry['t']:
                            # Get the corresponding type of main entry.
                            main_entry = str(int(entry.tag)-600)
                            if (record[main_entry]
                                    and record[main_entry]['a'] == entry['a']):
                                same_author = entry['t'].lower()
                            else:
                                diff_author = entry['t'].lower()
                        if same_author:
                            while same_author[-1] in any_punct:
                                same_author = same_author[:1]
                            if next_data.lower().find(same_author) == 0:
                                end_punct = ''.join([end_punct, ' ;'])
                        if diff_author:
                            while diff_author[-1] in any_punct:
                                diff_author = diff_author[:1]
                            if next_data.lower().find(diff_author) == 0:
                                end_punct = ''.join([end_punct, '.'])
                if not end_punct:
                    # Search for uniform titles in the 245.
                    for ut in uniform_titles:
                        if ut['a']:
                            ut = ut['a'].lower()
                            while ut[-1] in any_punct:
                                ut = ut[:-1]
                            if next_data.lower().find(ut) == 0:
                                end_punct = ''.join([end_punct, '.'])
                if not end_punct:
                    end_punct = ' :'
            # End field with terminal punctuation.
            if n == last_subdata_index(f):
                term_punct = tuple(['!', '?'])
                if (not sub.endswith(term_punct)
                        and not end_punct.endswith(term_punct)):
                    end_punct = ''.join([end_punct, '.'])
            if end_punct:
                append_punct(f, n, end_punct, exempt = exempt)






def main():
    """Iterates through a MARC file and saves edits"""
    with open('input_mrc/enc.mrc', 'rb') as fh:
        # Open the record and encode as unicode, to prevent errors.
        reader = MARCReader(fh, to_unicode=True, force_utf8=True)
        for record in reader:
            for field in record.fields:
                # original = field.__str__()
                punctuate(field)
                # if original != field.__str__():
                    #     print(f'original: {original}')
                    #     print(f'changed: {field}')
            # # Write the edited record to a new file
            # with open('output_mrc/015.mrc', 'ab') as out:
            #     out.write(record.as_marc())

if __name__ == '__main__':
    main()
