from pymarc import MARCReader
from helpers import *
from string import *

# The ASCII and ANSEL punctuation marks, plus the Euro sign and a space
any_punct = ['!', '"', '#', '$', '%', '&', '\'', '(', ')', '*', '+', ',', '-',
             '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^',
             '_', '`', '{', '|', '}', '~', 'ʹ', '·', '♭', '®', '±', 'ʺ', '£',
             '°', '℗', '©', '♯', '¿', '¡', '€', ' ']

ascii_letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
digits = '0123456789'

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
    '043', '047', '048', '061', '066', '071', '072', '074', '080', '084',
    '085', '088', '090', '096', '098', '099', '539', '542', '599', '648',
    '662', '690', '691', '695', '720', '751', '758'
    '990'
    ]


linking_entry_fields = ['760', '762', '765', '767', '770', '772', '773',
                        '774', '775', '776', '777', '780', '785', '786',
                        '787']


def punctuate(r, f):
    """Adds the punctuation to a field. Seperated from main() to
    reduce indentation."""
    count505 = len(r.get_fields('505'))
    # Introductory relationship subfields should end in a
    # colon.
    try:
        if f.subfields[0] == 'i':
            append_punct(f, 1, ':')
        elif f.subfields[0] == '3' and f.subfields[3] == 'i':
            append_punct(f, 3, ':')
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
    if f.tag in ['017', '018', '535', '583']:
        # Field does not end with a mark of punctuation
        # unless ending in an abbreviation or data ending
        # with a mark of punctuation.
        del_from_end(f, exempt = ['?', '!', '-', '"'],
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
                data = f.subfields[n+1].replace(') ', ')')
                f.subfields[n+1] = data
    # Field ends with a mark of punctuation
    if f.tag in ['036']:
        append_punct(f, last_subdata_index(f), '.',
                     exempt = ['-', ')', '!', '?'])
    if f.tag in ['037', '653', '654', '655', '753']:
        # subfields does not end with a mark of punctuation
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
                while len(f.subfields[n+1]) < 7:
                    f.subfields[n+1] = f.subfields[n+1] + '-'
    # For 2-character codes, the trailing blank is omitted.
    if f.tag in ['044']:
        for n, sub in enumerate(f.subfields):
            if n % 2 == 0 and sub in ['a', 'b', 'c']:
                data = f.subfields[n+1]
                if len(data) == 3 and data[2] == ' ':
                    f.subfields[n+1] = data[:2]
    # Hyphens are the only marks of punctuation used.
    if f.tag in ['045']:
        punct = [x for x in any_punct if x != '-']
        remove_punct(f, punct = punct)
    # Dates should not be padded with zeros
    if f.tag in ['046']:
        for n, sub in enumerate(f.subfields):
            if current_sub(f, n) in ['b', 'c', 'd', 'e']:
                while sub[0] == '0':
                    sub = sub[1:]
    if f.tag == '049':
        for n, sub in enumerate(f.subfields):
            # Enclose subfields d & m in brackets.
            if current_sub(f, n) in ['d', 'm']:
                prepend_punct(f, n, '[')
                append_punct(f, n, ']')
            # Do not enclose subfield n in brackets.
            elif current_sub(f, n) == 'n':
                del_from_start(f, n, del_list = ['['])
                del_from_end(f, n, del_list = ['['])
    # Do not retain enclosing parentheses or brackets in record.
    if f.tag == '050':
        for n, sub in enumerate(f.subfields):
            del_from_start(f, n, del_list = ['[', '('])
            del_from_end(f, n, del_list = [']', ')'])
    # Field ends in a period.
    if f.tag in ['051', '254', '256']:
        append_punct(f, last_subdata_index(f), '.')
    if f.tag == '052':
        for n, sub in enumerate(f.subfields):
            # Cutter number does not get the starting period.
            if current_sub(f, n) == 'b':
                del_from_start(f, n, del_list = ['.'])
        # Field does not end in a period.
        del_from_end(f, last_subdata_index(f), del_list = ['.'])
    # Field does not end in a period.
    if f.tag in ['055', '070', '086']:
        del_from_end(f, last_subdata_index(f), '.', abbrev_exempt = True)
    if f.tag in ['060']:
        # Do not retain enclosing brackets in the record.
        for n, sub in enumerate(f.subfields):
            del_list = [']']
            # Do not retain separating slashes in the record.
            if next_sub(f, n) == 'a':
                del_list.append('/')
            del_from_start(f, n, del_list = ['['])
            del_from_end(f, n, del_list = del_list)
        append_punct(f, last_subdata_index(f), '.')
    # Do not retain enclosing brackets in record.
    if f.tag in ['082', '083']:
        for n, sub in enumerate(f.subfields):
            del_from_start(f, n, del_list = ['['])
            del_from_end(f, n, del_list = [']'])
    # Slashes should not be entered in subfield a.
    if f.tag == '092':
        for n, sub in enumerate(f.subfields):
            if current_sub(f, n) == 'a':
                f.subfields[n].replace('/', '')
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
                for i in ['-', '?']: exempt.append(i)
            # Subfield c is sometimes enclosed in parantheses, other
            # times preceded by a comma. As yet I have not determined
            # a method of distinguishing cases.
            elif current_sub(f, n) == 'c':
                pass
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
                del_from_end(f, del_list = ',')
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
                    end_punct = ' :'
                # Close qualifying subfields off from preceding
                # subfields
                if (n < 3
                        or prev_sub(f, n) not in ['c', 'd',
                                                    'g', 'n']):
                    start_punct = '('
            # Check for use of subfield n as part/section
            elif current_sub(f, n) == 'n':
                if (prev_sub(f, n) not in ['k', 't']
                        and next_sub(f, n) != 'p'):
                    start_punct = '('
                if next_sub(f, n) in ['c', 'd', 'g']:
                    end_punct = ' :'
                elif next_sub(f, n) == 'p':
                    end_punct = ','
                elif next_sub(f, n)=='n':
                    end_punct = '.'
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
                del_from_end(f, del_list = ',')
                term_punct = tuple(['.', '-', ')', '!', '?'])
                if (not sub.endswith(term_punct)
                        and not end_punct.endswith(term_punct)):
                    end_punct = ''.join([end_punct, '.'])
            # Add any necessary ending punctuation.
            if end_punct:
                append_punct(f, n, end_punct, exempt = exempt)
    if f.tag == '111':
        for n, sub in enumerate(f.subfields):
            end_punct = ''
            exempt = []
            if current_sub(f, n) in ['c', 'd', 'g']:
                # Separate c subfields with space-semicolon
                if (current_sub(f, n) == 'c'
                        and next_sub(f, n) == 'c'):
                    end_punct = ';'
                # Close qualifying subfields off from following
                # subfields
                elif next_sub(f, n) not in ['c', 'd', 'g', 'n']:
                    end_punct = ')'
                # Separate subfields with space-colon.
                else:
                    end_punct = ' :'
                # Close qualifying subfields off from preceding
                # subfields
                if prev_sub(f, n) not in ['c', 'd', 'g', 'n']:
                    start_punct = '('
                # Do not add punctuation to open dates.
                if current_sub(f, n) == 'd':
                    for i in ['-', '?']: exempt.append(i)
            # Check for use of subfield n as part/section
            elif current_sub(f, n) == 'n':
                if (prev_sub(f, n) not in ['k', 't']
                        and next_sub(f,n) != 'p'):
                    start_punct = '('
                if next_sub(f, n) in ['c', 'd', 'g']:
                    end_punct = ' :'
                elif next_sub(f, n) == 'p':
                    end_punct = ','
                elif next_sub(f, n)== 'n':
                    end_punct = '.'
            # Precede subfields with period.
            if next_sub(f, n) in ['e', 'f', 'k', 'l', 'q', 't']:
                end_punct = ''.join([end_punct, '.'])
            elif next_sub(f, n) in ['j']:
                end_punct = ''.join([end_punct, ','])
            elif next_sub(f, n) == 'n' and current_sub(f, n) in ['k', 't']:
                end_punct = ''.join([end_punct, '.'])
            # Do not precede with punctuation
            elif next_sub(f, n) == 'u':
                for i in end_punct: exempt.append(i)
                del_from_end(f, n, exempt = exempt,
                             abbrev_exempt = True)
            # End field with terminal punctuation
            if n == last_subdata_index(f):
                del_from_end(f, del_list = ',')
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
                del_from_end(f, del_list = ',')
                term_punct = tuple(['.', '-', ')', '!', '?'])
                if (not sub.endswith(term_punct)
                        and not end_punct.endswith(term_punct)):
                    end_punct = ''.join([end_punct, '.'])
            # Add any necessary ending punctuation.
            if end_punct:
                append_punct(f, n, end_punct, exempt = exempt)
    if f.tag in ['210', '222']:
        for n, sub in enumerate(f.subfields):
            # Enclose subfield b in parentheses.
            if current_sub(f, n) == 'b':
                prepend_punct(f, n, '(')
                append_punct(f, n, ')')
            # Omit preceding and terminal punctuation from subfields.
            if n % 2 != 0:
                del_from_end(f, n, exempt = ['...', '!', '-', '?', ']', '>', ')'],
                             abbrev_exempt = True)
    if f.tag in ['240', '243']:
        for n, sub in enumerate(f.subfields):
            end_punct = ''
            exempt = []
            # Brackets that customarily enclose a uniform title are
            # not carried in the record.
            del_from_start(f, n, del_list = ['['])
            del_from_end(f, n, del_list = [']'])
            # Precede subfields with a comma.
            if next_sub(f, n) in ['d', 'm', 'r']:
                end_punct = ''.join([end_punct, ','])
            # Precede subfields with a period.
            elif next_sub(f, n) in ['f', 'k', 'l', 'p', 's']:
                end_punct = ''.join([end_punct, '.'])
            # Precede subfields with a semicolon.
            elif next_sub(f, n) == 'o':
                end_punct = ''.join([end_punct, ';'])
            elif next_sub(f, n) == 'n':
                for i in [',', '.']: exempt.append(i)
                # Subfield n is not preceded by punctuation if it is
                # enclosed in parenthese.
                if f.subfields[n+2][0] != '(':
                    if current_sub(f, n) in ['m']:
                        end_punct = ''.join([end_punct, ','])
                    elif current_sub(f, n) in ['n']:
                        end_punct = ''.join([end_punct, '.'])
            elif next_sub(f, n) == 's':
                if f.subfields[n+2][0] != '(':
                    end_punct = ''.join([end_punct, '.'])
            # Field does not end in a mark of punctuation.
            if n = last_subdata_index(f):
                exempt.append(end_punct)
                del_from_end(f, n, exempt = exempt, abbrev_exempt = True)
            if end_punct:
                append_punct(f, n, end_punct, exempt = exempt)
    if f.tag == '242':
        for n, sub in enumerate(f.subfields):
            end_punct = ''
            exempt = ['!', '-', '?']
            if current_sub(f, n) == 'h':
                prepend_punct(f, n, '[')
                end_punct = ']'
            # Omit punctuation in subfield y.
            elif current_sub(f, n) == 'y':
                f.subfields(n) = [x for x in sub if x not in any_punct]
            # If preceding punctuation has been entered at the
            # beginning of the subfield b data, take that as
            # conclusive evidence of the nature of the data. Otherwise,
            # assume the punctuation should be a space-colon.
            if next_sub(f, n) == 'b':
                next_data = f.subfields[n+2]
                for i in ['=', ';', ':']:
                    if next_data[0] == i:
                        f.subfields[n+2] = next_data[1:]
                        end_punct = ''.join([end_punct, i])
                if not end_punct:
                    end_punct = ''.join([end_punct, ' :'])
            # Precede with ' /'.
            elif next_sub(f, n) == 'c':
                end_punct = ''.join([end_punct, ' /'])
            elif next_sub(f, n) in ['n']:
                end_punct = ''.join([end_punct, '.'])
            # Precede subfield p with a period unless it follows
            # subfield p.
            elif next_sub(f, n) == 'p':
                if current_sub(f, n) == 'n':
                    end_punct = ''.join([end_punct, ','])
                else:
                    end_punct = ''.join([end_punct, '.'])
            # Last subfield preceding subfield y ends with a period.
            if n = last_subdata_index(f):
                if current_sub(f, n) == 'f':
                    index = n - 2
                else:
                    index = n
                exempt.append(end_punct)
                append_punct(f, index, exempt = exempt, abbrev_exempt = True)
    if f.tag == '245':
        varying_title_fields = r.get_fields('246')
        added_entries = r.get_fields('700', '710', '711')
        uniform_titles = r.get_fields('730')
        for n, sub in enumerate(f.subfields):
            end_punct = ''
            exempt = []
            if current_sub(f, n) == 'g':
                prepend_punct(f, n, '(')
                end_punct = ')'
            elif current_sub(f, n) == 'h':
                prepend_punct(f, n, '[')
                end_punct = ']'
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
                            if (r[main_entry]
                                    and r[main_entry]['a'] == entry['a']):
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
                    end_punct = ''.join([end_punct, ' :'])
            # Precede statement of responsibility with ' /'.
            elif next_sub(f, n) == 'c':
                end_punct = ''.join([end_punct, ' /'])
            # Precede subfields with a comma.
            elif next_sub(f, n) == 'f':
                end_punct = ''.join([end_punct, ','])
            # Precede subfield k with ' :' if there is a subfield a.
            elif next_sub(f, n) == 'k' and f['a']:
                end_punct = ''.join([end_punct, ' :'])
            # Precede subfield with '.' unless the
            # preceding subfield ends with an '!', '-', or '?'.
            elif next_sub(f, n) in ['n', 's']:
                end_punct = ''.join([end_punct, '.'])
                for i in ['!', '-', '?']:
                    exempt.append(i)
            # Precede subfield p with a period unless it follows
            # subfield p.
            elif next_sub(f, n) == 'p':
                if current_sub(f, n) == 'n':
                    end_punct = ''.join([end_punct, ','])
                else:
                    end_punct = ''.join([end_punct, '.'])
            # End field with terminal punctuation.
            if n == last_subdata_index(f):
                del_from_end(f, del_list = ',')
                term_punct = tuple(['!', '?'])
                if (not sub.endswith(term_punct)
                        and not end_punct.endswith(term_punct)):
                    end_punct = ''.join([end_punct, '.'])
            if end_punct:
                append_punct(f, n, end_punct, exempt = exempt)
    if f.tag == '246':
        # Field does not end with final punctuation.
        del_from_end(f, abbrev_exempt = True)
        for n, sub in enumerate(f.subfields):
            end_punct = ''
            exempt = []
            # Do not enter final punctuation at the beginning or the
            # end of subfield f, except '-' or '<'/'>'.
            if current_sub(f, n) == 'f':
                del_from_start(f, n, exempt = ['-', '<'])
                del_from_end(f, n, exempt = ['-', '>'])
            # Enclose in parentheses.
            elif current_sub(f, n) == 'g':
                prepend_punct(f, n, '(')
                end_punct = ')'
            # Enclose in brackets.
            elif current_sub(f, n) == 'h':
                prepend_punct(f, n, '[')
                end_punct = ']'
            # Subfield i is taken care of before the tag is checked.
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
                            if (r[main_entry]
                                    and r[main_entry]['a'] == entry['a']):
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
                    end_punct = ''.join([end_punct, ' :'])
            # Do not enter punctuation in the subfield preceding
            # subfield f unless the preceding subfield ends with an
            # abbreviation or with parentheses.
            elif next_sub(f, n) == 'f':
                del_from_end(f, n, exempt = [')'], abbrev_exempt = True)
            # Precede subfield n with a period.
            elif next_sub(f, n) == 'n':
                end_punct = ''.join([end_punct, '.'])
            # Precede subfield p with '.' unless it follows subfield n.
            elif next_sub(f, n) == 'p':
                if current_sub(f, n) == 'n':
                    end_punct = ''.join([end_punct, ','])
                else:
                    end_punct = ''.join([end_punct, '.'])
            # Field does not end in a mark of punctuation.
            if n = last_subdata_index(f):
                exempt.append(end_punct)
                del_from_end(f, n, exempt = exempt, abbrev_exempt = True)
            if end_punct:
                append_punct(f, n, end_punct, exempt = exempt)
    if f.tag == '247':
        end_punct = ''
        exempt = ['']
        for n, sub in enumerate(f.subfields):
            # Incomplete dates should be contained in angle brackets.
            if current_sub(f, n) == 'f':
                if f.subfields[n][0] = '-':
                    prepend_punct(f, n '<')
                exempt.append('->')
            # Enclose subfield in brackets.
            elif current_sub(f, n) == 'h':
                prepend_punct(f, n, '[')
                end_punct = ']'
            # Enclose subfield g in parentheses.
            elif current_sub(f, n) == 'g':
                prepend_punct(f, n, '(')
                end_punct = ''.join([end_punct, ')'])
            # If preceding punctuation has been entered at the
            # beginning of the subfield b data, take that as
            # conclusive evidence of the nature of the data. Otherwise,
            # assume the punctuation should be a space-colon.
            if next_sub(f, n) == 'b':
                next_data = f.subfields[n+2]
                for i in ['=', ';', ':']:
                    if next_data[0] == i:
                        f.subfields[n+2] = next_data[1:]
                        end_punct = ''.join([end_punct, i])
                if not end_punct:
                    end_punct = ''.join([end_punct, ' :'])
            # Precede subfield with period.
            elif next_sub(f, n) == 'n':
                end_punct = ''.join([end_punct, '.'])
            # Precede subfield p with a period unless it follows
            # subfield p.
            elif next_sub(f, n) == 'p':
                if current_sub(f, n) == 'n':
                    end_punct = ''.join([end_punct, ','])
                else:
                    end_punct = ''.join([end_punct, '.'])
            # Field does not end in a mark of punctuation.
            if n = last_subdata_index(f):
                exempt.append(end_punct)
                del_from_end(f, n, exempt = exempt, abbrev_exempt = True)
            if end_punct:
                append_punct(f, n, end_punct, exempt = exempt)
    if f.tag == '250':
        end_punct = ''
        for n, sub in enumerate(f.subfields):
            # There is not much to go on to determine if subfield b is
            # being used for a parallel edition statement or statement
            # of responsibility. Assume it is a statement of
            # responsibility unless there is a '=' beginning or
            # preceding it.
            if next_sub(f, n) == 'b':
                if f.subfields[n+1][0] == '=':
                    del_from_start(f, n+1, '=')
                    append_punct(f, n, ' =')
                else:
                    append_punct(f, n, ' /', exempt = ['='])
            #  Field ends with a period.
            if n == last_subdata_index(f):
                del_from_end(f, del_list = ',')
                append_punct(f, n, '.')
            if end_punct:
                append_punct(f, n, end_punct, exempt = exempt)
    if f.tag in ['251', '270', '340', '341', '342', '355', '357', '363', '365',
                 '366', '377', '380', '381', '382', '384', '385', '386', '388',
                 '987']:
        # Omit preceding from subfields, with the common OCLC end
        # punctuation exceptions.
        for n, sub in enumerate(f.subfields):
            if n % 2 != 0 and n != last_subdata_index(n):
                del_from_end(f, n,
                             exempt = ['...', '!', '-', '?', ']', '>', ')'],
                             abbrev_exempt = True)
        # Omit terminal punctuation except ending abbreviations.
        del_from_end(f, abbrev_exempt = True)
    if f.tag == '255':
        for n, sub in enumerate(f.subfields):
            end_punct = ''
            exempt = []
            # subfields c, d, and e are enclosed in a single set of
            # parentheses.
            if current_sub(f, n) in ['c', 'd', 'e']:
                if prev_sub(f, n) not in ['c', 'd', 'e']:
                    prepend_punct(f, n, '(')
                if next_sub(f, n) in ['c', 'd', 'e']:
                    end_punct = ' ;'
                else:
                    end_punct = ')'
            # Projection statement is preceded by ' ;'.
            if next_sub(f, n) == 'b':
                end_punct = ''.join([end_punct, ' ;'])
            #  Field ends with a period.
            if n == last_subdata_index(f):
                del_from_end(f, del_list = ',')
                end_punct = ''.join([end_punct, '.'])
            if end_punct:
                append_punct(f, n, end_punct, exempt = exempt)
    # Omit punctuation for the end of any subfield, except the last
    # which ends in a period.
    if f.tag == '257':
        exempt = ['...', '!', '-', '?', ']', '>', ')']
        for n, sub in enumerate(f.subfields):
            if n % 2 != 0 and n != last_subdata_index(f):
                del_from_end(f, n, exempt = exempt, abbrev_exempt = True)
            elif n == last_subdata_index(f):
                append_punct(f, n, '.', exempt = exempt)
    if f.tag == '258':
        for n, sub in enumerate(f.subfields):
            # Precede subfield by a ' :'.
            if next_sub(f, n) == 'b':
                append_punct(f, n, ' :')
            # Add a terminal period.
            if n == last_subdata_index(f):
                append_punct(f, n, '.',
                             exempt = ['...', '!', '-', '?', ']', '>', ')'])
    if f.tag == '260':
        for n, sub in enumerate(f.subfields):
            end_punct = ''
            exempt = []
            if sub[0] == '[' and sub[-1] != ']':
                end_punct = ']'
            elif sub[0] != '[' and sub[-1] == ']':
                prepend_punct(f, n, '[')
            # Enclose subfields e, f, and g within 1 set of parentheses.
            if current_sub(f, n) == ['e', 'f', 'g']:
                if prev_sub(f, n) not in ['e', 'f', 'g']:
                    append_punct(f, n, '(')
                if next_sub(f, n) in ['e', 'f', 'g']:
                    end_punct = ''.join([end_punct, ' :'])
                else:
                    end_punct = ')'
            # Precede subfield 3 with ':', or ' :' if following an open
            # date.
            if n == 1 and current_sub(f, n) == '3':
                if f.subfields[n].endswith(tuple(['-', '- ', '->'])):
                    end_punct = ''.join([end_punct, ' :'])
                else:
                    end_punct = ''.join([end_punct, ':'])
            # Otherwise, precede any subfield a with ' ;'.
            elif next_sub(f, n) == 'a':
                end_punct = ''.join([end_punct, ' ;'])
            # Precede subfield b with a ' :'.
            elif next_sub(f, n) == 'b':
                end_punct = ''.join([end_punct, ' :'])
            # Precede subfield c with a comma.
            elif next_sub(f, n) == 'c':
                end_punct = ''.join([end_punct, ','])
            # Field ends with a period.
            if n == last_subdata_index(f):
                end_punct = ''.join([end_punct, '.'])
                exempt = ['...', '!', '-', '?', ']', '>', ')']
            if end_punct:
                append_punct(f, n, end_punct, exempt = exempt)
    # All punctuation for this field is taken from LC's examples,
    # although subfield guidelines and most subfields are shown with
    # contradictory preceding punctuation.
    if f.tag == '261':
        for n, sub in enumerate(f.subfields):
            end_punct = ''
            exempt = []
            if next_sub(f, n) == 'a':
                end_punct = ''.join([end_punct, ';'])
                exempt.append(',')
            elif next_sub(f, n) == 'b' or n == last_subdata_index(f):
                end_punct = ''.join([end_punct, '.'])
                exempt.append(',')
            elif next_sub(f, n) == 'd':
                end_punct = ''.join([end_punct, ','])
            elif next_sub(f, n) == 'd':
                end_punct = ''.join([end_punct, ','])
                exempt.append('.')
            if end_punct:
                append_punct(f, n, end_punct)
    if f.tag == '262':
        for n, sub in enumerate(f.subfields):
            if current_sub(f, n) in ['k', 'l']:
                 end_punct = ''.join([end_punct, '.'])
            # Field ends with a period.
            elif n == last_subdata_index(f):
                end_punct = ''.join([end_punct, '.'])
                exempt = ['...', '!', '-', '?', ']', '>', ')']
            if end_punct:
                append_punct(f, n, end_punct)
    # Omit all punctuation except hyphens.
    if f.tag in ['263', '994']:
        f = [x for x in f if x not in any_punct or x == '-']
    if f.tag == '264':
        if f.indicator2 == '4':
            del_from_end(f, n, '.')
        else:
            for n, sub in enumerate(f.subfields):
                end_punct = ''
                exempt = []
                # Precede subfield a with ' ;' unless it is the 1st
                # subfield or occurs after a subfield 3.
                if n == 1 and current_sub(f, n) == '3':
                    if f.subfields[n].endswith(tuple(['-', '- ', '->'])):
                        end_punct = ''.join([end_punct, ' :'])
                    else:
                        end_punct = ''.join([end_punct, ':'])
                elif next_sub(f, n) == 'a':
                    end_punct = ''.join([end_punct, ' ;'])
                # Precede subfield c with a comma.
                elif next_sub(f, n) == 'c':
                    end_punct = ''.join([end_punct, ','])
                # Field ends with a period.
                if n == last_subdata_index(f):
                    end_punct = ''.join([end_punct, '.'])
                    exempt = ['-', ']']
                if end_punct:
                    append_punct(f, n, end_punct, exempt = exempt)
    if f.tag == '300':
        for n, sub in enumerate(f.subfields):
            end_punct = ''
            exempt = []
            # Follow an initial subfield 3 with ':' or ' :' if
            # following an open date.
            if n == 1 and current_sub(f, n) == '3':
                if f.subfields[n].endswith(tuple(['-', '- ', '->'])):
                    end_punct = ''.join([end_punct, ' :'])
                else:
                    end_punct = ''.join([end_punct, ':'])
            # Enclose subfield a following a subfied f in parentheses.
            elif current_sub(f, n) == 'a':
                if prev_sub(f, n) == 'f':
                    prepend_punct(f, n, '(')
                    if next_sub(f, n) != 'f':
                        end_punct = ''.join([end_punct, ')'])
            elif current_sub(f, n) == 'f':
                if prev_sub(f, n) == 'a' and f.subfields[n-1][0] == '(':
                    end_punct = ''.join([end_punct, ')'])
            # Precede second and subsequent occurrences of subfield a
            # with ' +' in most cases.
            if next_sub(f, n) == 'a':
                if current_sub != 'f':
                    end_punct = ''.join([end_punct, ' +'])
            # Precede subfield b with ' :'.
            elif next_sub(f, n) == 'b':
                end_punct = ''.join([end_punct, ' :'])
            # Precede subfield c with ' ;'.
            elif next_sub(f, n) == 'c':
                end_punct = ''.join([end_punct, ' ;'])
            # Preced subfield e with ' +'
            elif next_sub(f, n) == 'e':
                end_punct = ''.join([end_punct, ' +'])
            #  Field ends with a period if the record has a 490.
            if n == last_subdata_index(f):
                if r[490]:
                    end_punct = ''.join([end_punct, '.'])
                    exempt = ['-', ']']
                else:
                    del_from_end(f, del_list = '.')
            if end_punct:
                append_punct(f, n, end_punct, exempt = exempt)
    # Omit all punctuation.
    if f.tag in ['306', '994']:
        f = [x for x in f if x not in any_punct]
    if f.tag == '307':
        for n, sub in enumerate(f.subfields):
            end_punct = ''
            exempt = []
            # Separate days from hours with a comma.
            if current_sub(f, n) == 'a':
                found = True
                while found != False:
                    for i in ['Su ', 'M ', 'Tu ', 'W ', 'Th ', 'F ', 'Sa ']:
                        if (sub.find(i) != -1
                                and sub[sub.find(i) + len(i) + 1] in digits):
                            sub.replace(i, i[:-1] + ', ')
            # Precede subfield b with a semicolon.
            if next_sub(f, n) == 'b':
                end_punct = ''.join([end_punct, ';'])
            # Field ends with a period.
            if n == last_subdata_index(f):
                del_from_end(f, del_list = ',')
                end_punct = ''.join([end_punct, '.'])
                for i in ['...', '!', '-', '?', ']', '>', ')']:
                    exempt.append(i)
            if end_punct:
                append_punct(f, n, end_punct, exempt = exempt)
    if f.tag in ['310', '321']:
        end_punct = ''
        for n, sub in enumerate(f.subfields):
            # Precede subfield with ','.
            if next_sub(f, n) == 'b':
                append_punct(f, n, ',')
        # Field does not end with final punctuation.
        del_from_end(f, exempt = ['-', '>', ')'], abbrev_exempt = True)
    if f.tag in ['336', '337', '338']:
        # Omit preceding and terminal punctuation from subfields, with
        # no exceptions.
        if n % 2 != 0:
            del_from_end(f, n)
    if f.tag == '343':
        for n, sub in enumerate(f.subfields):
            end_punct = ''
            if next_sub(f, n) in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']:
                end_punct = ';'
            #  Field ends with a period.
            if n == last_subdata_index(f):
                end_punct = '.'
            if end_punct:
                append_punct(f, n, end_punct)
    if f.tag in ['344', '345', '346', '347', '348']:
        # Omit preceding and terminal punctuation from subfields, with
        # except for periods after abbreviations.
        if n % 2 != 0:
            del_from_end(f, n, abbrev_exempt = True)
    if f.tag == '351':
        for n, sub in enumerate(f.subfields):
            end_punct = ''
            # Follow an initial subfield 3 with ':' or ' :' if
            # following an open date.
            if n == 1 and current_sub(f, n) == '3':
                if f.subfields[n].endswith(tuple(['-', '- ', '->'])):
                    end_punct = ''.join([end_punct, ' :'])
                else:
                    end_punct = ''.join([end_punct, ':'])
            # Precede subfields a, b, & c with a ';' unless preceded by
            # subfield 3.
            elif next_sub(f, n) in ['a', 'b', 'c']:
                end_punct = ''.join([end_punct, ';'])
            #  Field ends with a period.
            if n == last_subdata_index(f):
                end_punct = ''.join([end_punct, '.'])
            if end_punct:
                append_punct(f, n, end_punct)
    if f.tag == '352':
        for n, sub in enumerate(f.subfields):
            end_punct = ''
            # Enclose the text in subfield ǂc in parentheses.
            if current_sub(f, n) == 'c':
                prepend_punct(f, n, '(')
                end_punct = ''.join([end_punct, ')'])
            # Enclose consecutive subfields d and/or e within 1 set of
            # parentheses.
            elif current_sub(f, n) in ['d', 'e']:
                if prev_sub(f, n) not in ['d', 'e']:
                    prepend_punct(f, n, '(')
                if next_sub(f, n) not in ['d', 'e']:
                    end_punct = ''.join([end_punct, ')'])
            # OCLC says: Precede subfields b and i by ' :' or ','
            # "as appropriate"; it is unclear to me what determines
            # what is approriate.
            if next_sub(f, n) in ['b', 'i']:
                if current_sub(f, n) == 'a':
                    end_punct = ''.join([end_punct, ' :'])
                else:
                    end_punct = ''.join([end_punct, ','])
            # Precede subfields ǂf, ǂg, and ǂq by a space-semicolon.
            elif next_sub(f, n) in ['f', 'g', 'q']:
                end_punct = ''.join([end_punct, ' ;'])
            #  Field ends with a period.
            if n == last_subdata_index(f):
                end_punct = ''.join([end_punct, '.'])
            if end_punct:
                append_punct(f, n, end_punct)
    if f.tag == '362':
        for n, sub in enumerate(f.subfields):
            end_punct = ''
            exempt = []
            # Precede subfield ǂz with a period.
            if next_sub(f, n) == 'z':
                end_punct = ''.join([end_punct, '.'])
            # Field ends with a period.
            if n == last_subdata_index(f):
                end_punct = ''.join([end_punct, '.'])
                exempt = ['...', '!', '-', '?', ']', '>', ')']
            if end_punct:
                append_punct(f, n, end_punct, exempt = exempt)
    if f.tag == '370':
        for n, sub in enumerate(f.subfields):
            end_punct = ''
            exempt = []
            # Precede subfield 3 with ':', or ' :' if following an open
            # date.
            if n == 1 and current_sub(f, n) == '3':
                if f.subfields[n].endswith(tuple(['-', '- ', '->'])):
                    end_punct = ''.join([end_punct, ' :'])
                else:
                    end_punct = ''.join([end_punct, ':'])
            # Omit preceding from subfields, with the common OCLC end
            # punctuation exceptions.
            if n % 2 != 0 and n != last_subdata_index(n):
                del_from_end(f, n,
                             exempt = ['...', '!', '-', '?', ']', '>', ')'],
                             abbrev_exempt = True)
            if end_punct:
                append_punct(f, n, end_punct, exempt = exempt)
        # Omit terminal punctuation except ending abbreviations.
        del_from_end(f, abbrev_exempt = True)
    if f.tag == '383':
        # Omit preceding from subfields, with the common OCLC end
        # punctuation exceptions.
        for n, sub in enumerate(f.subfields):
            if current_sub(f, n) and prev_sub(f, n):
                append_punct(f, n, ',')
            elif n % 2 != 0 and n != last_subdata_index(n):
                del_from_end(f, n,
                             exempt = ['...', '!', '-', '?', ']', '>', ')'],
                             abbrev_exempt = True)
        # Omit terminal punctuation except ending abbreviations.
        del_from_end(f, abbrev_exempt = True)
    if f.tag == '490':
        for n, sub in enumerate(f.subfields):
            end_punct = ''
            exempt = []
            # Follow an initial subfield 3 with ':' or ' :' if
            # following an open date.
            if n == 1 and current_sub(f, n) == '3':
                if f.subfields[n].endswith(tuple(['-', '- ', '->'])):
                    end_punct = ''.join([end_punct, ' :'])
                else:
                    end_punct = ''.join([end_punct, ':'])
            # Enclose subfield l in parentheses.
            elif current_sub(f, n) == 'l':
                prepend_punct(f, n, '(')
                end_punct = ''.join([end_punct, ')'])
            # Subfield a can be ued for parallel titles or subseries
            # titles. I don't know of any other information in the
            # record which could be used to distinguish between them.
            if next_sub(f, n) == 'a':
                if current_sub(f, n) == 'a':
                    end_punct = ''.join([end_punct, ' ='])
                elif current_sub(f, n) == 'v':
                    digits = f.subfields[n].lstrip(ascii_letters)
                    if (len(f.subfields) >= n+2
                            and f.subfields[n+1] == 'v'
                            and f.subfields[n+2].endswith(digits)):
                        end_punct = ''.join([end_punct, '.'])
                        exempt = any_punct
            # Precede subfield v with ' ;'.
            elif next_sub(f, n) == 'v':
                end_punct = ''.join([end_punct, ' ;'])
            # Precede subfield x with ' ;'.
            elif next_sub(f, n) == 'x':
                end_punct = ''.join([end_punct, ','])
            # Field does not end with a mark of punctuation unless the
            # field ends with an abbreviation or mark of punctuation.
            if n == last_subdata_index(f):
                del_from_end(f, n, exempt = ['!', '?', '"'],
                             abbrev_exempt = True)
            if end_punct:
                append_punct(f, n, end_punct, exempt = exempt)
    if f.tag == '500':
        for n, sub in enumerate(f.subfields):
            end_punct = ''
            exempt = []
            # Follow an initial subfield 3 with ':' or ' :' if
            # following an open date.
            if n == 1 and current_sub(f, n) == '3':
                if f.subfields[n].endswith(tuple(['-', '- ', '->'])):
                    end_punct = ''.join([end_punct, ' :'])
                else:
                    end_punct = ''.join([end_punct, ':'])
            # The field ends with a period unless another mark of
            # punctuation is present.
            if n == last_subdata_index(f):
                del_from_end(f, del_list = ',')
                end_punct = ''.join([end_punct, '.'])
                exempt = ['?', '!', '"']
            if end_punct:
                append_punct(f, n, end_punct, exempt = exempt)
    # Field ends with a '.' unless it ends with a common OCLC exception
    # (based on examples).
    if f.tag in ['501', '508', '567']:
        append_punct(f, last_subdata_index(f), '.',
                     exempt = ['!', '-', '?', ']', '>', ')'])
    # Notes with a single subfield a end in a '.', others do not.
    if f.tag == '502':
        if f.get_subfields('a') == '1':
            append_punct(f, last_subdata_index(f), '.')
        else:
            del_from_end(f, del_list = ['.'], abbrev_exempt = True)
    # Subfield a ends in a period.
    if f.tag == '504':
        for n, sub in f.subfields:
            if current_sub(f, n) == 'a':
                append_punct(f, n, '.')
    # 505 has too subfields with ambiguous punctuation: g may be
    # enclosed in parentheses or preceded by 2 dashes; t may be
    # preceded by 2 dashes, a period, or a semicolon.
    if f.tag == '505':
        count505 -= 1
        for n, sub in f.subfields:
            # Preceded statement of responsibility with ' /'.
            if next_sub(f, n) == 'r':
                append_punct(f, n, ' /')
        # End the last 505 field with a period.
        if count505 == 0:
            append_punct(f, last_subdata_index(n), '.')
        else:
            del_from_end(f, del_list = ['.'], exempt = ['!', '-', '?', '>'],
                         abbrev_exempt = True)
    if f.tag == '506':
        for n, sub in enumerate(f.subfields):
            end_punct = ''
            # Follow an initial subfield 3 by ':' or ' :' if following
            # an open date.
            if n == 1 and current_sub(f, n) == '3':
                if f.subfields[n].endswith(tuple(['-', '- ', '->'])):
                    end_punct = ''.join([end_punct, ' :'])
                else:
                    end_punct = ''.join([end_punct, ':'])
            # Otherwise, precede subfields a, b, c, d, and e by ';'.
            elif next_sub(f, n) in ['a', 'b', 'c', 'd', 'e']:
                end_punct = ''.join([end_punct, ';'])
            # Precede subfield ǂf by '.'; add terminal punctuation
            # before subfields g or q.
            elif (next_sub(f, n) in ['f', 'g', 'q']
                    or (n == last_subdata_index(f)
                    and current_sub(f, n) not in ['g', 'q'])):
                end_punct = ''.join([end_punct, '.'])
            if end_punct:
                append_punct(f, n, end_punct)
    if f.tag in ['507', '513']:
        for n, sub in enumerate(f.subfields):
            # Subfield b seems to be preceded by ';'.
            if next_sub(f, n) == 'b':
                append_punct(f, n, ';')
            # Field ends in a period.
            elif n == last_subdata_index(f):
                append_punct(f, n, '.', exempt = ['-', '?', '!']))
    if f.tag == '510':
        for n, sub in enumerate(f.subfields):
            end_punct = ''
            # Field does not end with punctuation, unless ending with
            # an abbreviation or other data that ends with punctuation.
            if n == last_subdata_index:
                exempt = ['...', '!', '-', '?', ']', '>', ')']
                del_from_end(f, exempt = exempt)
            # Subfields a, b, c, and/or x end in ',' if another
            # subfield follows.
            elif current_sub(f, n) in ['a', 'b', 'c', 'x']:
                end_punct = ''.join([end_punct, ','])
            if end_punct:
                append_punct(f, n, end_punct)
    # Fields end with a period unless another mark of punctuation
    # (as defined by LC) is present.
    if f.tag in ['511', '514', '515', '516', '518', '520', '521', '522',
                 '524', '525', '526', '534', '538', '541', '544', '545',
                 '546', '547', '550', '552', '555', '556', '561', '562',
                 '563', '565', '580', '581', '584', '585', '588', '590',
                 '591', '592', '593', '594', '595', '596', '597', '598',
                 '752'
                 ]:
        append_punct(f, last_subdata_index(f), '.',
                     exempt = ['!', '-', '?', '"'])
    if f.tag == '530':
        for n, sub in enumerate(f.subfields):
            end_punct = ''
            exempt = []
            # All subfields appear to be separated by ';', except when
            # following subfield 3.
            if (current_sub(f, n) != '3'
                    and next_sub(f, n) in ['a', 'b', 'c', 'd']):
                end_punct = ''.join([end_punct, ';'])
            # Field ends with '.' unless another LC punctuation mark is
            # present.
            if n == last_subdata_index(f):
                end_punct = ''.join([end_punct, '.'])
                exempt = ['!', '-', '?', '"']
            if end_punct:
                append_punct(f, n, end_punct, exempt = exempt)
    if f.tag == '532':
        # Field does not end with final punctuation.
        del_from_end(f, abbrev_exempt = True)
    # Examples show inconsistent punctuation for several subfields.
    if f.tag == '533':
        for n, sub in enumerate(f.subfields):
            end_punct = ''
            exempt = []
            # Subfield a ends in a '.'
            if current_sub(f, n) in 'a':
                end_punct = ''.join([end_punct, '.'])
            # Exempt dates ending in '-' or ']' from receiving
            # punctuation.
            elif current_sub(f, n) in ['d', 'm']:
                for i in ['-', ']']: exempt.append(i)
            # Enclose subfield f in parentheses.
            elif current_sub(f, n) == 'f':
                prepend_punct(f, n, '(')
                end_punct = ''.join([end_punct, ')'])
            # Follow an initial subfield 3 with ':' or ' :' if
            # following an open date.
            if n == 1 and current_sub(f, n) == '3':
                if f.subfields[n].endswith(tuple(['-', '- ', '->'])):
                    end_punct = ''.join([end_punct, ' :'])
                else:
                    end_punct = ''.join([end_punct, ':'])
            # Precede subfields b, e, f with '.', and end the field
            # with '.'.
            elif (next_sub(f, n) in ['b', 'e', 'f']
                    or n == last_subdata_index(n)):
                if end_punct[-1] != '.':
                    end_punct = ''.join([end_punct, '.'])
            # Precede subfield with a colon.
            elif next_sub(f, n) == 'c':
                end_punct = ''.join([end_punct, ' :'])
            # Precede subfield with a comma.
            elif next_sub(f, n) == 'd':
                end_punct = ''.join([end_punct, ','])
            # Do not end terminal period if field ends in an LC
            # punctuation mark.
            if n == last_subdata_index(f):
                exempt = ['!', '-', '?', '"']
            if end_punct:
                append_punct(f, n, end_punct, exempt = exempt)
    if f.tag == '540':
        for n, sub in enumerate(f.subfields):
            end_punct = ''
            exempt = []
            # Precede subfield 3 with ':', or ' :' if following an open
            # date.
            if n == 1 and current_sub(f, n) == '3':
                if f.subfields[n].endswith(tuple(['-', '- ', '->'])):
                    end_punct = ''.join([end_punct, ' :'])
                else:
                    end_punct = ''.join([end_punct, ':'])
            elif next_sub(f, n) in ['b', 'c', 'd']:
                end_punct = ''.join([end_punct, ';'])
            elif next_sub(f, n) == 'u':
                end_punct = ''.join([end_punct, ':'])
            # Add terminal punctuation before subfields g or q.
            elif (next_sub(f, n) in ['g', 'q']
                    or (n == last_subdata_index(f)
                    and current_sub(f, n) not in ['g', 'q'])):
                end_punct = ''.join([end_punct, '.'])
            if end_punct:
                append_punct(f, n, end_punct, exempt = exempt)
    if f.tag in ['600', '696']:
        for n, sub in enumerate(f.subfields):
            end_punct = ''
            exempt = ['"']
            # Follow an initial subfield 3 with ':' or ' :' if
            # following an open date.
            if n == 1 and current_sub(f, n) == '3':
                if f.subfields[n].endswith(tuple(['-', '- ', '->'])):
                    end_punct = ''.join([end_punct, ' :'])
                else:
                    end_punct = ''.join([end_punct, ':'])
            elif current_sub(f, n) in ['a', 'z']:
                exempt.append(')')
            # Do not add punctuation to open dates.
            elif current_sub(f, n) in ['d']:
                for i in ['-', '?']: exempt.append(i)
            # Enclose qualifying information in parentheses.
            elif current_sub(f, n) in ['q']:
                prepend_punct(f, n, '(')
                end_punct = ''.join([end_punct, ')'])
            # Numeration should not be preceded by punctuation.
            if next_sub(f, n) == 'b':
                del_from_end(f, n, exempt = exempt, abbrev_exempt = True)
            # Precede subfields with comma.
            elif next_sub(f, n) in ['d', 'e', 'j', 'm', 'r']:
                end_punct = ''.join([end_punct, ','])
            # Preced subfieds with a period.
            elif next_sub(f, n) in ['f', 'k', 'l', 't']:
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
            # Subfield s is preceded by a period, but under mysterious
            # circumstances it is enclosed in parentheses instead.
            elif next_sub(f, n) == 's':
                if f.subfields[n+1][0] != '(':
                    end_punct = ''.join([end_punct, '.'])
            # Do not precede with any punctuation
            elif next_sub(f, n) in ['u', 'v', 'x', 'y', 'z']:
                for i in end_punct: exempt.append(i)
                del_from_end(f, n, exempt = exempt,
                             abbrev_exempt = True)
            # End field with terminal punctuation
            if n == last_subdata_index(f):
                del_from_end(f, del_list = ',')
                term_punct = tuple(['.', '-', ')', '!', '?'])
                if (not sub.endswith(term_punct)
                        and not end_punct.endswith(term_punct)):
                    end_punct = ''.join([end_punct, '.'])
            # Add any necessary ending punctuation.
            if end_punct:
                append_punct(f, n, end_punct, exempt = exempt)
    if f.tag in ['610', '697']:
        for n, sub in enumerate(f.subfields):
            end_punct = ''
            exempt = ['"']
            # Follow an initial subfield 3 with ':' or ' :' if
            # following an open date.
            if n == 1 and current_sub(f, n) == '3':
                if f.subfields[n].endswith(tuple(['-', '- ', '->'])):
                    end_punct = ''.join([end_punct, ' :'])
                else:
                    end_punct = ''.join([end_punct, ':'])
            elif current_sub(f, n) in ['c', 'd', 'g']:
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
                    end_punct = ' :'
                # Close qualifying subfields off from preceding
                # subfields
                if (n < 3
                        or prev_sub(f, n) not in ['c', 'd',
                                                    'g', 'n']):
                    start_punct = '('
            # Enclose subfield in brackets.
            elif current_sub(f, n) == 'h':
                prepend_punct(f, n, '[')
                end_punct = ']'
            # Check for use of subfield n as part/section
            elif current_sub(f, n) == 'n':
                if (prev_sub(f, n) not in ['k', 'm', 't']
                        and next_sub(f, n) != 'p'):
                    start_punct = '('
                if next_sub(f, n) in ['c', 'd', 'g']:
                    end_punct = ' :'
                elif next_sub(f, n) == 'p':
                    end_punct = ','
                elif next_sub(f, n)=='n':
                    end_punct = '.'
            # Precede subfields with period.
            if next_sub(f, n) in ['b', 'f', 'k', 'l', 's', 't']:
                end_punct = ''.join([end_punct, '.'])
            # Precede subfields with comma.
            elif next_sub(f, n) in ['e', 'm', 'r']:
                end_punct = ''.join([end_punct, ','])
            # Precede part/section with period.
            elif next_sub(f, n) in ['n']:
                if current_sub(f, n) in ['k', 't']:
                    end_punct = '.'
                elif current_sub(f, n) == 'm':
                    end_punct = ','
            # Precede arranged statement with semicolon.
            elif next_sub(f, n) == 'o':
                end_punct = ''.join([end_punct, ';'])
            # Preceding punctuation of subfield p is based
            # the subfield before it.
            elif next_sub(f, n) == 'p':
                if current_sub(f, n) == 'n':
                    end_punct = ''.join([end_punct, ','])
                else:
                    end_punct = ''.join([end_punct, '.'])
            # Do not precede with punctuation
            elif next_sub(f, n) in ['u', 'v', 'x', 'y', 'z']:
                for i in end_punct: exempt.append(i)
                del_from_end(f, n, exempt = exempt,
                             abbrev_exempt = True)
            # End field with terminal punctuation
            if n == last_subdata_index(f):
                del_from_end(f, del_list = ',')
                term_punct = tuple(['.', '-', ')', '!', '?'])
                if (not sub.endswith(term_punct)
                        and not end_punct.endswith(term_punct)):
                    end_punct = ''.join([end_punct, '.'])
            # Add any necessary ending punctuation.
            if end_punct:
                append_punct(f, n, end_punct, exempt = exempt)
    if f.tag in ['611', '698']:
        for n, sub in enumerate(f.subfields):
            end_punct = ''
            exempt = ['"']
            # Precede subfield a with ' ;' unless it is the 1st
            # subfield or occurs after a subfield 3.
            if n == 1 and current_sub(f, n) == '3':
                if f.subfields[n].endswith(tuple(['-', '- ', '->'])):
                    end_punct = ''.join([end_punct, ' :'])
                else:
                    end_punct = ''.join([end_punct, ':'])
            elif current_sub(f, n) in ['c', 'd', 'g']:
                # Separate c subfields with ' ;'.
                if (current_sub(f, n) == 'c'
                        and next_sub(f, n) == 'c'):
                    end_punct = ';'
                # Close qualifying subfields off from following
                # subfields.
                elif (n == last_subdata_index(f)
                        or next_sub(f, n) not in ['c', 'd', 'g', 'n']):
                    end_punct = ')'
                # Separate subfields with ' :'.
                else:
                    end_punct = ' :'
                # Close qualifying subfields off form preceding
                # subfields.
                if (n < 3
                        or prev_sub(f, n) not in ['c', 'd', 'g', 'n']):
                    start_punct = '('
                # Do not add punctuation to open dates.
                if current_sub(f, n) == 'd':
                    for i in ['-', '?']: exempt.append(i)
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
            # Precede subfields with a period.
            if next_sub(f, n) in ['e', 'f', 'k', 'l', 'q', 's', 't']:
                end_punct = ''.join([end_punct, '.'])
            # Preced subfields with a comma.
            elif next_sub(f, n) in ['j']:
                end_punct = ''.join([end_punct, ','])
            elif next_sub(f, n) == 'n' and current_sub(f, n) in ['k', 't']:
                end_punct = ''.join([end_punct, '.'])
            # Preceding punctuation of subfield p is based
            # the subfield before it.
            elif next_sub(f, n) == 'p':
                if current_sub(f, n) == 'n':
                    end_punct = ''.join([end_punct, ','])
                else:
                    end_punct = ''.join([end_punct, '.'])
            # Do not precede with any punctuation
            elif next_sub(f, n) == ['u', 'v', 'x', 'y', 'z':
                for i in end_punct: exempt.append(i)
                del_from_end(f, n, exempt = exempt,
                             abbrev_exempt = True)
            # End field with terminal punctuation.
            if n == last_subdata_index(f):
                del_from_end(f, del_list = ',')
                term_punct = tuple(['.', '-', ')', '!', '?'])
                if (not sub.endswith(term_punct)
                        and not end_punct.endswith(term_punct)):
                    end_punct = ''.join([end_punct, '.'])
            # Add any necessary ending punctuation.
            if end_punct:
                append_punct(f, n, end_punct, exempt = exempt)
    if f.tag in ['630', '699']:
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
            elif next_sub(f, n) in ['e', 'm', 'r']:
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
            # Do not precede with any punctuation
            elif next_sub(f, n) in ['v', 'x', 'y', 'z']:
                for i in end_punct: exempt.append(i)
                del_from_end(f, n, exempt = exempt,
                                         abbrev_exempt = True)
            # End field with terminal punctuation
            if n == last_subdata_index(f):
                del_from_end(f, del_list = ',')
                term_punct = tuple(['.', '-', ')', '!', '?'])
                if (not sub.endswith(term_punct)
                        and not end_punct.endswith(term_punct)):
                    end_punct = ''.join([end_punct, '.'])
            # Add any necessary ending punctuation.
            if end_punct:
                append_punct(f, n, end_punct, exempt = exempt)
    if f.tag in ['647', '688']:
        # Field does not end with a mark of punctuation
        # unless ending in an abbreviation or data ending
        # with a mark of punctuation.
        del_from_end(f, exempt = ['...', '-', ')', '!', '?'],
                     abbrev_exempt = True)
    if f.tag == '650':
        for n, sub in enumerate(f.subfields):
            end_punct = ''
            exempt = ['"']
            if current_sub(f, n) in ['a', 'z']:
                exempt.append(')')
            elif current_sub(f, n) == 'd':
                for i in ['-', '?']: exempt.append(i)
            # Precede subordinate units with a period.
            if next_sub(f, n) == 'b':
                end_punct = ''.join([end_punct, '.'])
            # Punctuation for c, d, g unclear.
            # Precede relator terms with a comma.
            elif next_sub(f, n) == 'e':
                end_punct = ''.join([end_punct, ','])
            # Do not precede subdivisions with any punctuation.
            elif next_sub(f, n) in ['v', 'x', 'y', 'z']:
                for i in end_punct: exempt.append(i)
                del_from_end(f, n, exempt = exempt,
                             abbrev_exempt = True)
            # End field with terminal punctuation.
            if n == last_subdata_index(f):
                del_from_end(f, del_list = ',')
                term_punct = tuple(['.', '-', ')', '!', '?'])
                if (not sub.endswith(term_punct)
                        and not end_punct.endswith(term_punct)):
                    end_punct = ''.join([end_punct, '.'])
            # Add any necessary ending punctuation.
            if end_punct:
                append_punct(f, n, end_punct, exempt = exempt)
    if f.tag == '651':
        for n, sub in enumerate(f.subfields):
            end_punct = ''
            exempt = []
            if current_sub(f, n) in ['a', 'z']:
                exempt.append(')')
            # Precede subfield with a comma.
            if next_sub(f, n) == 'e':
                end_punct = ''.join([end_punct, ','])
            # Do not precede subdivisions with any punctuation.
            elif next_sub(f, n) in ['g', 'v', 'x', 'y', 'z']:
                for i in end_punct: exempt.append(i)
                del_from_end(f, n, exempt = exempt,
                             abbrev_exempt = True)
            # End field with terminal punctuation.
            if n == last_subdata_index(f):
                del_from_end(f, del_list = ',')
                term_punct = tuple(['.', '-', ')', '!', '?'])
                if (not sub.endswith(term_punct)
                        and not end_punct.endswith(term_punct)):
                    end_punct = ''.join([end_punct, '.'])
            # Add any necessary ending punctuation.
            if end_punct:
                append_punct(f, n, end_punct, exempt = exempt)
    if f.tag in ['654', '655', '656', '657', '658', '740', '754']:
        for n, sub in enumerate(f.subfields):
            # Field ends with a period unless there is punctuation.
            if n == last_subdata_index(f):
                append_punct(f, n, '.'exempt = ['?', '!', '-', ')', '"'])
            # Punctuation does not separate subdivisions.
            elif n % 2 != 0:
                del_from_end(f, n, exempt = ['?', '!', '-', ')', '"'],
                             abbrev_exempt = True)
    if f.tag == '700':
        for n, sub in enumerate(f.subfields):
            end_punct = ''
            exempt = []
            # Follow an initial subfield 3 with ':' or ' :' if
            # following an open date.
            if n == 1 and current_sub(f, n) == '3':
                if f.subfields[n].endswith(tuple(['-', '- ', '->'])):
                    end_punct = ''.join([end_punct, ' :'])
                else:
                    end_punct = ''.join([end_punct, ':'])
            # Do not add punctuation to open dates.
            elif current_sub(f, n) in ['d']:
                for i in ['-', '?']: exempt.append(i)
            # Do not add punctuation to titles ending in punctuation.
            elif current_sub(f, n) in ['t']:
                for i in ['-', '!', '?']: exempt.append(i)
            # Enclose qualifying information in parentheses.
            elif current_sub(f, n) in ['q']:
                prepend_punct(f, n, '(')
                end_punct = ''.join([end_punct, ')'])
            elif current_sub(f, n) == 's':
                if prev_sub(f, n) == 'l':
                    prepend_punct(f, n, '(')
                    end_punct = ''.join([end_punct, ')'])
            # Numeration should not be preceded by punctuation.
            if next_sub(f, n) == 'b':
                del_from_end(f, n, exempt = exempt, abbrev_exempt = True)
            # Precede date with a comma, unless it is following other
            # qualifying information.
            elif next_sub(f, n) == 'd':
                if not (f.subfields[n].find('(')
                        and not f.subfields[n].find(')')):
                    end_punct = ''.join([end_punct, ','])
                    exempt.append(' :')
            # Precede subfields with comma.
            elif next_sub(f, n) in ['e', 'j', 'm', 'r']:
                end_punct = ''.join([end_punct, ','])
            # Preced subfieds with a period.
            elif next_sub(f, n) in ['f', 'h', 'k', 'l', 't']:
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
            # Subfield s is preceded by a period, but seems to be
            # enclosed in parentheses instead when following l.
            elif next_sub(f, n) == 's' and current_sub != 'l':
                end_punct = ''.join([end_punct, '.'])
            # Do not precede with any punctuation
            elif next_sub(f, n) == 'u':
                for i in end_punct: exempt.append(i)
                del_from_end(f, n, exempt = exempt,
                             abbrev_exempt = True)
            # End field with terminal punctuation.
            if n == last_subdata_index(f):
                del_from_end(f, del_list = ',')
                term_punct = tuple(['.', '-', ')', '!', '?'])
                if (not sub.endswith(term_punct)
                        and not end_punct.endswith(term_punct)):
                    end_punct = ''.join([end_punct, '.'])
            # Add any necessary ending punctuation.
            if end_punct:
                append_punct(f, n, end_punct, exempt = exempt)
    if f.tag in ['710']:
        for n, sub in enumerate(f.subfields):
            end_punct = ''
            exempt = ['"']
            # Precede subfield a with ' ;' unless it is the 1st
            # subfield or occurs after a subfield 3.
            if n == 1 and current_sub(f, n) == '3':
                if f.subfields[n].endswith(tuple(['-', '- ', '->'])):
                    end_punct = ''.join([end_punct, ' :'])
                else:
                    end_punct = ''.join([end_punct, ':'])
            elif current_sub(f, n) in ['c', 'd', 'g']:
                # Separate c subfields with ' ;'.
                if (current_sub(f, n) == 'c'
                        and next_sub(f, n) == 'c'):
                    end_punct = ';'
                # Close qualifying subfields off from following
                # subfields.
                elif (n == last_subdata_index(f)
                        or next_sub(f, n) not in ['c', 'd', 'g', 'n']):
                    end_punct = ')'
                # Separate subfields with ' :'.
                else:
                    end_punct = ' :'
                # Close qualifying subfields off form preceding
                # subfields.
                if (n < 3
                        or prev_sub(f, n) not in ['c', 'd', 'g', 'n']):
                    start_punct = '('
                # Do not add punctuation to open dates.
                if current_sub(f, n) == 'd':
                    for i in ['-', '?']: exempt.append(i)
            # Check for use of subfield n as part/section.
            elif current_sub(f, n) == 'n':
                if (prev_sub(f, n) not in ['k', 't']
                        and next_sub(f, n) != 'p'):
                    start_punct = '('
                if next_sub(f, n) in ['c', 'd', 'g']:
                    end_punct = ' :'
            elif current_sub(f, n) == 's':
                if prev_sub(f, n) == 'l':
                    prepend_punct(f, n, '(')
                    end_punct = ''.join([end_punct, ')'])
            elif current_sub(f, n) == 't':
                for i in ['!', '-', '?']:
                    exempt.append(i)
            # Precede subfields with a period.
            if next_sub(f, n) in ['b', 'f', 'k', 'l', 't']:
                end_punct = ''.join([end_punct, '.'])
            # Precede subfields with comma.
            elif next_sub(f, n) in ['e', 'm', 'r']:
                end_punct = ''.join([end_punct, ','])
            # Choose punctuation to precede subfield n
            # using context to guess how it is being used.
            elif next_sub(f, n) == ['n']:
                exempt.append(',')
                exempt.append('.')
                if f.subfields[n+1][0] != '(':
                    if current_sub(f, n) in ['t', 'k']:
                        end_punct = ''.join([end_punct, '.'])
                    elif current_sub(f, n) in ['c', 'd', 'g']:
                        end_punct = ''.join([end_punct, ' :'])
            elif next_sub(f, n) == 'o':
                end_punct = ''.join([end_punct, ';'])
            # Preceding punctuation of subfield p is based
            # the subfield before it.
            elif next_sub(f, n) == 'p':
                if current_sub(f, n) == 'n':
                    end_punct = ''.join([end_punct, ','])
                else:
                    end_punct = ''.join([end_punct, '.'])
            # Subfield s is preceded by a period, but seems to be
            # enclosed in parentheses instead when following l.
            elif next_sub(f, n) == 's' and current_sub != 'l':
                end_punct = ''.join([end_punct, '.'])
            # Do not precede with any punctuation
            elif next_sub(f, n) == 'u':
                for i in end_punct: exempt.append(i)
                del_from_end(f, n, exempt = exempt,
                             abbrev_exempt = True)
            # End field with terminal punctuation.
            if n == last_subdata_index(f):
                del_from_end(f, del_list = ',')
                term_punct = tuple(['.', '-', ')', '!', '?'])
                if (not sub.endswith(term_punct)
                        and not end_punct.endswith(term_punct)):
                    end_punct = ''.join([end_punct, '.'])
            # Add any necessary ending punctuation.
            if end_punct:
                append_punct(f, n, end_punct, exempt = exempt)
    if f.tag == '711':
        for n, sub in enumerate(f.subfields):
            end_punct = ''
            exempt = ['"']
            # Precede subfield a with ' ;' unless it is the 1st
            # subfield or occurs after a subfield 3.
            if n == 1 and current_sub(f, n) == '3':
                if f.subfields[n].endswith(tuple(['-', '- ', '->'])):
                    end_punct = ''.join([end_punct, ' :'])
                else:
                    end_punct = ''.join([end_punct, ':'])
            elif current_sub(f, n) in ['c', 'd', 'g']:
                # Separate c subfields with ' ;'.
                if (current_sub(f, n) == 'c'
                        and next_sub(f, n) == 'c'):
                    end_punct = ';'
                # Close qualifying subfields off from following
                # subfields.
                elif (n == last_subdata_index(f)
                        or next_sub(f, n) not in ['c', 'd', 'g', 'n']):
                    end_punct = ')'
                # Separate subfields with ' :'.
                else:
                    end_punct = ' :'
                # Close qualifying subfields off form preceding
                # subfields.
                if (n < 3
                        or prev_sub(f, n) not in ['c', 'd', 'g', 'n']):
                    start_punct = '('
                # Do not add punctuation to open dates.
                if current_sub(f, n) == 'd':
                    for i in ['-', '?']: exempt.append(i)
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
            # Precede subfields with a period.
            if next_sub(f, n) in ['e', 'f', 'k', 'l', 'q', 's', 't']:
                end_punct = ''.join([end_punct, '.'])
            # Preced subfields with a comma.
            elif next_sub(f, n) in ['j']:
                end_punct = ''.join([end_punct, ','])
            elif next_sub(f, n) == 'n' and current_sub(f, n) in ['k', 't']:
                end_punct = ''.join([end_punct, '.'])
            # Preceding punctuation of subfield p is based
            # the subfield before it.
            elif next_sub(f, n) == 'p':
                if current_sub(f, n) == 'n':
                    end_punct = ''.join([end_punct, ','])
                else:
                    end_punct = ''.join([end_punct, '.'])
            # Do not precede with any punctuation
            elif next_sub(f, n) == 'u':
                for i in end_punct: exempt.append(i)
                del_from_end(f, n, exempt = exempt,
                             abbrev_exempt = True)
            # End field with terminal punctuation.
            if n == last_subdata_index(f):
                del_from_end(f, del_list = ',')
                term_punct = tuple(['.', '-', ')', '!', '?'])
                if (not sub.endswith(term_punct)
                        and not end_punct.endswith(term_punct)):
                    end_punct = ''.join([end_punct, '.'])
            # Add any necessary ending punctuation.
            if end_punct:
                append_punct(f, n, end_punct, exempt = exempt)
    if f.tag in ['730', '830']:
        for n, sub in enumerate(f.subfields):
            end_punct = ''
            exempt = ['"']
            # Follow an initial subfield 3 with ':' or ' :' if
            # following an open date.
            if n == 1 and current_sub(f, n) == '3':
                if f.subfields[n].endswith(tuple(['-', '- ', '->'])):
                    end_punct = ''.join([end_punct, ' :'])
                else:
                    end_punct = ''.join([end_punct, ':'])
            # Precede date with a comma, unless it is following other
            # qualifying information.
            elif current_sub(f, n) == 'd':
                prepend_punct(f, n, '(')
                end_punct = ''.join([end_punct, ')'])
            # Enclose subfield h in brackets.
            elif current_sub(f, n) == 'h':
                prepend_punct(f, n, '[')
                end_punct = ']'
            # Preced subfields with period.
            if next_sub(f, n) in ['f', 'k', 'l', 'n', 's', 't']:
                end_punct = ''.join([end_punct, '.'])
            # Precede subfields with comma.
            elif next_sub(f, n) in ['m', 'r']:
                end_punct = ''.join([end_punct, ','])
            elif next_sub(f, n) == 'o':
                end_punct = ''.join([end_punct, ';'])
            # Precede subfield p with a period unless it follows
            # subfield p.
            elif next_sub(f, n) == 'p':
                if current_sub(f, n) == 'n':
                    end_punct = ''.join([end_punct, ','])
                else:
                    end_punct = ''.join([end_punct, '.'])
            # Precede volume number with space-semicolon.
            elif next_sub(f, n) == 'v':
                end_punct = ''.join([end_punct, ' ;'])
            # End field with terminal period.
            if n == last_subdata_index(f):
                if not end_punct.endswith('.'):
                    end_punct = ''.join([end_punct, '.'])
            # Add any necessary ending punctuation.
            if end_punct:
                append_punct(f, n, end_punct, exempt = exempt)


def main():
    """Iterates through a MARC file and saves edits"""
    with open('input_mrc/enc.mrc', 'rb') as fh:
        # Open the record and encode as unicode, to prevent errors.
        reader = MARCReader(fh, to_unicode=True, force_utf8=True)
        for record in reader:
            for field in record.fields:
                # Move past control fields, undefined fields, LC/CONSER
                # fields, or fields without punctuation instructions.
                if (field.is_control_field() or field.tag in undefined_fields
                        or field.tag in ['012'] or field.tag in no_instructions):
                    continue
                else:
                    original = field.__str__()
                    punctuate(record, field)
                    if original != field.__str__():
                        with open('output_mrc/changed.txt', 'a') as out:
                            try:
                                out.write(f'original: {original}')
                                out.write(f'changed:  {field}')
                            except UnicodeEncodeError as e:
                                print(f'original: {original}')
                                print(f'changed:  {field}')
                    else:
                        with open('output_mrc/changed.txt', 'a') as out:
                            try:
                                out.write(field.__str__())
                            except UnicodeEncodeError as e:
                                 print(f'unchange: {field.__str__()}')
            # # Write the edited record to a new file
            # with open('output_mrc/015.mrc', 'ab') as out:
            #     out.write(record.as_marc())


if __name__ == '__main__':
    main()
