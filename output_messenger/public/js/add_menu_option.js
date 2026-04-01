$(document).on("form-refresh", function (event, frm) {

    // console.log("==============refreshhhh!!!============")
    setTimeout(() => {
        frappe.db.get_single_value("Output Messenger Settings OM", "enable_output_messenger")
            .then(enabled => {
                if (enabled) {
                    setup_output_messenger(frm)
                }
            })
    }, 200);
})

function setup_output_messenger(frm) {
    frm.page.add_menu_item(__('Output Messenger'), function (e) {
        let dialog = undefined
        const dialog_field = []

        dialog_field.push(
            {
                fieldtype: "MultiSelectPills",
                fieldname: "recipients",
                label: __("Select Recipients"),
                reqd: true,
                get_data: function (txt) {
                    return frappe.db.get_link_options("User", txt, {
                        custom_output_user_id: ["!=", undefined] || ["!=", ""],
                        enabled: 1,
                    });
                },
            },
            {
                fieldtype: "Small Text",
                fieldname: "notes",
                label: __("Notes")
            }

        )

        dialog = new frappe.ui.Dialog({
            title: __("Send Output Notification"),
            fields: dialog_field,
            primary_action_label: 'Notify',
            primary_action: function (values) {
                if (values) {
                    console.log(values, "=====")
                    const route = frappe.get_route();
                    console.log(route, "===route===")
                    const route_link = `/app/${route[1].toLowerCase().replace(/ /g, "-")}/${route[2]}`;
                    const full_url = window.location.origin + route_link;

                    frappe.call({
                        method: "output_messenger.api.send_output_notification_to_users",
                        args: {
                            "recipients_list": values.recipients,
                            "notes": values.notes,
                            "doctype": frm.doc.doctype,
                            "docname": frm.doc.name
                        },
                        callback: function (r) {
                            console.log(r.message)
                        }
                    })
                    // console.log(full_url, "===full_url===")
                    // frappe.msgprint({
                    //     title: "Document Link",
                    //     message: `<a href="${full_url}" target="_blank">${full_url}</a>`
                    // });
                }
                dialog.hide()
            }
        })

        dialog.show()
    }); 
}