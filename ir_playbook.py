import openai
from openai import OpenAI
import os

# Initialize the OpenAI client
client = OpenAI()

# Set your OpenAI API key here
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_incident_response_playbook(threat_type, environment_details):
    """
    Generate an incident response playbook based on the provided threat type and environment details.
    """
    # Create the messages for the OpenAI API
    messages = [
        {"role": "system", "content": "You are a SOC manager with 25 years of experience looking to create an incident response playbook."},
        {"role": "user", "content": f"Create a detailed incident response playbook for handling a '{threat_type}' threat affecting the following environment: {environment_details}."}
    ]

    # Make the API call
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=2048,
            n=1,
            stop=None,
            temperature=0.7
        )
        response_content = response.choices[0].message.content.strip()
        return response_content
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def save_playbook_to_markdown(playbook_content, threat_type):
    """
    Save the generated playbook content to a Markdown file named after the threat type.
    """
    try:
        # Create a filename based on the threat type
        filename = f"{threat_type.replace(' ', '_').lower()}_incident_response_playbook.md"
        
        # Save the content to a Markdown file
        with open(filename, "w") as file:
            file.write("# Incident Response Playbook\n\n")
            file.write(f"## Threat Type: {threat_type}\n\n")
            file.write(playbook_content)
        
        print(f"Playbook saved to {filename}")
    except Exception as e:
        print(f"An error occurred while saving the playbook: {e}")

# Sample Environment Details Format
"""
# Sample Environment Details

Network Architecture:
- The organization has a segmented network with separate VLANs for corporate, guest, and production environments. 
- The DMZ hosts public-facing web applications, while critical databases are located in a secure, isolated subnet.

Critical Assets:
- Key assets include the company’s ERP system, Active Directory, and customer databases, which store sensitive personal and financial information.

Security Tools:
- The environment uses a combination of Palo Alto firewalls, Snort IDS/IPS, CrowdStrike endpoint protection, and Splunk for SIEM.

Operating Systems:
- The majority of servers run on Windows Server 2019, with some Linux servers hosting web applications.

User and Access Management:
- User accounts are managed via Active Directory, with MFA enforced for all privileged accounts. 
- A PAM solution, CyberArk, is used for managing admin access.

Data Classification:
- Data is classified into three categories: Public, Confidential, and Highly Confidential. 
- Encryption is mandatory for all Highly Confidential data at rest and in transit.

Third-Party Integrations:
- The environment is integrated with AWS for cloud services and Office 365 for email and collaboration.

Incident History:
- The organization has previously experienced phishing attacks and ransomware incidents targeting the finance department.

Regulatory Requirements:
- The company must comply with GDPR and PCI-DSS, requiring breach notifications within 72 hours of discovery.

Communication Paths:
- Incident response involves the SOC team, IT Operations, and the CISO, with escalation to the executive team for major incidents.

Monitoring:
- All network traffic is monitored, and logs are collected in Splunk with a retention period of one year.

Threat Intelligence:
- The organization subscribes to ThreatConnect for threat intelligence, with feeds integrated into the SIEM for real-time analysis.
"""

# Get input from the user
threat_type = input("Enter the threat type: ")
print("\nPlease enter the environment details. Refer to the sample format in the code comments above if needed.")
environment_details = input("Enter environment details: ")

# Generate the playbook
playbook = generate_incident_response_playbook(threat_type, environment_details)

# Save the generated playbook to a Markdown file
if playbook:
    save_playbook_to_markdown(playbook, threat_type)
else:
    print("Failed to generate the playbook.")
