"""
Python Syntax Highlighter
Provides basic syntax highlighting for Python code using QSyntaxHighlighter
"""
from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QFont, QColor
from PySide6.QtCore import QRegularExpression
from PySide6.QtWidgets import QApplication


class PythonSyntaxHighlighter(QSyntaxHighlighter):
    """Python Syntax Highlighter"""

    # VS Code Dark+ inspired palette
    _DARK = {
        "keyword":  "#569CD6",  # blue
        "builtin":  "#4EC9B0",  # teal
        "string":   "#CE9178",  # warm orange
        "comment":  "#6A9955",  # muted green
        "number":   "#B5CEA8",  # light green
        "function": "#DCDCAA",  # yellow
        "class":    "#4EC9B0",  # teal
    }

    # Classic light palette (original, slightly adjusted)
    _LIGHT = {
        "keyword":  "#0033B3",  # blue
        "builtin":  "#7B2D8B",  # purple
        "string":   "#067D17",  # green
        "comment":  "#8C8C8C",  # gray
        "number":   "#FF8C00",  # orange
        "function": "#00627A",  # teal
        "class":    "#00627A",  # teal
    }

    def __init__(self, document):
        super().__init__(document)

        app = QApplication.instance()
        is_dark = (
            app is not None
            and app.palette().window().color().lightness() < 128
        )
        c = self._DARK if is_dark else self._LIGHT

        self.highlighting_rules = []

        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor(c["keyword"]))
        keyword_format.setFontWeight(QFont.Weight.Bold)

        keywords = [
            'and', 'as', 'assert', 'break', 'class', 'continue', 'def',
            'del', 'elif', 'else', 'except', 'False', 'finally', 'for',
            'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'None',
            'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'True',
            'try', 'while', 'with', 'yield', 'async', 'await'
        ]
        for word in keywords:
            self.highlighting_rules.append((QRegularExpression(f'\\b{word}\\b'), keyword_format))

        builtin_format = QTextCharFormat()
        builtin_format.setForeground(QColor(c["builtin"]))
        builtins = [
            'print', 'len', 'range', 'str', 'int', 'float', 'list', 'dict',
            'set', 'tuple', 'bool', 'type', 'isinstance', 'open', 'abs',
            'min', 'max', 'sum', 'all', 'any', 'enumerate', 'zip'
        ]
        for word in builtins:
            self.highlighting_rules.append((QRegularExpression(f'\\b{word}\\b'), builtin_format))

        string_format = QTextCharFormat()
        string_format.setForeground(QColor(c["string"]))
        self.highlighting_rules.append((
            QRegularExpression('"[^"\\\\]*(\\\\.[^"\\\\]*)*"'), string_format
        ))
        self.highlighting_rules.append((
            QRegularExpression("'[^'\\\\]*(\\\\.[^'\\\\]*)*'"), string_format
        ))

        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor(c["comment"]))
        comment_format.setFontItalic(True)
        self.highlighting_rules.append((QRegularExpression('#[^\n]*'), comment_format))

        number_format = QTextCharFormat()
        number_format.setForeground(QColor(c["number"]))
        self.highlighting_rules.append((
            QRegularExpression('\\b[0-9]+\\.?[0-9]*\\b'), number_format
        ))

        function_format = QTextCharFormat()
        function_format.setForeground(QColor(c["function"]))
        function_format.setFontWeight(QFont.Weight.Bold)
        self.highlighting_rules.append((
            QRegularExpression('\\bdef\\s+([A-Za-z_][A-Za-z0-9_]*)'), function_format
        ))

        class_format = QTextCharFormat()
        class_format.setForeground(QColor(c["class"]))
        class_format.setFontWeight(QFont.Weight.Bold)
        self.highlighting_rules.append((
            QRegularExpression('\\bclass\\s+([A-Za-z_][A-Za-z0-9_]*)'), class_format
        ))

        self.tri_single_format = QTextCharFormat()
        self.tri_single_format.setForeground(QColor(c["string"]))
        self.tri_double_format = QTextCharFormat()
        self.tri_double_format.setForeground(QColor(c["string"]))

    def highlightBlock(self, text):
        """Apply syntax highlighting to a text block"""
        # Apply basic rules
        for pattern, format in self.highlighting_rules:
            match_iterator = pattern.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(
                    match.capturedStart(),
                    match.capturedLength(),
                    format
                )

        # Handle multi-line strings (triple quotes)
        self.setCurrentBlockState(0)

        # Triple double quotes
        start_index = 0
        if self.previousBlockState() != 1:
            start_index = text.find('"""')

        while start_index >= 0:
            end_index = text.find('"""', start_index + 3)
            if end_index == -1:
                self.setCurrentBlockState(1)
                comment_length = len(text) - start_index
            else:
                comment_length = end_index - start_index + 3

            self.setFormat(start_index, comment_length, self.tri_double_format)
            start_index = text.find('"""', start_index + comment_length)

        # Triple single quotes
        if self.currentBlockState() == 0:
            start_index = 0
            if self.previousBlockState() != 2:
                start_index = text.find("'''")

            while start_index >= 0:
                end_index = text.find("'''", start_index + 3)
                if end_index == -1:
                    self.setCurrentBlockState(2)
                    comment_length = len(text) - start_index
                else:
                    comment_length = end_index - start_index + 3

                self.setFormat(start_index, comment_length, self.tri_single_format)
                start_index = text.find("'''", start_index + comment_length)

