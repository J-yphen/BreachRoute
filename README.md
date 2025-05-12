# BreachRoute
## Overview
**BreachRoute** is a Python Flask application designed for penetration testers and security researchers to easily serve, manage, and monitor payloads for out-of-the-band (OOB) attack scenarios. It provides a secure, interactive, and flexible platform to create, update, activate, and deactivate endpoints, with live previews and seamless file storage integration over the internet.


## Features
- [x] **Live Preview:**: Instantly preview payloads and endpoints as you create or modify them, streamlining testing and validation.
- [x] **Dynamic Endpoint** Management: Create, update, and delete endpoints on the fly.
- [x] **Activate/Deactivate Endpoints:** Enable or disable any endpoint instantly, without restarting the server.
- [x] **Authentication:** Secure login system protects all management features.
- [x] **Object Storage Integration:** Store and retrieve files over the internet using your preferred cloud provider.
- [x] **User-Friendly Interface:** Manage endpoints, files, and logs through an intuitive web UI.


## Getting Started

### Prerequisites
- Python
- Flask

### Installation
```bash
git clone https://github.com/J-yphen/BreachRoute.git
cd breachroute
pip install -r requirements.txt
```

### Configuration
Before running BreachRoute, you need to configure environment variables
In the root directory of your project, create a file named .env and add the following variables:

```
# Required for Flask session security
FLASK_SECRET_KEY=your-very-secret-key

# Database connection string (required if using an online database)
DATABASE_URL=your-database-connection-url

```


> **Note:**  
> - Replace the values with your actual secrets and credentials.


### Running the App

1. Start the server:
    ```
    python ./run.py
    ```

2. Visit `/setup` in your browser for the first-time setup to create your account and configure object storage.

> **Note:**  
> - Once setup is completed, you cannot add or change object storage via the UI.  
> - Please make sure to configure object storage during the initial setup at `/setup`.


## Usage
- Login: Access the management dashboard at /login to authenticate.
- Manage Endpoints: Use the dashboard to create, update, activate/deactivate, or delete endpoints in real time.
- Live Preview: Instantly see how payloads will be served.
- Object Storage: Configure your object storage provider in the app settings to upload and retrieve files.


## Security
- All management actions require authentication.
- Endpoints can be activated or deactivated at any time.
- Never run the app in debug mode in production.
- Store sensitive credentials (such as DB URL) securely via environment variables.

## Contributing
Pull requests and feature suggestions are welcome! Please open an issue to discuss your ideas or report bugs.


## TODO
- [ ] **Logging and Monitoring (Webhooks):** Track all interactions with endpoints for auditing and debugging.
- [ ] **Docker Support:** Provide ready-to-use Docker deployment for consistent environments and rapid setup.
- [ ] **Forgot Password:** Implement a secure password reset mechanism.
- [ ] **Update Password & Re-configure Object Storage:** Allow users to update their password and modify object storage configuration after initial setup.
- [ ] **RESTful API:** Expose endpoints and file management features via a RESTful API for automation and integration with other tools.
