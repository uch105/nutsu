import os
import sys
import django
from decouple import config

project_root = config("PROJECT_ROOT")
sys.path.append(project_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prescribemate.settings')
django.setup()

import re

def normalize_bd_phone_number(phone_str):
    """
    Normalizes Bangladeshi phone numbers to 880XXXXXXXXXX format.
    
    Args:
        phone_str (str): Raw phone number string in any common format
    
    Returns:
        str: Normalized phone number in 880XXXXXXXXXX format
    
    Raises:
        ValueError: If the phone number cannot be normalized
    """

    digits = re.sub(r'[^0-9]', '', phone_str)

    if digits.startswith('8800') and len(digits) >= 13:
        digits = '880' + digits[4:]

    elif digits.startswith('0'):
        digits = '880' + digits[1:]

    elif len(digits) == 10 and digits[0] in '123456789':
        digits = '880' + digits

    if not (len(digits) == 13 and digits.startswith('880') and digits[3] in '123456789'):
        raise ValueError(f"Invalid Bangladeshi phone number: {phone_str}")
    
    return digits

'''
test_numbers = [
    '+880-01712345678',
    '01712345678',
    '01712-345678',
    '880 0171 2345678',
    '880-0171-2345678',
    '880 0171-2345678',
    '01912345678',
    '8801912345678',
    '880 019 12345678',
    '8800123456789',
    '1234567890'
]

print("{:25} -> {}".format("Input", "Normalized"))
print("-" * 40)
for number in test_numbers:
    try:
        normalized = normalize_bd_phone_number(number)

    except ValueError as e:
        print(f"{number:25} -> ERROR: {str(e)}")
'''