import re

def clean_headfoot(before):
    junk = [
        r'^[A-Z0-9., ]+\s\n?', # header
        r'\n\d+\n\n',          # page numbers
        r'(\d+)?\n?.*\n\n?$' ] # footer
    after = before
    for regex in junk:
        after =  re.sub(regex, '', after)
    return after

