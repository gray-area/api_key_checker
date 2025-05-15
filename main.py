import requests
import json
import argparse
import os
import sys
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# ANSI escape codes for colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
BOLD = "\033[1m"
RESET = "\033[0m"

class APIValidator:
    def __init__(self, output_format="color", log_dir="logs"):
        self.output_format = output_format
        self.log_dir = log_dir
        
        # Create logs directory if it doesn't exist
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        # Prepare log file with timestamp
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_filename = f"{self.log_dir}/{self.timestamp}.log"
        self.log_file = open(self.log_filename, "w")
        
        # Store errors for summary display
        self.current_key_errors = []
        self.is_current_key_valid = False
        
    def __del__(self):
        if hasattr(self, 'log_file') and self.log_file:
            self.log_file.close()
            
    def print_and_log(self, service, api_name, status_code, error_message=None):
        # Consider key invalid if there's an error message, even with status 200
        is_valid = status_code == 200 and not error_message
        
        if is_valid:
            status_text = f"{GREEN}VALID{RESET}" if self.output_format == "color" else "VALID"
            log_status = "VALID"
            # Mark at least one API endpoint as valid
            self.is_current_key_valid = True
        else:
            status_text = f"{RED}INVALID{RESET}" if self.output_format == "color" else "INVALID"
            log_status = "INVALID"
            
            # Store error for summary
            if error_message:
                self.current_key_errors.append(f"{service} - {api_name}: {error_message}")
            elif status_code != 200:
                self.current_key_errors.append(f"{service} - {api_name}: HTTP {status_code}")
            
        output_line = f"{service} - {api_name} response status: {status_code} ({status_text})"
        print(output_line)
        
        # Write to log with error message
        log_line = f"{service} - {api_name} response status: {status_code} ({log_status})"
        self.log_file.write(f"{log_line}\n")
        if error_message:
            self.log_file.write(f"Error: {error_message}\n")
    
    def display_error_summary(self, service, key_identifier):
        """
        Display a summary of collected errors for the current key after all checks
        """
        if not self.is_current_key_valid and self.current_key_errors:
            error_summary = f"\n{RED}{BOLD}VALIDATION FAILED FOR {service} KEY: {key_identifier}{RESET}\n"
            error_summary += f"{RED}Errors:{RESET}\n"
            for error in self.current_key_errors:
                error_summary += f"{RED}• {error}{RESET}\n"
            print(error_summary)
            
            # Log the summary without color codes
            self.log_file.write(f"\nVALIDATION FAILED FOR {service} KEY: {key_identifier}\n")
            self.log_file.write("Errors:\n")
            for error in self.current_key_errors:
                self.log_file.write(f"• {error}\n")
        
        # Reset for next key
        self.current_key_errors = []
        self.is_current_key_valid = False
    
    def validate_google_api(self, api_key):
        print(f"{BLUE}{BOLD}Testing Google API key validity...{RESET}")
        self.log_file.write("=== Google API Key Tests ===\n")
        
        # Test Google Maps Geocoding API
        try:
            url = f"https://maps.googleapis.com/maps/api/geocode/json?address=New+York&key={api_key}"
            response = requests.get(url, timeout=10)
            error_msg = None
            
            # Check for error messages in JSON response even if status code is 200
            if response.status_code == 200:
                json_response = response.json()
                if json_response.get("status") != "OK":
                    error_msg = json_response.get("error_message") or f"API returned status: {json_response.get('status')}"
                # Check "error" field too (used by some Google APIs)
                if "error" in json_response:
                    error_msg = json_response.get("error", {}).get("message", "Unknown error")
                    
            self.print_and_log("Google", "Maps Geocoding API", response.status_code, error_msg)
        except Exception as e:
            self.print_and_log("Google", "Maps Geocoding API", 500, str(e))
        
        # Test YouTube Data API
        try:
            url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&key={api_key}"
            response = requests.get(url, timeout=10)
            error_msg = None
            
            # Check for error in response
            if response.status_code == 200:
                json_response = response.json()
                if "error" in json_response:
                    error_msg = json_response.get("error", {}).get("message", "Unknown error")
                    
            self.print_and_log("Google", "YouTube Data API", response.status_code, error_msg)
        except Exception as e:
            self.print_and_log("Google", "YouTube Data API", 500, str(e))
        
        # Test Cloud Vision API
        try:
            url = f"https://vision.googleapis.com/v1/images:annotate?key={api_key}"
            payload = {
                "requests": [
                    {
                        "image": {
                            "source": {
                                "imageUri": "https://storage.googleapis.com/cloud-samples-data/vision/face/faces.jpeg"
                            }
                        },
                        "features": [
                            {
                                "type": "LABEL_DETECTION",
                                "maxResults": 1
                            }
                        ]
                    }
                ]
            }
            headers = {"Content-Type": "application/json"}
            response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=10)
            error_msg = None
            
            # Check for error in response
            if response.status_code == 200:
                json_response = response.json()
                if "error" in json_response:
                    error_msg = json_response.get("error", {}).get("message", "Unknown error")
                    
            self.print_and_log("Google", "Cloud Vision API", response.status_code, error_msg)
        except Exception as e:
            self.print_and_log("Google", "Cloud Vision API", 500, str(e))
        
        # Test Google Translate API
        try:
            url = f"https://translation.googleapis.com/language/translate/v2?key={api_key}&q=hello&target=es"
            response = requests.get(url, timeout=10)
            error_msg = None
            
            # Check for error in response
            if response.status_code == 200:
                json_response = response.json()
                if "error" in json_response:
                    error_msg = json_response.get("error", {}).get("message", "Unknown error")
                    
            self.print_and_log("Google", "Translate API", response.status_code, error_msg)
        except Exception as e:
            self.print_and_log("Google", "Translate API", 500, str(e))
            
        # Display summary of errors for this key
        key_id = api_key[:6] + "..." + api_key[-4:] if len(api_key) > 10 else api_key
        self.display_error_summary("Google", key_id)
            
    def validate_aws_api(self, access_key, secret_key):
        print(f"{BLUE}{BOLD}Testing AWS API credentials validity...{RESET}")
        self.log_file.write("=== AWS API Credentials Tests ===\n")
        
        # AWS requires more complex authentication using the aws-sdk
        # For basic validation, we can check S3 access
        try:
            import boto3
            from botocore.exceptions import ClientError
            
            # Create a session with the provided credentials
            session = boto3.Session(
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key
            )
            
            # Test S3 service
            try:
                s3 = session.client('s3')
                response = s3.list_buckets()
                self.print_and_log("AWS", "S3 API", 200)
            except ClientError as e:
                error_code = e.response['Error']['Code']
                error_msg = e.response['Error']['Message']
                self.print_and_log("AWS", "S3 API", 403, f"{error_code}: {error_msg}")
                
            # Test EC2 service
            try:
                ec2 = session.client('ec2')
                response = ec2.describe_regions()
                self.print_and_log("AWS", "EC2 API", 200)
            except ClientError as e:
                error_code = e.response['Error']['Code']
                error_msg = e.response['Error']['Message']
                self.print_and_log("AWS", "EC2 API", 403, f"{error_code}: {error_msg}")
                
        except ImportError:
            self.print_and_log("AWS", "API", 500, "boto3 library not installed. Run 'pip install boto3' to validate AWS credentials.")
        except Exception as e:
            self.print_and_log("AWS", "API", 500, str(e))
            
        # Display summary of errors for this key
        key_id = access_key[:6] + "..." + access_key[-4:] if len(access_key) > 10 else access_key
        self.display_error_summary("AWS", key_id)
            
    def validate_azure_api(self, api_key):
        print(f"{BLUE}{BOLD}Testing Azure API key validity...{RESET}")
        self.log_file.write("=== Azure API Key Tests ===\n")
        
        # Test Azure Cognitive Services - Text Analytics
        try:
            url = "https://api.cognitive.microsoft.com/bing/v7.0/search"
            headers = {
                "Ocp-Apim-Subscription-Key": api_key,
                "Content-Type": "application/json"
            }
            params = {"q": "microsoft azure", "count": 1}
            response = requests.get(url, headers=headers, params=params, timeout=10)
            error_msg = None
            
            # Check for error messages in response
            if response.status_code == 200:
                try:
                    json_response = response.json()
                    # Azure may include errors in different formats
                    if "error" in json_response:
                        error_obj = json_response.get("error", {})
                        error_msg = error_obj.get("message") or str(error_obj)
                except ValueError:
                    # Not JSON or couldn't parse
                    pass
                    
            self.print_and_log("Azure", "Bing Search API", response.status_code, error_msg)
        except Exception as e:
            self.print_and_log("Azure", "Bing Search API", 500, str(e))
            
        # Test Azure Computer Vision API
        try:
            url = "https://api.cognitive.microsoft.com/vision/v3.1/analyze"
            headers = {
                "Ocp-Apim-Subscription-Key": api_key,
                "Content-Type": "application/json"
            }
            body = {
                "url": "https://upload.wikimedia.org/wikipedia/commons/3/3c/Shaki_waterfall.jpg"
            }
            response = requests.post(url, headers=headers, json=body, timeout=10)
            error_msg = None
            
            # Check for error messages in response
            if response.status_code == 200:
                try:
                    json_response = response.json()
                    if "error" in json_response:
                        error_obj = json_response.get("error", {})
                        error_msg = error_obj.get("message") or str(error_obj)
                except ValueError:
                    # Not JSON or couldn't parse
                    pass
                    
            self.print_and_log("Azure", "Computer Vision API", response.status_code, error_msg)
        except Exception as e:
            self.print_and_log("Azure", "Computer Vision API", 500, str(e))
            
        # Display summary of errors for this key
        key_id = api_key[:6] + "..." + api_key[-4:] if len(api_key) > 10 else api_key
        self.display_error_summary("Azure", key_id)
            
    def validate_github_api(self, token):
        print(f"{BLUE}{BOLD}Testing GitHub API token validity...{RESET}")
        self.log_file.write("=== GitHub API Token Tests ===\n")
        
        # Test GitHub API - User endpoint
        try:
            url = "https://api.github.com/user"
            headers = {
                "Authorization": f"token {token}",
                "Accept": "application/vnd.github.v3+json"
            }
            response = requests.get(url, headers=headers, timeout=10)
            error_msg = None
            
            # Check for error messages in response
            if response.status_code == 200:
                try:
                    json_response = response.json()
                    if "message" in json_response and "documentation_url" in json_response:
                        # This typically indicates an error response from GitHub
                        error_msg = json_response.get("message")
                except ValueError:
                    # Not JSON or couldn't parse
                    pass
                    
            self.print_and_log("GitHub", "User API", response.status_code, error_msg)
        except Exception as e:
            self.print_and_log("GitHub", "User API", 500, str(e))
            
        # Test GitHub API - Repos endpoint
        try:
            url = "https://api.github.com/user/repos"
            headers = {
                "Authorization": f"token {token}",
                "Accept": "application/vnd.github.v3+json"
            }
            response = requests.get(url, headers=headers, timeout=10)
            error_msg = None
            
            # Check for error messages in response
            if response.status_code == 200:
                try:
                    json_response = response.json()
                    if isinstance(json_response, dict) and "message" in json_response:
                        # This typically indicates an error response
                        error_msg = json_response.get("message")
                except ValueError:
                    # Not JSON or couldn't parse
                    pass
                    
            self.print_and_log("GitHub", "Repos API", response.status_code, error_msg)
        except Exception as e:
            self.print_and_log("GitHub", "Repos API", 500, str(e))
            
        # Display summary of errors for this key
        token_id = token[:6] + "..." + token[-4:] if len(token) > 10 else token
        self.display_error_summary("GitHub", token_id)


