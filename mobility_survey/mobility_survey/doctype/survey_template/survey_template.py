# Copyright (c) 2026, Mobility Pro DMCC and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import get_url

class SurveyTemplate(Document):
	def get_survey_url(self):
		base_url = get_url() 
		return f"{base_url}/survey_view?template={self.name}"
	
	def validate(self):
		self.survey_url = self.get_survey_url()