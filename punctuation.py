from pymarc import MARCReader
from helpers import *

# The ASCII and ANSEL punctuation marks, plus the Euro sign
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


def main():
    with open('input_mrc/enc.mrc', 'rb') as fh:
        # Open the record and encode as unicode, to prevent errors.
        reader = MARCReader(fh, to_unicode=True, force_utf8=True)
        for record in reader:
            for num, f in enumerate(record.fields):
                original = f.__str__()
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
                        if n % 2 != 0 and f.subfields[n-1] == 'q':
                            # Begin qualifying data with a parenthesis.
                            if n == 1 or f.subfields[n-3] != 'q':
                                prepend_punct(f, n, '(')
                            # Separate subfields q with space-
                            # semicolon.
                            if (n == last_subdata_index(f)
                                    or f.subfields[n+1] != 'q'):
                                end_punct = ''.join([end_punct, ')'])
                            elif f.subfields[n+1] == 'q':
                                    end_punct = ''.join([end_punct, ' ;'])
                        # Precede subfield c with space-colon.
                        if (n < last_subdata_index(f)
                                and f.subfields[n+1] == 'c'):
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
                        if n % 2 != 0 and f.subfields[n-1] == 'q':
                            # Begin qualifying data with a parenthesis.
                            if n == 1 or f.subfields[n-3] != 'q':
                                prepend_punct(f, n, '(')
                            # Separate subfields q with space-
                            # semicolon.
                            if (n == last_subdata_index(f)
                                    or f.subfields[n+1] != 'q'):
                                end_punct = ''.join([end_punct, ')'])
                            elif f.subfields[n+1] == 'q':
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
                    for n, sub in enumerate(field.subfields):
                        if sub == 'a' and n % 2 == 0:
                            data = field.subfields[n+1].replace(') ', ')')
                            field.subfields[n+1] = data
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
                # if original != f.__str__():
                #     print(f'original: {original}')
                #     print(f'changed: {f}')
                if f.tag == '043':
                    if len(f['a']) != 7 or f['b']:
                        print(f)
            #     if f.tag in ['010', '016', '017', '019', '022',
            #                  '024', '025', '026', '030', '038', '040', '041',
            #                  '042', '044', '046', '047', '048', '052', '082',
            #                  '083', '085', '088', '092']:
            #         del_terminal_punct(f, abbrev_exempt=False)
            #     # No terminal punctuation, unless ending in an
            #     # abbreviation
            #     if f.tag in ['032', '034', '050', '066', '070', '071', '072',
            #                  '090', '246',
            #                  '490']:
            #         del_terminal_punct(f)
            #     # Omit any punctuation from the end of the field unless
            #     # it ends with an ellipsis, hyphen, closing
            #     # parenthesis, exclamation point, question mark, or
            #     # period following an abbreviation
            #     if f.tag in ['015', '020', '027', '028']:
            #         del_terminal_punct(f,
            #                            exempt=['...', '-', ')', '!', '?'])
            #     # Enclose data in $q in parentheses, separating each
            #     # subfield with a semicolon
            #     if f.tag in ['015', '027', '028']:
            #         enclose_subs(f, 'q', '(', ' ;', ')')
            #     # Remove any parentheses enclosing $a or $z
            #     if f.tag in ['015']:
            #         for n, sub in f.subfields:
            #             if sub in ['a', 'z'] and n % 2 == 0:
            #                 del_from_start(f, n+1, del_list=['('])
            #                 del_from_end(f, n+1, del_list=[')'])
            #     # Add periods to fields that end in a mark of
            #     # punctuation
            #     if f.tag in ['036', '240', '243']:
            #         add_terminal_punct(f, exempt_punct=['?', '!', '-'])
            #     # Field 037 does not end in a punctuation mark, but
            #     # subfield data often does
            #     if f.tag in ['037']:
            #         del_terminal_punct(f, exempt=['.', ')', ']'])
            #     # Does not end in a period unless the period is part of
            #     # the data
            #     if f.tag in ['060', '061', '096']:
            #         del_terminal_punct(f, exempt=['.'])
            #     # For serially-issued resources with U.S. SuDoc
            #     # classification, the number may end in a / or :
            #     if f.tag in ['086']:
            #         del_terminal_punct(f, exempt=[':', '/'])
            #     # Personal name fields
            #     if f.tag in ['017', '018']:
            #         del_terminal_punct(f,
            #                            exempt=['.',	'?', '!', '-'])
            #     # Field 031 does not get terminal punctuation, but
            #     # ?, +, and ! are coded information
            #     if f.tag in ['031']:
            #         del_terminal_punct(f,
            #                            exempt=['?', '+', '!'])
            #     # No terminal punctuation added, but subfields may end
            #     # in an abbreviation, paranthesis or hyphen
            #     if f.tag in ['033']:
            #         if last_subcode(f) == 'a':
            #             exempt=['-']
            #             abbrev_exempt=False
            #         elif last_subcode(f) == 'p':
            #             exempt=[')']
            #             abbrev_exempt=True
            #         else:
            #             exempt=['']
            #             abbrev_exempt=False
            #         del_terminal_punct(f, exempt=exempt,
            #                            abbrev_exempt=abbrev_exempt)
            #     # Field usually ends in trailing hyphens
            #     if f.tag in ['043', '045']:
            #         del_terminal_punct(f, exempt=['-'])
            #     # Subfield d is enclosed in brackets
            #     if f.tag in ['049']:
            #         enclose_subs(f, 'd', '[', '', ']')
            #     if f.tag in ['051', '070', '222']:
            #         add_terminal_punct(f)
            #     if f.tag in ['055']:
            #         del_terminal_punct(f, exempt=['*'])
            #     # Field sometimes ends in qualifying information
            #     if f.tag in ['074', '080', '084']:
            #         del_terminal_punct(f, exempt=[')'])
            #     if f.tag in ['082']:
            #         del_terminal_punct(f, exempt=['/', ':'])
            #     if f.tag in ['015']:
            #         for n, sub in enumerate(f.subfields):
            #             if (sub == 'a' or sub == 'z') and n % 2 == 0:
            #                 del_from_end(f, n+1, del_list=[')'])
            #                 del_from_start(f, n+1, del_list=['('])
            #     if f.tag in ['020', '024']:
            #         for n, sub in enumerate(f.subfields):
            #             if sub == 'q' and n % 2 == 0:
            #                 if f.subfields[n-2] != 'q':
            #                     prepend_punct(f, n+1, '(')
            #                 # Check if the f has a next subfield
            #                 if len(f.subfields) > n+2:
            #                     if f.subfields[n+2] == 'c':
            #                         append_punct(f, n+1, ') :')
            #                     elif f.subfields[n+2] == 'q':
            #                         append_punct(f, n+1, ' ;')
            #                     else:
            #                         append_punct(f, n+1, ')')
            #                 else:
            #                     append_punct(f, n+1, ')')
            #             if sub == 'c' and n > 0 and n % 2 == 0:
            #                 append_punct(f, n-1, ' :')
            #     # Follow a fingerprint date with a period
            #     if f.tag in ['026']:
            #         for n, sub in enumerate(f.subfields):
            #             if sub == 'c' and n % 2 == 0:
            #                 append_punct(f, n+1, '.')
            #     # Period that usually precedes a Cutter number is
            #     # omitted in subfield $c.
            #     if f.tag in ['033']:
            #         for n, sub in enumerate(f.subfields):
            #             if sub == 'c' and n % 2 == 0:
            #                 del_from_start(f, n+1, del_list=['.'])
            #     if f.tag in ['035']:
            #         for n, sub in enumerate(f.subfields):
            #             if sub in ['a', 'z'] and n % 2 == 0:
            #                 append_punct(f, n+1, '(')
            #     # Personal names
            #     if f.tag in ['100', '600', '696', '700', '790', '796', '800',
            #                  '896']:
            #         for n, sub in f.subfields:
            #             # Preced titles and terms of address with a ,
            #             if sub == 'c' and n % 2 == 0:
            #                 if f.subfields[n+1][0] != '(':
            #                     append_punct(f, n-1, ',', exempt=['"'])
            #             # Enclose fuller form of name in parentheses,
            #             # without putting any preceding punctuation
            #             # for the next subfield in parentheses
            #             if sub == 'q' and n % 2 == 0:
            #                 prepend_punct(f, n+1, '(')
            #                 if f.subfields[n+2] in 'dej':
            #                     append_punct(f, n+1, '),')
            #                 elif f.subfields[n+2] in 'fklpt':
            #                     append_punct(f, n+1, ').')
            #                 elif f.subfields[n+2] in 'g':
            #                     append_punct(f, n+1, ') :')
            #                 else:
            #                     append_punct(f, n+1, ')')
            #         # Precede dates and attribution qualifiers with a
            #         # comma
            #         precede_sub(f, 'd', ',', exempt=['"'])
            #         precede_sub(f, 'j', ',', exempt=['"'])
            #         # Precede miscellaneous info with a colon
            #         precede_sub(f, 'g', ' :')
            #         # Punctuation preceding n is determined by type of work
            #         # No punctuation precedes affiliation
            #         del_pre_punct(f, subfields=['u'], exempt=[')'],
            #                       abbrev_exempt=True)
            #         # punctuation unless the field ends with an
            #         # abbreviation, an initialism, or data that ends with a
            #         # mark of punctuation
            #         add_terminal_punct(f, exempt_punct=['...', '-', ')', '!',
            #                                             '?'])
            #     if f.tag in ['100', '110']:
            #         # Precede the name of a part of a work with a
            #         # period, unless following the number of the part
            #         if sub == 'p' and n % 2 == 0:
            #             if f.subfields[n-2] == 'n':
            #                 append_punct(f, n-1, ',', exempt=['"'])
            #             else:
            #                 append_punct(f, n-1, '.', exempt=['"'])
            #         # Relator terms are preceded by a comma unless
            #         # following an open date
            #         precede_sub(f, 'e', ',', exempt=['"', '-'])
            #         # Preced date, forms, languages, and titles of
            #         # works with a period
            #         precede_sub(f, 'f', '.', exempt=['"'])
            #         precede_sub(f, 'k', '.', exempt=['"'])
            #         precede_sub(f, 'l', '.', exempt=['"'])
            #         precede_sub(f, 't', '.')
            #     # Corporate names
            #     if f.tag in ['110', '610', '697', '710', '791', '797', '810',
            #                  '897']:
            #         for n, sub in enumerate(f.subfields):
            #             # Enclose disambiguating information in
            #             # parenthese, and separate each subfield with
            #             # a space-colon
            #             if sub in ['d', 'g', 'n'] and n % 2 == 0:
            #                 if f.subfields[n-2] in ['c', 'd', 'g', 'n']:
            #                     append_punct(f, n-1, ' :')
            #                 else:
            #                     prepend_punct(f, n, '(')
            #             # Separate each location with a semicolon
            #             elif sub == 'c' and n % 2 == 0:
            #                 if f.subfields[n-2] in ['d', 'g', 'n']:
            #                     append_punct(f, n-1, ' :')
            #                 elif f.subfields[n-2] == 'c':
            #                     append_punct(f, n-1, ';')
            #                 else:
            #                     prepend_punct(f, n+1, '(')
            #             # Subject subdivisions have no preceding
            #             # punctuation
            #             elif sub in ['v', 'x', 'y', 'z'] and n % 2 == 0:
            #                 del_from_end(f, n-1, exempt=[')'],
            #                              abbrev_exempt=True)
            #         # Precede each subordinate unit with a period
            #         precede_sub(f, 'b', '.', exempt=['"'])
            #         # No punctuation precedes affiliation or subject
            #         # subdivisions
            #         del_pre_punct(f, subfields=['u', 'v', 'x', 'y', 'z'],
            #                       exempt=[')'], abbrev_exempt=True)
            # if f.tag in ['110']:
            #     # No punctuation separates form and part
            #     for n, sub in f.subfields:
            #         if sub == 'p' and n % 2 == 0 and f.subfields[n-2] == 'k':
            #             del_from_end(f, n-1, abbrev_exempt=True)
            # if f.tag in ['110', '111']:
            #     end_punct = ''
            #     start_punct = ''
            #     for n, sub in f.subfields:
            #         if f.subfields[n-1] in ['c', 'd', 'n'] and n % 2 != 0:
            #             # Separate c subfields with space-semicolon
            #             if f.subfields[n-1] == 'c' and f.subfields[n+1] == 'c':
            #                 end_punct = ';'
            #             # Close qualifying subfields off from following
            #             # subfields
            #             elif (n == len(f.subfields)-1
            #                     or f.subfields[n+1] not in ['c', 'd', 'n']):
            #                 end_punct = ')'
            #             # Separate with space-colon
            #             else:
            #                 end_punct = ' :'
            #             # Close qualifying subfields off from preceding
            #             # subfields
            #             if f.subfields[n-3] not in ['c', 'd', 'n']:
            #                 start_punct = '('
            #         # Precede subfields with period
            #         if f.subfields[n+1] in ['e', 'f', 'k', 'l'] and n % 2 != 0:
            #             end_punct = ''.join([end_punct, '.'])
            #         # Precede subfields with comma
            #         elif f.subfields[n+1] in ['g', 'j'] and n % 2 != 0:
            #             end_punct = ''.join([end_punct, ','])
            #         # Add the punctuation
            #         if end_punct:
            #             append_punct(f, n, end_punct)
            #         if start_punct:
            #             prepend_punct(f, n, start_punct)

                # Enclose disambiguating information in
                # parenthese, and separate each subfield with
                # a space-colon
                # if sub in ['d', 'g', 'n'] and n % 2 == 0:
                #     if f.subfields[n-2] in ['c', 'd', 'g', 'n']:
                #         append_punct(f, n-1, ' :')
                #     else:
                #         prepend_punct(f, n, '(')
                # Separate each location with a semicolon
                # elif sub == 'c' and n % 2 == 0:
                #     if f.subfields[n-2] in ['d', 'g', 'n']:
                #         append_punct(f, n-1, ' :')
                #     elif f.subfields[n-2] == 'c':
                #         append_punct(f, n-1, ';')
                #     else:
                #         prepend_punct(f, n+1, '(')
                # Subject subdivisions have no preceding
                # punctuation
                # elif sub in ['v', 'x', 'y', 'z'] and n % 2 == 0:
                #     del_from_end(f, n-1, exempt=[')'],
                #                  abbrev_exempt=True)
            # # Write the edited record to a new file
            # with open('output_mrc/015.mrc', 'ab') as out:
            #     out.write(record.as_marc())

if __name__ == '__main__':
    main()