def process_key_file(file_path, validator, service):
    """Process a file containing multiple API keys."""
    print(f"Processing keys from file: {file_path}")
    success_count = 0
    error_count = 0
    skipped_count = 0
    
    try:
        with open(file_path, 'r') as file:
            keys = [line.strip() for line in file if line.strip() and not line.startswith('#')]
            
        print(f"Found {len(keys)} keys to process")
        
        for key in keys:
            if service == 'google':
                validator.validate_google_api(key)
                success_count += 1
            elif service == 'azure':
                validator.validate_azure_api(key)
                success_count += 1
            elif service == 'github':
                validator.validate_github_api(key)
                success_count += 1
            elif service == 'aws':
                # AWS keys are typically in pairs (access key, secret key)
                parts = key.split(',')
                if len(parts) == 2:
                    access_key, secret_key = parts
                    validator.validate_aws_api(access_key.strip(), secret_key.strip())
                    success_count += 1
                else:
                    print(f"{YELLOW}Warning: Skipping invalid AWS key format. Expected format: ACCESS_KEY,SECRET_KEY{RESET}")
                    skipped_count += 1
            else:
                print(f"{RED}Error: Unknown service '{service}'{RESET}")
                error_count += 1
                break
            
            # Add a separator between key tests
            print("-" * 60)
            validator.log_file.write("-" * 60 + "\n")
                
    except Exception as e:
        print(f"{RED}Error processing file {file_path}: {str(e)}{RESET}")
        error_count += 1
        
    return success_count, error_count, skipped_count


