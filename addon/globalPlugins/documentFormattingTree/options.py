try:
	import addonHandler

	addonHandler.initTranslation()
except Exception:
	_ = lambda text: text


class Option:
	def __init__(
		self, label: str, key: str, choices=None, values=None, minimum: int | None = None, maximum: int | None = None
	):
		self.label = label
		self.key = key
		self.choices = choices or []
		self.values = values or []
		self.minimum = minimum
		self.maximum = maximum


class Category:
	def __init__(self, label: str, boolOptions=(), choiceOptions=(), spinOptions=()):
		self.label = label
		self.boolOptions = list(boolOptions)
		self.choiceOptions = list(choiceOptions)
		self.spinOptions = list(spinOptions)


def buildCategories() -> list[Category]:
	return [
		Category(
			_("Font"),
			[
				Option(_("Font name"), "reportFontName"),
				Option(_("Font size"), "reportFontSize"),
				Option(_("Superscripts and subscripts"), "reportSuperscriptsAndSubscripts"),
				Option(_("Emphasis"), "reportEmphasis"),
				Option(_("Highlighted text"), "reportHighlight"),
				Option(_("Style"), "reportStyle"),
				Option(_("Color"), "reportColor"),
			],
			[
				Option(
					_("Font attributes"),
					"fontAttributeReporting",
					[_("Off"), _("Speech"), _("Braille"), _("Speech and braille")],
					[0, 1, 2, 3],
				),
			],
		),
		Category(
			_("Document information"),
			[
				Option(_("Comments"), "reportComments"),
				Option(_("Bookmarks"), "reportBookmarks"),
				Option(_("Editor revisions"), "reportRevisions"),
			],
			[
				Option(
					_("Spelling or grammar errors"),
					"reportSpellingErrors2",
					[_("Speech"), _("Sound"), _("Braille")],
					[1, 2, 4],
				),
			],
		),
		Category(
			_("Pages and spacing"),
			[
				Option(_("Pages"), "reportPage"),
				Option(_("Line numbers"), "reportLineNumber"),
				Option(_("Ignore blank lines for line indentation reporting"), "ignoreBlankLinesForRLI"),
				Option(_("Paragraph indentation"), "reportParagraphIndentation"),
				Option(_("Line spacing"), "reportLineSpacing"),
				Option(_("Alignment"), "reportAlignment"),
			],
			[
				Option(
					_("Line indentation reporting"),
					"reportLineIndentation",
					[_("Off"), _("Speech"), _("Tones"), _("Speech and tones")],
					[0, 1, 2, 3],
				),
			],
			[
				Option(_("Indent tone duration (ms)"), "indentToneDuration", minimum=10, maximum=2000),
			],
		),
		Category(
			_("Table information"),
			[
				Option(_("Tables"), "reportTables"),
				Option(_("Cell coordinates"), "reportTableCellCoords"),
			],
			[
				Option(
					_("Headers"),
					"reportTableHeaders",
					[_("Off"), _("Rows and columns"), _("Rows"), _("Columns")],
					[0, 1, 2, 3],
				),
				Option(_("Cell borders"), "reportCellBorders", [_("Off"), _("Style"), _("Color and style")], [0, 1, 2]),
			],
		),
		Category(
			_("Elements"),
			[
				Option(_("Headings"), "reportHeadings"),
				Option(_("Links"), "reportLinks"),
				Option(_("Link type"), "reportLinkType"),
				Option(_("Graphics"), "reportGraphics"),
				Option(_("Lists"), "reportLists"),
				Option(_("Block quotes"), "reportBlockQuotes"),
				Option(_("Groupings"), "reportGroupings"),
				Option(_("Landmarks and regions"), "reportLandmarks"),
				Option(_("Articles"), "reportArticles"),
				Option(_("Frames"), "reportFrames"),
				Option(_("Figures and captions"), "reportFigures"),
				Option(_("Clickable"), "reportClickable"),
				Option(_("Report formatting changes after the cursor (can cause a lag)"), "detectFormatAfterCursor"),
			],
		),
	]
