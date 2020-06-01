#!/usr/bin/python

import sys

def parse_sexp(toc_input, toc_output, indent_str, i):
    """
    Translate TOC in the s-exp format output by ``djvused`` to a
    format understood by ``pdfbeads``.

    ``toc_input[i:]`` is the string to parse, and ``indent_str`` is
    the string of tabulations for our current level in the output
    TOC. The output from ``djvused`` should not include the
    '(bookmarks' prefix. Anything up until the opening brace is
    disregarded, as well as anything after its matching closing brace.

    If the input is badly formatted, weird things will happen.
    """

    while True:

        if toc_input[i] == '(':
            i += 1
            i, title = next_quote(toc_input, i)
            i, page  = next_quote(toc_input, i)

            # `djvused` outputs page numbers prefixed with '#' (the
            # second character of the `page` variable) which we don't
            # want in our output
            page = page[0]+page[2:]

            toc_output += ["{0}{1} {2}".format(indent_str, title, page)]

            i = parse_sexp(toc_input, toc_output, indent_str+'\t', i)

        elif toc_input[i] == ')':
            return i+1

        i += 1

def next_quote(str, i):
    """
    Finds the next substring ``str[k:j]`` of ``str[i:]`` enclosed by
    non-escaped double-quotes and returns the tuple ``j, res`` where
    ``res`` is ``str[k:j]`` with escaped double-quotes replaced by
    single-quotes.
    """

    # Find the opening quote. This is simple because we can safely
    # assume there is only whitespace in between
    j = i
    while str[j] != '"':
        j += 1
    i = j
    j += 1
    output = ['"']

    # Find the closing quote. This is a bit more involved because the
    # output may include escaped double quotes, which `pdfbeads`
    # cannot handle correctly. To circumvent this bug, we replace
    # every escaped double quote inside the literal with a single quote.
    while True:
        if str[j] == '"':
            if str[j-1] == "\\":
                output.pop()
                output += ["'"]
            else:
                output += [str[j]]
                break
        else:
            output += [str[j]]
        j += 1

    return j+1, ''.join(output)

if __name__ == '__main__':
    toc_input = sys.stdin.read()

    # It's possible that the file does not have a table of contents,
    # in which case we won't read anything at all
    if len(toc_input) > 0:
        # We must skip the '(bookmarks' prefix as it doesn't fit the
        # general pattern expected by `parse_sexp`.
        toc_output = []
        parse_sexp(toc_input[1:], toc_output, '', 0)
        print('\n'.join(toc_output))
