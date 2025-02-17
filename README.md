# HiddenLotus - HydPyHackathon15

Hi everyone! 👋  

This is the codebase for the **HydPyHackathon**, developed by the **HiddenLotus** team.  

## 📌 Setup Instructions  

1. **Install Dependencies**  
   Run the following command to install the required dependencies:  
   ```bash
   pip install -r requirements.txt
   ```

2. **Setup the Database**  
   Run the `setup.py` script to initialize the database:
   ```bash
   python setup.py
   ```

3. **Run the Main Script**  
   After setting up the database, execute the `main.py` script:
   ```bash
   python main.py
   ```

## 🔑 API Keys Required  

Before running the project, make sure to set up your API keys:  

- **OpenAI API Key** – Required for AI-based functionalities.  
- **Twilio API Key** – Required for SMS/Call-based notifications.  

You can store these keys in an `.env` file:
```ini
OPENAI_API_KEY=your_openai_api_key
TWILIO_API_KEY=your_twilio_api_key
```

## 📂 Project Structure  

```
📞 HiddenLotus
├── 📂 conversation_logs    # Stores conversation logs
├── 📂 database             # Contains database-related files
├── agent.db                # SQLite database file
├── main.py                 # Main script to run the application
├── setup.py                # Script to set up the database
├── step1.py                # Additional functionality
├── utils.py                # Utility functions
└── README.md               # This file
```

## 🚀 Happy Hacking!  

Let us know if you have any questions or issues! 🎯

