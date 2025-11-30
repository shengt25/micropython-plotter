"""
Python语法高亮器
使用QSyntaxHighlighter为Python代码提供基础的语法高亮
"""
from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QFont, QColor
from PySide6.QtCore import QRegularExpression


class PythonSyntaxHighlighter(QSyntaxHighlighter):
    """Python语法高亮器"""

    def __init__(self, document):
        super().__init__(document)

        # 定义高亮规则
        self.highlighting_rules = []

        # 关键字格式 (蓝色加粗)
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#0000FF"))
        keyword_format.setFontWeight(QFont.Weight.Bold)

        # Python关键字列表
        keywords = [
            'and', 'as', 'assert', 'break', 'class', 'continue', 'def',
            'del', 'elif', 'else', 'except', 'False', 'finally', 'for',
            'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'None',
            'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'True',
            'try', 'while', 'with', 'yield', 'async', 'await'
        ]

        for word in keywords:
            pattern = QRegularExpression(f'\\b{word}\\b')
            self.highlighting_rules.append((pattern, keyword_format))

        # 内置函数 (深紫色)
        builtin_format = QTextCharFormat()
        builtin_format.setForeground(QColor("#8B008B"))
        builtins = [
            'print', 'len', 'range', 'str', 'int', 'float', 'list', 'dict',
            'set', 'tuple', 'bool', 'type', 'isinstance', 'open', 'abs',
            'min', 'max', 'sum', 'all', 'any', 'enumerate', 'zip'
        ]
        for word in builtins:
            pattern = QRegularExpression(f'\\b{word}\\b')
            self.highlighting_rules.append((pattern, builtin_format))

        # 字符串 (绿色)
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#008000"))
        # 双引号字符串
        self.highlighting_rules.append((
            QRegularExpression('"[^"\\\\]*(\\\\.[^"\\\\]*)*"'),
            string_format
        ))
        # 单引号字符串
        self.highlighting_rules.append((
            QRegularExpression("'[^'\\\\]*(\\\\.[^'\\\\]*)*'"),
            string_format
        ))

        # 注释 (灰色斜体)
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#808080"))
        comment_format.setFontItalic(True)
        self.highlighting_rules.append((
            QRegularExpression('#[^\n]*'),
            comment_format
        ))

        # 数字 (橙色)
        number_format = QTextCharFormat()
        number_format.setForeground(QColor("#FF8C00"))
        self.highlighting_rules.append((
            QRegularExpression('\\b[0-9]+\\.?[0-9]*\\b'),
            number_format
        ))

        # 函数定义 (深蓝色)
        function_format = QTextCharFormat()
        function_format.setForeground(QColor("#00008B"))
        function_format.setFontWeight(QFont.Weight.Bold)
        self.highlighting_rules.append((
            QRegularExpression('\\bdef\\s+([A-Za-z_][A-Za-z0-9_]*)'),
            function_format
        ))

        # 类定义 (深蓝色)
        class_format = QTextCharFormat()
        class_format.setForeground(QColor("#00008B"))
        class_format.setFontWeight(QFont.Weight.Bold)
        self.highlighting_rules.append((
            QRegularExpression('\\bclass\\s+([A-Za-z_][A-Za-z0-9_]*)'),
            class_format
        ))

        # 三引号字符串格式
        self.tri_single_format = QTextCharFormat()
        self.tri_single_format.setForeground(QColor("#008000"))
        self.tri_double_format = QTextCharFormat()
        self.tri_double_format.setForeground(QColor("#008000"))

    def highlightBlock(self, text):
        """对一个文本块应用语法高亮"""
        # 应用基本规则
        for pattern, format in self.highlighting_rules:
            match_iterator = pattern.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(
                    match.capturedStart(),
                    match.capturedLength(),
                    format
                )

        # 处理多行字符串（三引号）
        self.setCurrentBlockState(0)

        # 三重双引号
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

        # 三重单引号
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

