#!/usr/bin/env python
import os
import logging
import json
import re
import argparse

from weasyprint import HTML, CSS
from github import Github, Auth
from groq import Groq
from linkedin_api import Linkedin

def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Generate a professional resume from LinkedIn and GitHub data',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--output-dir',
        default=os.environ.get('RESUME_OUTPUT_DIR', './build'),
        help='Directory to save the generated resume (default: $RESUME_OUTPUT_DIR or ./build)'
    )
    
    parser.add_argument(
        '--profile-image',
        default=os.environ.get('RESUME_PROFILE_IMAGE_PATH'),
        help='Path to profile image (default: $RESUME_PROFILE_IMAGE_PATH)'
    )
    
    parser.add_argument(
        '--college-logo',
        default=os.environ.get('RESUME_COLLEGE_LOGO_PATH'),
        help='Path to college logo (default: $RESUME_COLLEGE_LOGO_PATH)'
    )
    
    parser.add_argument(
        '--linkedin-profile',
        default=os.environ.get('RESUME_LINKEDIN_PROFILE'),
        help='LinkedIn profile username (default: $RESUME_LINKEDIN_PROFILE)'
    )
    
    parser.add_argument(
        '--email',
        default=os.environ.get('RESUME_EMAIL'),
        help='Email address to display on resume (default: $RESUME_EMAIL)'
    )
    
    parser.add_argument(
        '--phone',
        default=os.environ.get('RESUME_PHONENO'),
        help='Phone number to display on resume (default: $RESUME_PHONENO)'
    )
    
    parser.add_argument(
        '--github-url',
        default=os.environ.get('RESUME_GITHUB_URL'),
        help='GitHub profile URL (default: $RESUME_GITHUB_URL)'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug logging'
    )

    return parser.parse_args()

args = parse_arguments()
    
# Configure logging
log_level = logging.DEBUG if args.debug else logging.INFO
logging.basicConfig(level=log_level)


RESUME_LINKEDIN_EMAIL = os.environ["RESUME_LINKEDIN_EMAIL"]
RESUME_LINKEDIN_PASSWORD = os.environ["RESUME_LINKEDIN_PASSWORD"]
RESUME_GITHUB_API_KEY = os.environ["RESUME_GITHUB_API_KEY"]
RESUME_GROQ_API_KEY = os.environ["RESUME_GROQ_API_KEY"]

RESUME_LINKEDIN_PROFILE = args.linkedin_profile
RESUME_EMAIL = args.email
RESUME_PHONENO = args.phone
RESUME_GITHUB_URL = args.github_url
RESUME_PROFILE_IMAGE_PATH = args.profile_image
RESUME_COLLEGE_LOGO_PATH = args.college_logo
RESUME_OUTPUT_DIR = args.output_dir

# Initialize required clients
logging.info("Initializing clients...")
logging.basicConfig(level=logging.DEBUG)

linkedin = Linkedin(RESUME_LINKEDIN_EMAIL,RESUME_LINKEDIN_PASSWORD)
logging.info("Linkedin client initialized.")

groq = Groq(api_key=RESUME_GROQ_API_KEY)
logging.info("Groq client initialized.")

github = Github(auth=Auth.Token(RESUME_GITHUB_API_KEY))
logging.info("Github client initialized.")


# Predifined Functions
def groq_chat(content):
    chat_completion = groq.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": content,
            }
        ],
        model="llama3-70b-8192",
        temperature=0.01,
        response_format={"type": "json_object"}
    )
    return chat_completion.choices[0].message.content

def get_github_languages():
    languages = {}
    for repo in github.get_user().get_repos():
        for lang, bytes in repo.get_languages().items():
            if lang not in languages:
                languages[lang] = bytes
            else:
                languages[lang] += bytes
    return languages


def fix_text(text, bypass=True):
    if bypass:
        return text
    content = f"""
    json schema:
    {'{"fixed_text": str}'}
    query:
    Fix the following text:
    {text}
    """
    return json.loads(groq_chat(content))["fixed_text"]

def extract_project_description_link(description):
    pattern = r"@([\w./-]+)$"
    m = re.search(pattern, description)

    if m:
        return m.group(1)
    return None

logging.info("Fetching profile from LinkedIn.")
linkedin_profile = linkedin.get_profile(RESUME_LINKEDIN_PROFILE)
linkedin_profile_skills = linkedin.get_profile_skills(RESUME_LINKEDIN_PROFILE)
logging.info("Profile fetched.")

name = linkedin_profile["firstName"] + " " + linkedin_profile["lastName"]
email = RESUME_EMAIL or linkedin_profile["emailAddress"]
phone = RESUME_PHONENO or linkedin_profile["phoneNumbers"][0]["number"]
logging.info(f"{name = }, {email =}")
address = linkedin_profile["geoLocationName"] + ", " + linkedin_profile["geoCountryName"]



