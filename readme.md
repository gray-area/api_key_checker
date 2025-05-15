# API Key Checker

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

A simple yet powerful tool to validate Google API keys. This lightweight utility helps developers test the validity of their Google API keys before deploying them to production environments.

## 📋 Features

- Quick validation of Google API keys
- Detailed output of key status
- Simple command-line interface
- Fast and efficient execution

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
python main.py --key YOUR_GOOGLE_API_KEY
```

### Options

```
--key          Your Google API key to validate
--verbose      Enable detailed output
--output       Specify output format (text, json)
```

## 🔮 Future Enhancements

- **Multi-Platform Support**: Extend validation capabilities to other services:
  - Amazon AWS
  - Microsoft Azure
  - GitHub
  - And more cloud providers
  
- **Service Selection**: Add the ability to specify which service you want to validate against
  - `--service google|aws|azure|github`

- **Batch Processing**: Allow validation of multiple keys at once
  
- **Configuration File**: Support for config files to store default settings


## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Thanks to all contributors who have helped with the development
- Inspired by the need for simple API key validation tools
