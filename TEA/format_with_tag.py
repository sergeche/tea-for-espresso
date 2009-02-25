'''
Formats the selected text by wrapping it in the passed tag

When called without the second argument, the text will be wrapped in
paragraph tags
'''

import tea_utils as tea

def act(context, tag='p', tagname=None):
    '''
    Required action method
    
    Note the use of extra keyword arguments; if you wish to use extra
    arguments they must be defined as keyword arguments with a 
    sensible default.  See TextActions/Actions.xml for an example of
    how to construct those arguments in XML definition.
    '''
    text, range = tea.get_single_selection(context)
    if text == None:
        return False
    snippet = '#{1:<' + tag + '>#{2:' + text + '}</' + tag + '>}#0'
    # Set the legible tag name
    if tagname == None:
        tagname = tag.capitalize()
    # Insert the text via recipe
    return tea.insert_snippet_over_selection(context, snippet, range,
                                             'Format with ' + tagname)