def main():
    parser = argparse.ArgumentParser(description='Multi-Platform API Key Validator')
    
    parser.add_argument('--service', type=str, choices=['google', 'aws', 'azure', 'github', 'all'],
                        help='Specify which service to validate against', required=True)
    
    key_group = parser.add_mutually_exclusive_group(required=True)
    key_group.add_argument('--key', type=str, help='API key to validate')
    key_group.add_argument('--key-file', type=str, help='Path to file containing API keys (one per line)')
    
    # AWS specific arguments
    parser.add_argument('--aws-secret', type=str, help='AWS Secret Key (required with --service aws and --key)')
    
    # Output format
    parser.add_argument('--output', type=str, choices=['color', 'plain'], default='color',
                        help='Output format (color or plain text)')
    
    # Log directory
    parser.add_argument('--log-dir', type=str, default='logs',
                        help='Directory to store log files')
    
    args = parser.parse_args()
    
    # Initialize validator
    validator = APIValidator(output_format=args.output, log_dir=args.log_dir)
    
    try:
        # Process based on service type and input method
        if args.key_file:
            # Batch processing from file
            success, errors, skipped = process_key_file(args.key_file, validator, args.service)
            print(f"\nBatch processing complete: {success} successful, {errors} errors, {skipped} skipped")
        else:
            # Single key processing
            if args.service == 'google':
                validator.validate_google_api(args.key)
            elif args.service == 'azure':
                validator.validate_azure_api(args.key)
            elif args.service == 'github':
                validator.validate_github_api(args.key)
            elif args.service == 'aws':
                if not args.aws_secret:
                    print(f"{RED}Error: --aws-secret is required when using --service aws with a single key{RESET}")
                    sys.exit(1)
                validator.validate_aws_api(args.key, args.aws_secret)
            elif args.service == 'all':
                # For 'all' service with a single key, we'll try it against all platforms
                # (though this is not typically recommended as keys are service-specific)
                validator.validate_google_api(args.key)
                if args.aws_secret:
                    validator.validate_aws_api(args.key, args.aws_secret)
                validator.validate_azure_api(args.key)
                validator.validate_github_api(args.key)
                
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Process interrupted by user{RESET}")
    except Exception as e:
        print(f"\n{RED}Error: {str(e)}{RESET}")
    finally:
        print(f"\nFull output saved to {validator.log_filename}")
        validator.log_file.close()


if __name__ == "__main__":
    main()
