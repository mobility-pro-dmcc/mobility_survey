import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def execute():
    custom_fields = {
        "Employee": [
            {
                "fieldname": "work_mode",
                "label": "Work Mode",
                "fieldtype": "Select",
                "options": "\nRemote\nOn-site\nHibrid",
                "insert_after": "reports_to"
            },
            {
                "fieldname": "location",
                "label": "Location",
                "fieldtype": "Link",
                "options": "Location",
                "insert_after": "grade"
            }
        ],
    }

    create_custom_fields(custom_fields, ignore_validate=True)