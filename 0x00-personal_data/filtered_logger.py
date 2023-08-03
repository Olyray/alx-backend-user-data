#!/usr/bin/env python3
"""A module for a filtered logger"""


import re
from typing import List
import logging

patterns = {
    'extract': lambda x, y: r'(?P<field>{})=[^{}]*'.format('|'.join(x), y),
    'replace': lambda x: r'\g<field>={}'.format(x),
}


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str
        ) -> str:
    """The function to obfuscate the log"""
    extract, replace = (patterns['extract'], patterns['replace'])
    return re.sub(extract(fields, separator), replace(redaction), message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initializing the class"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Obfuscating the log record"""
        message = super().format(record)
        return filter_datum(
            self.fields, self.REDACTION, message, self.SEPARATOR
            )
