# Automated Resume Builder

This tool automatically generates a professional resume by pulling data from LinkedIn and GitHub profiles. It uses LinkedIn API for professional details, GitHub API for repository information, and Groq API for text processing.

## Environment Variables

```sh
# Important
RESUME_GITHUB_API_KEY # GitHub Personal Access Token
RESUME_GROQ_API_KEY # Groq API key for text processing
RESUME_LINKEDIN_PASSWORD # Your LinkedIn account password


RESUME_LINKEDIN_EMAIL # Your LinkedIn account email
RESUME_LINKEDIN_PROFILE # Your LinkedIn profile username (e.g., 'john-doe')
RESUME_EMAIL # Email to display on resume
RESUME_PHONENO # Phone number to display on resume
RESUME_GITHUB_URL # Your GitHub profile URL
RESUME_PROFILE_IMAGE_PATH # Path to your profile image
RESUME_COLLEGE_LOGO_PATH # Path to your college/university logo
RESUME_OUTPUT_DIR # Directory where resume will be generated
```

## Usage

```sh
usage: build-resume [-h] [--output-dir OUTPUT_DIR] [--profile-image PROFILE_IMAGE] [--college-logo COLLEGE_LOGO] [--linkedin-profile LINKEDIN_PROFILE]
                    [--email EMAIL] [--phone PHONE] [--github-url GITHUB_URL] [--debug]

Generate a professional resume from LinkedIn and GitHub data

options:
  -h, --help            show this help message and exit
  --output-dir OUTPUT_DIR
                        Directory to save the generated resume (default: $RESUME_OUTPUT_DIR or ./build)
  --profile-image PROFILE_IMAGE
                        Path to profile image (default: $RESUME_PROFILE_IMAGE_PATH)
  --college-logo COLLEGE_LOGO
                        Path to college logo (default: $RESUME_COLLEGE_LOGO_PATH)
  --linkedin-profile LINKEDIN_PROFILE
                        LinkedIn profile username (default: $RESUME_LINKEDIN_PROFILE)
  --email EMAIL         Email address to display on resume (default: $RESUME_EMAIL)
  --phone PHONE         Phone number to display on resume (default: $RESUME_PHONENO)
  --github-url GITHUB_URL
                        GitHub profile URL (default: $RESUME_GITHUB_URL)
  --debug               Enable debug logging
```
