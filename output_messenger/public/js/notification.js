frappe.ui.form.on("Notification", {
	refresh: function (frm) {
		frm.set_query("custom_notification_sender_om", () => {
			return {
				filters: {
					custom_output_user_id: ["!=", undefined] || ["!=", ""],
					enabled: 1,
				},
			};
		});

		frm.set_df_property(
			"column_break_5",
			"depends_on",
			"eval:in_list(['Email', 'SMS', 'WhatsApp', 'Wati Whatsapp', 'Output Messenger'], doc.channel)"
		);
	},
})