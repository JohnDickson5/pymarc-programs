from pymarc import MARCReader
from helpers import *

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

abbrev_list = []
not_abbrev_list = []


# def edit_242(record, index, pre_punct):
#     """Mirror changes in preceding punctuation made to the 245 in
#     every 242
#     """
#     for f in record:
#         if f.tag == '242':
#             # Check that the subf at the index is followed by
#             # another subfield
#             if len(f.subfields) >= index + 2:
#                 sub = f.subfields[index]
#                 next_sub = f.subfields[index+2]
#                 if not sub.endswith(prepunct):
#                     # Remove partial punctuation from end of sub
#                     while sub[-1] in pre_punct:
#                         sub = sub[:-1]
#                     # Remove any part of the punctuation that was
#                     # entered in the next sub
#                     while next_sub[0] in pre_punct + ' ':
#                         next_sub = next_sub[1:]
#                     sub = sub + punctuation
#                     f.subfields[index] = sub
#                     f.subfields[index+2] = next_sub


# def pre_punct_245b(record, f):
#     """Adds preceding punctuation before 245 subf b when it is
#     possible to determine that it begins with a parallel title or
#     title of another work contained in the resource
#     """
#     i = 0
#     dict245 = {}
#     for n, sub in enumerate(f.subfields):
#         subs242 = 'abchnp'
#         if sub in 'subs242' or f.subfields[n-1] in subs242:
#             dict245[i] = sub
#             i += i
#         if sub == 'b':
#             data = f.subfields[n+1] # Data in subf b
#             prev = f.subfields[n-1] # The previous subfield
#             # Before checking for punctuation, check that the
#             # subf is long enough to contain it, in order
#             # to avoid index errors
#             if len(prev) > 2:
#                 pre_punct = [' :', ' =', ' ;']
#                 if (prev[-2:] not in pre_punct \
#                         and not prev.endswith('.'):
#                     varying_titles = record.get_fields('246')
#                     for vt in varying_titles:
#                         if vt.indicator2 == '1':
#                             parallel = vt['a'].lower()
#                             # For the purpose of searching,
#                             # remove any punctuation at the end
#                             # of the 246$a
#                             while (parallel[-1] in punct
#                                     or parallel[-1] in ' .'):
#                                 parallel = parallel[:-1]
#                             while data[0] in ' =':
#                                 data = data[1:]
#                             # If any change was made, update the field
#                             if data != f.subfields[n+1]:
#                                 f.subfields[n+1] = data
#                             if data.lower().find(parallel) == 0:
#                                 # Remove any misentered
#                                 # preceding punctuation
#                                 while prev[-1] in ' =':
#                                     prev = prev[:-1]
#                                 f.subfields[n-1] = prev + ' ='
#                                 edit_242(record, i-1, ' =')
#                             elif data.lower().find(parallel) > 0:
#                                 parallel_pos = data.lower().find(parallel)
#                     # Look for titles in added entries
#                     added_entries = record.get_fields('700', '710', '711')
#                     for entry in added_entries:
#                         same_author = ''
#                         diff_author = ''
#                         if entry.tag == '700' and entry.indicator2 == '2':
#                             if record['100']:
#                                 if record['100']['a'] == entry['a']:
#                                     same_author = entry['t'].lower()
#                             elif saw['t']:
#                                 diff_author = entry['t'].lower()
#                         if entry.tag == '710' and entry.indicator2 == '2':
#                             if record['110']:
#                                 if record['110']['a'] == entry['a']:
#                                     same_author = entry['t'].lower()
#                             elif saw['t']:
#                                 diff_author = entry['t'].lower()
#                         if entry.tag == '711' and entry.indicator2 == '2':
#                             if record['111']:
#                                 if record['111']['a'] == entry['a']:
#                                     same_author = entry['t'].lower()
#                             elif saw['t']:
#                                 diff_author = entry['t'].lower()
#                         if same_author:
#                             while data[0] in ' ;':
#                                 data = data[1:]
#                             if data != f.subfields[n+1]:
#                                 f.subfields[n+1] = data
#                             while same_author[-1] in punct + '.':
#                                 same_author = same_author[:-1]
#                             if data.lower().find(same_author) == 0:
#                                 while prev[-1] in ' ;':
#                                     prev = prev[:-1]
#                                 f.subfields[n-1] = prev + ' ;'
#                                 edit_242(record, i-1, ' ;')
#                         if diff_author:
#                             while data[0] in ' .':
#                                 data = data[1:]
#                             if f.subfields[n+1] != data:
#                                 f.subfields[n+1] = data
#                             while diff_author[-1] in punct + '.':
#                                 diff_author = diff_author[:-1]
#                             if data.lower().find(diff_author) == 0:
#                                 while prev[-1] in ' .':
#                                     prev = prev[:-1]
#                                 f.subfields[n-1] = prev + '.'
#                                 edit_242(record, i-1, '.')
#                     uniform_titles = record.get_fields('730')
#                     for ut in uniform_titles:
#                         ut = ut['a'].lower()
#                         while ut[-1] in punct or ut[-1]:
#                             ut = ut[:-1]
#                         while data[0] == '.':
#                             data = data[1:]
#                         if f.subfields[n+1] != data:
#                             f.subfields[n+1] = data
#                         if data.lower().find(ut) == 0:
#                             f.subfields[n-1] = prev[n-1] + "."
#                             edit_242(record, i-1, '.')
#             else:
#                 print("Short sub: " + f)


