'''Wraps the currently selected text in a snippet'''

import tea_actions as tea

def act(context, first_snippet='', following_snippet='',
        final_append='', undo_name=None):
    '''
    Required action method
    
    Wraps the selected text in a snippet
    
    Support for discontiguous selections will be implemented when recipes
    can support snippets; until then only first_snippet will be used
    '''
    # TODO: change to a loop once snippets in recipes are supported
    # This function will handle the logic of when to use open vs. multi
    text, range = tea.get_single_selection(context)
    if text == None:
        text = ''
    # Only indent the snippet if there aren't multiple lines in the selected text
    if len(text.splitlines()) > 1:
        indent = False
    else:
        indent = True
    snippet = tea.construct_snippet(text, first_snippet + final_append)
    return tea.insert_snippet(context, snippet, indent)
