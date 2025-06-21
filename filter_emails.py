import re
import os
from pathlib import Path
from typing import List, Optional

# my email filtering script - extracts emails from text files
# created this to clean up messy contact lists

def find_all_emails_in_text(text: str) -> List[str]:
    # look for email patterns in the text
    # this regex should catch most email formats
    
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    
    # get all matches and remove duplicates (keep order)
    found_emails = re.findall(email_pattern, text)
    # remove duplicates but keep the order they appeared
    unique_emails = []
    for email in found_emails:
        if email not in unique_emails:
            unique_emails.append(email)
    
    return unique_emails


def write_emails_to_file(emails: List[str], output_path: str) -> None:
    # save the emails to a file with commas between them
    
    # make sure the folder exists
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # join them with commas and write
    email_string = ', '.join(emails)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(email_string)


def filter_emails_from_file(input_path: str, output_path: str) -> Optional[int]:
    # main function that does the work
    
    try:
        # check if file exists first
        if not os.path.exists(input_path):
            print(f"Error: can't find '{input_path}'")
            print("   check if the file exists and path is right")
            return None
        
        # read the file
        print(f"reading: {input_path}")
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # find the emails
        print("looking for emails...")
        emails = find_all_emails_in_text(content)
        
        if not emails:
            print("no emails found")
            return 0
        
        # save them
        print(f"saving {len(emails)} email(s) to: {output_path}")
        write_emails_to_file(emails, output_path)
        
        # show results
        print(f"done! found {len(emails)} email(s)")
        print("emails found:")
        for i, email in enumerate(emails, 1):
            print(f"   {i}. {email}")
        
        return len(emails)
        
    except PermissionError:
        print(f"permission error - can't access '{input_path}' or write to '{output_path}'")
        print("   check file permissions")
        return None
    except UnicodeDecodeError:
        print(f"encoding problem with '{input_path}' - might not be a text file")
        print("   make sure it's a plain text file")
        return None
    except Exception as e:
        print(f"something broke: {e}")
        print("   check the file and try again")
        return None


def run_email_filter():
    # setup paths and run the filter
    
    input_file = "input_files/beforetext.txt"
    output_file = "output_files/aftertext.txt"
    
    print("starting email filter...")
    print("=" * 50)
    
    # do the work
    email_count = filter_emails_from_file(input_file, output_file)
    
    print("=" * 50)
    if email_count is not None:
        print(f"finished! processed {email_count} email(s)")
    else:
        print("failed - check the errors above")


if __name__ == "__main__":
    run_email_filter() 