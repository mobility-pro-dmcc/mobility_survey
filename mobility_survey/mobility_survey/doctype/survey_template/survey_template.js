// Copyright (c) 2026, Mobility Pro DMCC and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Survey Template", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on('Survey Template', {
    refresh: function(frm) {
        // Only show the button if the document has already been saved and has a name
        if (!frm.is_new()) {
            
            frm.add_custom_button(__('Edit Template'), function() {
                // window.location.origin dynamically gets {protocol}://{origin}
                let baseUrl = window.location.origin;
                let targetUrl = `${baseUrl}/survey_builder?name=${frm.doc.name}`;
                
                // Redirect the user to the template page
                window.location.href = targetUrl;
                
                // Alternative: If you want it to open in a new tab instead, use:
                // window.open(targetUrl, '_blank');
                
            }); // This places it under the "Actions" dropdown group. 
                               // Remove , __('Actions') if you want it as a standalone button.
        }
    }
});