header_section = f"""
      <div style="display: flex; align-items: center; margin-bottom: 20px">
        <img
          src="{RESUME_PROFILE_IMAGE_PATH}"
          alt="Profile Picture"
          style="height: 100px; border-radius: 2%; margin-right: 20px"
        />
        <h1 style="margin: 0; text-align: center; flex: 2">{name}</h1>
        <img
          src="{RESUME_COLLEGE_LOGO_PATH}"
          alt="Aloysius College Logo"
          style="height: 90px; border-radius: 2%; margin-right: 15px"
        />
      </div>
"""


contact_section = f'''
<div class="contact">
        {address} <br/>
        Mobile: +91 63601 27946

        | LinkedIn: <a href="https://www.linkedin.com/in/{RESUME_LINKEDIN_PROFILE}" target="_blank">@loyston-pais</a>

        | Email: <a href="{email}">{email}</a>
        
        | Github: <a href="{RESUME_GITHUB_URL}" target="_blank">@loystonpais</a>

        | Portfolio Website: <a href="https://loy.ftp.sh" target="_blank">loy.ftp.sh</a>

      </div>
'''



summary = linkedin_profile["summary"]
profile_summary_section = f'''
<div class="section">
        <h2>Profile Summary</h2>
        <p>
            {summary}
        </p>
      </div>
'''

language_proficiency_list = []
for language in linkedin_profile['languages']:
    language_name = language['name']
    proficiency = language['proficiency']
    if proficiency == "NATIVE_OR_BILINGUAL":
        proficiency = "Fluent"
    elif proficiency == "FULL_PROFESSIONAL":
        proficiency = "Fluent"
    else:
        continue
    language_proficiency_list.append(
        f"<li>{language_name} ({proficiency})</li>")
language_proficiency_span = "\n".join(language_proficiency_list)
language_proficiency_section = f"""
<div class="section">
    <h2>Language Proficiency</h2>
    <ul>
        {language_proficiency_span}
    </ul>
</div>
"""



academic_span_list = []

for edu in linkedin_profile.get("education", []):
    degree = edu.get("degreeName", "")
    field = edu.get("fieldOfStudy", "")
    school = edu.get("schoolName", "")
    start_year = edu.get("timePeriod", {}).get("startDate", {}).get("year", "")
    end_year = edu.get("timePeriod", {}).get("endDate", {}).get("year", "")
    grade = edu.get("grade")


    if grade and grade.endswith("%"):
        grade = f"{grade} (CGPA)"
    if degree:
        academic_span_list.append(
            f'''
            <li>
                <span class="title">{degree}{f" ({field})" if field else ""}, </span>
    {school} {f"({start_year} - {end_year})" if start_year and end_year else f"({end_year})"}{f": {grade}" if grade else ""}
            </li>
        ''')
academic_span = "\n".join(academic_span_list)

academic_section = f"""
<div class="section">
    <h2>Academic Qualification</h2>
    <ul>
        {academic_span}
    </ul>
</div>
"""





skills = [skill["name"] for skill in linkedin_profile_skills]
reply = groq_chat(f"write one-liner description for the given skills: {', '.join(skills)}. Arrange them in a better order for resume. The json schema should be for example" 
                + json.dumps({"skills": [{"lang": "langName", "line": "line"}]}))
reply = [(data["lang"], data["line"]) for data in json.loads(reply)["skills"]]

skills_list = "\n".join(f"<li>{skill}</>" for skill in skills)

skills_list2 = "\n".join(f"<li>{lang}</li>" for lang, line in reply)

skills_paragraph = '<p class="skills">' + ", ".join(f"{lang}" for lang, line in reply) + "</p>"

skills_list_wrapped = f"<ul> {skills_list} </ul>" 

skills_section = f"""
<div class="section">
    <h2>Skills</h2>
    {skills_paragraph}
</div>
"""


projects = linkedin_profile["projects"]
projects_list = []
for project in projects:
    title = project.get("title", "")
    description = project.get("description", "").strip()
    link = extract_project_description_link(description)
    if link.startswith("github.com"):
        description = description.replace(f"@{link}", f'<a href="https://{link}" target="_blank">github</a>')
    elif link is None:
        pass
    else:
        print(f"Project link extraction failure.. {description =}")
    projects_list.append(f"<li>{title} - {description}</li>")
projects_list = "\n".join(projects_list)
projects_list_wrapped = f"<ul> {projects_list} </ul>"
projects_section = f"""
<div class="section">
    <h2>Projects</h2>
    {projects_list_wrapped}
</div>
"""


final = f"""
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{name} - Resume</title>
    <link rel="stylesheet" type="text/css" href="resume.css">
  </head>
  <body>
    <page size="A4">
      {header_section}
      {contact_section}
      {profile_summary_section}
      {academic_section}
      {language_proficiency_section}
      {skills_section}
      {projects_section}
    </page>
  </body>
</html>

    """

os.system(f"mkdir -p {RESUME_OUTPUT_DIR}/")

HTML(string=final, base_url=".").write_pdf(f"{RESUME_OUTPUT_DIR}/resume.pdf", stylesheets=[CSS("resume.css")])
