# Contributing
When contributing to this repository, please first discuss the change you wish to make via issue, email, or any other method with the owners of this repository before making a change.
Please note we have a code of conduct, please follow it in all your interactions with the project.
[Code of Conduct](#code-of-conduct) 

# Pre-Requirements
To contribute to our community project,please download and install the following:

1.  [Vagrant](https://www.vagrantup.com/)
2.  [VirtualBox](https://www.virtualbox.org/)
3.  [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

### Run the project on your local machine

A step by step series that tell you how to get Hotails up and running

1. Clone the repository
2. Open command prompt in Hotails directory
3. Spin the environment using `vagrant up` 
4. That's it! your virtual machine is up and running 
5. Go to http://localhost:8000 in your web browser
6. You can enter the virtual machine by running `vagrant ssh`
7. When finished, run `vagrant destroy -f` to tear down the environment\
**_NOTE:_** By running this command all changes on the virtual machine will be deleted.

**Note: Vagrant may not work on some machines (such as Apple M1-based machines), so please make sure to find a suitable solution.** 

# Pull Request Process
1.	Fork the repository and create a separate branch regarding your contribution.
2.	Update the CHANGELOG file with details of changes to the interface, this includes new environment variables, exposed ports, useful file locations, and container parameters.
3.	Changes to README file should be commited **ONLY** when there are changes relevant to the essence of the project, or the ways to deploy it!
4.	Issue a pull request and ask us to review it. Don't forget to link the PR to a relevant issue if it exists, **If not CREATE it!**
5.	Make sure your code is conformed to the PEP8 standard

**Note: If your PR does not meet one of the requirements, the PR will not be reviewed!**

## Issue a pull request:
1.	Set yourself as an Assignee
2.	Try to make your changes small as you can
3.	Write useful descriptions and titles
4.	Ask cotributors to review your PR.
5.	Once you have the sign-off of two developers and one of the maintainers, your PR will be merged.

## Pull request template:
1. Making changes/Creating XFILE
2. Empty line
3. What, why & how?
4. Testing
5. Add Screenshots(if needed)


## Reviewing PRs:
1. Allways provide constructive feedback
2. Be precise about what needs to be improved
3. Visualize the bigger picture

# Code Testing

This project uses Pytest as its test framework.

* [Pytest - Quick guide](https://docs.pytest.org/en/7.2.x/getting-started.html)
* Please note that Pytest is already installed in this project's virtual environment.

# Coding Conventions
Before adding code to our project please note that we use PEP8 standards & Flake8 test checking. You can read about it in the reference below.

* [PEP8](https://peps.python.org/pep-0008/)
* [Flake8](https://flake8.pycqa.org/en/latest/)

# Issues

Issues should be used to report a problem/bug in the main branch, request a new feature, or to propose potential changes.

## Guidelines to creating a new issue:

1.  Before you create a new issue, please make sure that there is no existing issue which addresses the same purpose.
2.  Every issue should have a meaningful and concise title that clearly describes its purpose.
3.  Every issue should have a meaningful and concise description that provides relevant information on the issue.
4.  When describing issues please try to phrase your issue in terms of the behavior you think needs changing rather than the code you think needs changing.

**Note:	Closing an issue doesn't necessarily mean the end of a discussion. If you believe your issue has been closed incorrectly, explain why and we'll consider if it needs to be reopened.**

# Code of Conduct
## Our Pledge
In the interest of fostering an open and welcoming environment, we as contributors and maintainers pledge to make participation in our project and our community a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.
## Our Standards
#### Examples of behavior that contributes to creating a positive environment include:

•	Using welcoming and inclusive language

•	Being respectful of differing viewpoints and experiences

•	Gracefully accepting constructive criticism

•	Focusing on what is best for the community

•	Showing empathy towards other community members

#### Examples of unacceptable behavior by participants include:

•	The use of sexualized language or imagery and unwelcome sexual attention or advances

•	Trolling, insulting/derogatory comments, and personal or political attacks

•	Public or private harassment

•	Publishing others' private information, such as a physical or electronic address, without explicit permission

•	Other conduct which could reasonably be considered inappropriate in a professional setting

## Our Responsibilities
Project maintainers are responsible for clarifying the standards of acceptable behavior and are expected to take appropriate and fair corrective action in response to any instances of unacceptable behavior.
Project maintainers have the right and responsibility to remove, edit, or reject comments, commits, code, wiki edits, issues, and other contributions that are not aligned to this Code of Conduct, or to ban temporarily or permanently any contributor for other behaviors that they deem inappropriate, threatening, offensive, or harmful.

## Scope
This Code of Conduct applies both within project spaces and in public spaces when an individual is representing the project or its community. Examples of representing a project or community include using an official project e-mail address, posting via an official social media account, or acting as an appointed representative at an online or offline event. Representation of a project may be further defined and clarified by project maintainers.

## Enforcement
Instances of abusive, harassing or otherwise unacceptable behavior may be reported by contacting the project team on GitHub. All complaints will be reviewed and investigated and will result in a response that is deemed necessary and appropriate to the circumstances. The project team is obligated to maintain confidentiality about the reporter of an incident. Further details of specific enforcement policies may be posted separately.
Project maintainers who do not follow or enforce the Code of Conduct in good faith may face temporary or permanent repercussions as determined by other members of the project's leadership.
