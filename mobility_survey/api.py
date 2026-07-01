# -*- coding: utf-8 -*-
import frappe
import json
from frappe import _
from frappe.rate_limiter import rate_limit

@frappe.whitelist(allow_guest=True)
def get_survey_template(template_id):
    """
    Retrieves the configuration schema and the custom template descriptive name 
    using the document's primary unique ID (name).
    """
    if not template_id:
        frappe.throw(_("Please provide a valid template ID to load."))

    if frappe.db.exists("Survey Answer", {"survey_template": template_id, "user": frappe.session.user}) and frappe.session.user == "Guest":
        return {
            "already_submitted": True,
            "structure": [],
            "template_name": ""
        }

    # Fetch both the structure JSON and the descriptive title field from the database
    doc_fields = frappe.db.get_value("Survey Template", template_id, ["structure_json", "template_name"], as_dict=True)
    
    if not doc_fields:
        return {
            "already_submitted": False,
            "structure": [],
            "template_name": template_id
        }

    try:
        parsed_structure = json.loads(doc_fields.structure_json) if doc_fields.structure_json else []
    except (ValueError, TypeError):
        parsed_structure = []

    return {
        "already_submitted": False,
        "structure": parsed_structure,
        "template_name": doc_fields.template_name or template_id
    }

@frappe.whitelist()
def save_survey_template(structure, template_id, template_name):
    """
    Saves the survey schema structure and updates the internal descriptive 'template_name' field
    without altering the document's primary key index (name).
    """
    if not template_id:
        frappe.throw(_("Missing required template document ID handle."))

    try:
        parsed_structure = json.loads(structure)
    except (ValueError, TypeError):
        frappe.throw(_("The survey configuration payload is corrupted or malformed."))

    cleaned_name = template_name.strip()
    serialized_structure = json.dumps(parsed_structure, indent=4, ensure_ascii=False)

    if frappe.db.exists("Survey Template", template_id):
        # Update the existing record fields directly
        frappe.db.set_value(
            "Survey Template", 
            template_id, 
            {
                "structure_json": serialized_structure,
                "template_name": cleaned_name
            }
        )
        saved_id = template_id
    else:
        # Fallback creation if it doesn't exist
        doc = frappe.get_doc({
            "doctype": "Survey Template",
            "name": template_id,
            "template_name": cleaned_name,
            "structure_json": serialized_structure
        })
        doc.insert(ignore_permissions=True)
        saved_id = doc.name
        
    frappe.db.commit()
    
    return {
        "status": "success", 
        "template_id": saved_id
    }

@frappe.whitelist(allow_guest=True)
@rate_limit(key="ip", limit=500, seconds=3600)
def submit_survey_response(template_id, answers):
    """
    Accepts user answers as a flattened key-value object map,
    and commits them under a new Response tracking record.
    """
    if not template_id or not answers:
        frappe.throw(_("Invalid submission request payload content context."))

    try:
        parsed_answers = json.loads(answers)
    except (ValueError, TypeError):
        frappe.throw(_("Submitted answers payload string structure is malformed."))

    if frappe.db.exists("Survey Answer", {"survey_template": template_id, "user": frappe.session.user}) and frappe.session.user != "Guest":
        frappe.throw(_("You have already completed this survey session configuration."))

    # Generate a new unique Response ledger record linked securely to the template
    response_doc = frappe.get_doc({
        "doctype": "Survey Answer",
        "survey_template": template_id,
        "user": frappe.session.user
    })
    
    # Pack dynamic child elements properly inside child table targets
    response_doc.set("answers", [{"question": key, "answer": str(value)} for key, value in parsed_answers.items()])
    response_doc.insert(ignore_permissions=True)
    
    # Anonymize ownership metrics safely if needed
    frappe.db.set_value("Survey Answer", response_doc.name, {"owner": "Administrator", "modified_by": "Administrator"}, update_modified=False)
    frappe.db.commit()

    return {"status": "success", "message": _("Your answers have been securely logged.")}