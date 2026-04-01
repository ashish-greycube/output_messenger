### Output Messenger

Output Messenger Integration

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch develop
bench install-app output_messenger
```

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/output_messenger
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade

<hr>

### Key Features:
**i) Notification Integration:** <br>
     - Added a new channel: Output Messenger in the Notification DocType<br>
     - Notifications will now be sent via Output Messenger when triggered<br>

**ii) Manual Messaging (All DocTypes)** <br>
     - Added a menu item: Send Output Messenger   <br>
     - On click: <br>
          - Opens a dialog box    <br>
          - Allows user selection <br>
          - Sends the current document link via Output Messenger <br>

<hr>

### License

mit
