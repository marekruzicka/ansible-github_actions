# Ansible stdout callback plugin compatible with github actions workflow

- ansible stdout callback plugin
- ouput compatible with github workflows
  - minimal ouput that still provides relevant information in a way that can be presented within workflow window on github
  - ok msg : notice
  - changed msg : warning
  - failed msg : error
  - group by plays (ability to collapse within gihub UI)
  - group by tasks (ability to collapse within gihub UI)