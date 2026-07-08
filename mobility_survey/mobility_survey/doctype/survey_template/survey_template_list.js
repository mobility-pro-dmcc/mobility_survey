frappe.listview_settings['Survey Template'] = {
    add_fields: ["survey_url", "template_name"],
    hide_name_column: true,
    primary_action: function() {
        window.location.href = `${window.location.origin}/survey_builder`;
    },
    button: {
        show: function(doc) {
            return true;
        },
        get_label: function() {
            return __("Go to Survey");
        },
        get_description: function(doc) {
            return __("Click to go to Survey");
        },
        action: function(doc) {
            window.location.href = "/survey_view?template=" + doc.name;
        },
    }
};