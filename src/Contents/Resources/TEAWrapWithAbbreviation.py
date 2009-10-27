'''
@author: Sergey Chikuyonok (serge.che@gmail.com)
'''
'''Class that allow TEA to convert between spaces and tabs for indenting'''

import re

from Foundation import *
from AppKit import *
from PyObjCTools import AppHelper
import objc

from TEAforEspresso import TEAforEspresso
import tea_actions as tea

from zencoding import zen_core as zen
from zencoding import html_matcher as html_matcher

class TEAWrapWithAbbreviation(TEAforEspresso):
	'''Class for entabbing and detabbing current document or selection'''
	customSheet = objc.IBOutlet()
	abbr = objc.IBOutlet()
	spinner = objc.IBOutlet()
	
	@objc.signature('B@:@@')
	def performActionWithContext_error_(self, context, error):
		'''
		Gets the user's abbreviation
		'''
		# Load the sheet
		if not self.customSheet:
			NSBundle.loadNibNamed_owner_('TEAEnterAbbreviation', self)
		
		# Set up the default number
#		prefs = tea.get_prefs(context)
#		num_spaces = prefs.numberOfSpacesForTab()
#		self.abbr.setStringValue_(num_spaces)
		
		NSApp.beginSheet_modalForWindow_modalDelegate_didEndSelector_contextInfo_(
			self.customSheet,
			context.windowForSheet(),
			self,
			'didEndSheet:returnCode:contextInfo:',
			None
		)
		# Save the context for later reference (once the sheet is complete)
		self.context = context
		# Because this gets passed through to Obj-C, using int prevents beeping
		return True
	
	@objc.IBAction
	def doSubmitSheet_(self, sender):
		NSApp.endSheet_returnCode_(self.customSheet, 1)
	
	@objc.IBAction
	def cancel_(self, sender):
		NSApp.endSheet_returnCode_(self.customSheet, 0)
	
	@AppHelper.endSheetMethod
	def didEndSheet_returnCode_contextInfo_(self, sheet, code, info):
		def replacements(match):
			'''Utility function for replacing items'''
			return match.group(0).replace(self.search, self.replace)
		
		if code == 1:
			# Leave sheet open with "processing" spinner
			self.spinner.startAnimation_(self)
			wrap(self.context, self.abbr.stringValue())
			self.spinner.stopAnimation_(self)
		
		sheet.orderOut_(self)
		
def wrap(context, abbr, profile_name='xhtml'):
	ranges = tea.get_ranges(context)
	rng = ranges[0]
	cursor = rng.location + rng.length
	range_start, range_end = rng.location, rng.location + rng.length
	content = context.string()
	
	zen.newline = tea.get_line_ending(context)
	
	if not abbr:
		return False
	
	tea.log('abbr is %s' % abbr)
	if range_start == range_end:
		# no selection, find tag pair
		start, end = html_matcher.match(content, cursor)
		if start is None:
			# nothing to wrap
			return False
		
		last = html_matcher.last_match
		range_start = last['opening_tag'].start
		range_end = last['closing_tag'] and last['closing_tag'].end or last['opening_tag'].end
		
	content = content[range_start:range_end]
	
	# Detect the type of document we're working with
	zones = {
		'css, css *': 'css',
		'xsl, xsl *': 'xsl',
		'xml, xml *': 'xml'
	}
	doc_type = tea.select_from_zones(context, rng, 'html', **zones)
	result = zen.wrap_with_abbreviation(abbr, content, doc_type, profile_name)
	
	
	if result:
		tea.log('set new range')
		tea.set_selected_range(context, tea.new_range(range_end, 0))
		
		tea.log('replace content')
		replace_editor_content(context, content, result)
		return True
	
	return False

def replace_editor_content(context, editor_str, content):
	"""
	Replaces current editor's substring with new content. Multiline content
	will be automatically padded
	 
	@param {String} editor_str Current editor's substring
	@param {String} content New content
	"""
	if not content:
		return
		
	# set newlines according to editor's settings
	content = content.replace(r'\n', zen.get_newline())
	
	# add padding for current line
	content = zen.pad_string(content, get_current_line_padding(context)) 
	
	# get char index where we need to place cursor
	rng = tea.get_ranges(context)[0]
	start_pos = rng.location - len(editor_str)
	cursor_pos = content.find('|')
	content = content.replace('|', '')
	
	# replace content in editor
	tea.insert_text_over_range(context, content, tea.new_range(start_pos, len(editor_str)), 'Wrap with Abbreviation')
	
	# place cursor
	if cursor_pos != -1:
		tea.set_selected_range(context, tea.new_range(start_pos + cursor_pos, 0))


def get_current_line_padding(context):
	"""
	Returns padding of current editor's line
	@return str
	"""
	line, r = tea.get_line(context, tea.get_ranges(context)[0])
	m = re.match(r'^(\s+)', str(line))
	return m and m.group(0) or ''
		
	
def unindent(context, text):
	"""
	Unindent content, thus preparing text for tag wrapping
	@param text: str
	@return str
	"""
	pad = get_current_line_padding(context)
	lines = zen.split_by_lines(text)
	
	for i,line in enumerate(lines):
		if line.search(pad) == 0:
			lines[i] = line[len(pad):]
			
	
	return zen.get_newline().join(lines)