def main():
    with open('input_mrc/enc.mrc', 'rb') as fh:
        # Open the record and encode as unicode, to prevent errors
        reader = MARCReader(fh, to_unicode=True, force_utf8=True)
        for record in reader:
            for num, f in enumerate(record.fields):
                if f.tag in ['036']:
                    add_terminal_punct(f, exempt_punct=['?', '!', '-'])
                if f.tag in ['010', '024', '025']:
                    del_terminal_punct(f, abbrev_exempt=False)
                if f.tag in ['015', '020', '027', '028']:
                    del_terminal_punct(f,
                                       exempt=['...', '-', ')', '!', '?'])
                if f.tag in ['017', '018']:
                    del_terminal_punct(f,
                                       exempt=['.',	'?', '!', '-'])
                if f.tag in ['031']:
                    del_terminal_punct(f,
                                       exempt=['?', '+', '!'])
                if f.tag in ['032', '034']:
                    del_terminal_punct(f)
                if f.tag in ['037']:
                    if f.subfields[last_subcode_index(f)] == 'c':
                        del_terminal_punct(f, exempt_punct=[')'])
                    else:
                        del_terminal_punct(f, exempt_punct=['?', '!', '-'])
                if f.tag in ['015']:
                    for n, sub in enumerate(f.subfields):
                        if (sub == 'a' or sub == 'z') and n % 2 == 0:
                            del_from_end(f, n+1, del_list=[')'])
                            del_from_start(f, n+1, del_list=['('])
                if f.tag in ['015', '027', '028']:
                    enclose_subs(f, 'q', '(', ';', ')')
                if f.tag in ['020', '024']:
                    for n, sub in enumerate(f.subfields):
                        if sub == 'q' and n % 2 == 0:
                            if f.subfields[n-2] != 'q':
                                prepend_punct(f, n+1, '(')
                            # Check if the f has a next subfield
                            if len(f.subfields) > n+2:
                                if f.subfields[n+2] == 'c':
                                    append_punct(f, n+1, ') :')
                                elif f.subfields[n+2] == 'q':
                                    append_punct(f, n+1, ' ;')
                                else:
                                    append_punct(f, n+1, ')')
                            else:
                                append_punct(f, n+1, ')')
                        if sub == 'c' and n > 0 and n % 2 == 0:
                            append_punct(f, n-1, ' :')
                        if f.__str__().endswith(tuple([':', ":)"])):
                            with open('output_mrc/020test.txt', 'a') as out:
                                try:
                                    out.write(record.__str__())
                                except UnicodeEncodeError as e:
                                    pass
                # if (f.tag in ['015', '020', '024', '027', '028']
                #         or f.tag in linking_entry_fields):
                #     del_terminal_punct(f, exempt=['...', ')', '!', '?'],
                #                        abbrev_exempt=True)
                # if f.tag in ['210', '222']:
                #     enclose_subs(f, 'b', '(', '', ')')
                # if f.tag in ['100', '600', '700', '800']:
                #     add_terminal_period(f)
                # if f.tag in ['210', '222', '251', '270', '340', '341',
                #                  '342', '355', '357', '363', '365', '366',
                #                  '377', '380', '381', '382', '384', '385',
                #                  '386', '388', '938', '956', '987']:
                #     # remove_pre_punct(f, "!-?]}>)")
                #     del_terminal_punct(f, del_list=['.'])
                # if f.tag == '242':
                #     remove_all_punct(f, 'y')
                #     control_subs.append('y')
                #     add_terminal_period(f)
                #     control_subs.remove('y')
                # if f.tag == '242' or f.tag == '245':
                #     add_pre_punct(f, 'c', ' /')
                #     add_pre_punct(f, 'n', '.', '...!-?')
                #     # Enumerate subfields to determine if any $p
                #     # follows a $n
                #     for n, sub in enumerate(f.subfields):
                #         if sub == 'p':
                #             prev = f.subfields[n-1]
                #             while prev.endswith(' '):
                #                 prev = prev[:-1]
                #             # If the previous subf is n, make sure
                #             # it ends in a comma
                #             if f.subfields[n-2] == 'n':
                #                 if not prev.endswith(','):
                #                     prev = prev + ','
                #             # Otherwise, make sure the previous
                #             # subf ends in an ellipsis,
                #             # exclamation, hyphen, question mark, or
                #             # period
                #             elif prev[-1] not in '.!-?':
                #                 # If not, add period
                #                 prev = prev + '.'
                #             # Update the subf if it has been changed
                #             if f.subfields[n-1] != prev:
                #                 f.subfields[n-1] = prev
                # if f.tag == '245':
                #     # add_pre_punct(f, 'f', ',')
                #     enclose_subs(f, 'g', '(', '', ')')
                #     if f['a']:
                #         add_pre_punct(f, 'k', ' :')
                #     # subf p following a subf n vs. not
                #     add_pre_punct(f, 's', '.', '...!-?')
                #     pre_punct_245b(record, f)
                # list4 = ['245', '250', '254', '255', '256', '343', '351',
                #          '352']
                # if f.tag in list4:
                #     add_terminal_period(f)
                # if f.tag == '246':
                #     remove_terminal_punct(f)
                # if f.tag == '300':
                #     add_pre_punct(field, 'b', ' :')
            # # Write the edited record to a new file
            # with open('output_mrc/242.mrc', 'ab') as out:
            #     out.write(record.as_marc())

if __name__ == '__main__':
    main()
