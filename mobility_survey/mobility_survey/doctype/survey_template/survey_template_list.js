frappe.listview_settings['Survey Template'] = {
    refresh: function(listview) {
        // 1. Hide the default primary "Add Your DocType" button
        listview.page.clear_primary_action();

        // 2. Add your custom primary "Create Template" button
        listview.page.set_primary_action(
            __('Create Template'), 
            function() {
                // Get the current browser protocol and origin
                let baseUrl = window.location.origin;
                
                // Redirect the user to the survey builder
                window.location.href = `${baseUrl}/survey_builder`;
            },
            'plus' // Optional: adds a plus icon to the button
        );
    }
};