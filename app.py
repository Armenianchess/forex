from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, IntegerField, FloatField
from wtforms.validators import InputRequired, Length, AnyOf, Optional, StopValidation
from wtforms.validators import EqualTo, ValidationError
from forex_python.converter import CurrencyRates, CurrencyCodes
from decimal import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisisasecret!'


class Form11(FlaskForm):

	def validate_converting_from(self, converting_from):
		if converting_from.data not in ('USD','IDR','BGN','ILS','GBP','DKK','CAD','JPY','HUF','RON','MYR','SEK','SGD','HKD','AUD','CHF','KRW','CNY','TRY','HRK','NZD','THB','EUR','NOK','RUB','INR','MXN','CZK','BRL','PLN','PHP','ZAR'):
			raise ValidationError('Not a valid code: '+converting_from.data)

	def validate_converting_to(self, converting_to):
		if converting_to.data not in ('USD','IDR','BGN','ILS','GBP','DKK','CAD','JPY','HUF','RON','MYR','SEK','SGD','HKD','AUD','CHF','KRW','CNY','TRY','HRK','NZD','THB','EUR','NOK','RUB','INR','MXN','CZK','BRL','PLN','PHP','ZAR'):
			raise ValidationError('Not a valid code: '+converting_to.data)

	def currency(form, field):
		try:
			Decimal(field.data)
		except:
			raise StopValidation('Not a valid amount.')

	converting_from = StringField('Converting from', validators=[InputRequired()])
	converting_to = StringField('Converting to', validators=[InputRequired()])
	amount = StringField('Amount', [currency,InputRequired()])
    
@app.route('/form', methods=['GET', 'POST'])
def form():
    form = Form11()
    if form.validate_on_submit():
    	c = CurrencyRates(force_decimal=True)
    	dd = form.amount.data
    	aa = c.convert(form.converting_from.data, form.converting_to.data, Decimal(dd))
    	cc = CurrencyCodes()
    	ss = cc.get_symbol(form.converting_to.data)
    	return 'The result is {} {}.'.format(ss,round(aa,2))
    return render_template('form.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)


