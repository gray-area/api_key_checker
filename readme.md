# API Key Checker

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

A simple yet powerful tool to validate API keys. This lightweight utility helps penetration testers to test API keys that have been found.

## 📋 Features

- Quick validation of discovered API keys
- Detailed output of key status
- Simple command-line interface
- Fast and efficient execution

## Supported Checks

- Google
- Amazon AWS
- Microsoft Azure
- GitHub

## 🖼️ Screenshot

![Example Results](/Images/Results.PNG)

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/gray-area/api_key_checker.git

# Navigate to project directory
cd api_key_checker

# Install dependencies
pip install -r requirements.txt
```

## 💻 Usage

```bash
python main.py --service (google|aws|azure|github) --key YOUR__API_KEY
```

### Options

```
--key          Your Google API key to validate
--verbose      Enable detailed output
--output       Specify output format (text, json)
```

## 🔮 Future Enhancements
  
- **Batch Processing**: Allow validation of multiple keys at once
  
- **Configuration File**: Support for config files to store default settings

- **Provider Separation**: Each provider will eventually have their own file that will list all of their API URLs to be tested.

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Inspired by the need for simple API key validation tools
