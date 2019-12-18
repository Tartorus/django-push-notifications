import re
from decimal import Decimal

from django import forms
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _


__all__ = ["HexaDecimalField", "HexaDecimalField"]

hex_re = re.compile(r"^(([0-9A-f])|(0x[0-9A-f]))+$")
signed_integer_engines = [
	"django.db.backends.postgresql",
	"django.db.backends.postgresql_psycopg2",
	"django.contrib.gis.db.backends.postgis",
	"django.db.backends.sqlite3"
]


def _hex_string_to_decimal(value):
	return Decimal(int(value, 16))


def _decimal_to_hex(value):
	if value is not None:
		value = str(hex(int(value))).replace('0x', '')
	return value


class HexaDecimalField(forms.CharField):
	"""
	A form field that accepts only hexadecimal numbers
	"""
	def __init__(self, *args, **kwargs):
		self.default_validators = [
			RegexValidator(hex_re, _("Enter a valid hexadecimal number"), "invalid")
		]
		super(HexaDecimalField, self).__init__(*args, **kwargs)

	def prepare_value(self, value):
		# converts decimal from db to hex before it is displayed in admin
		if value and isinstance(value, Decimal):
			value = _decimal_to_hex(value)
		return super(forms.CharField, self).prepare_value(value)


class HexDecimalField(models.DecimalField):
	"""
	This field stores a hexadecimal *string* as a decimal. In all cases, the
	value we deal with in python is always in hex.
	"""

	def get_prep_value(self, value):
		""" Return the integer value to be stored from the hex string """
		if value is None or value == "":
			return None
		if isinstance(value, str):
			value = _hex_string_to_decimal(value)
		return value

	def from_db_value(self, value, *args):
		""" Return an unsigned int representation from all db backends """
		if value is None:
			return value
		return _decimal_to_hex(value)

	def to_python(self, value):
		""" Return a str representation of the hexadecimal """
		if isinstance(value, str):
			return _hex_string_to_decimal(value)
		if value is None:
			return value
		return value

	def formfield(self, **kwargs):
		defaults = {"form_class": HexaDecimalField}
		defaults.update(kwargs)
		return super(models.DecimalField, self).formfield(**defaults)

	def run_validators(self, value):
		value = _hex_string_to_decimal(value)
		return super(models.DecimalField, self).run_validators(value)
