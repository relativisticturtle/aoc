# Getting session-cookie using Chrome:

- Navigate to Advent of Code and login
- Right-click > "Inspect" > "Application"-tab
- "Storage" > "Session Storage" > "Cookies" > https://adventofcode.com
- Copy&paste to session.txt

# Installing virtual environment

Assuming Python 3.7 in default user-location:

```
%LOCALAPPDATA%\Programs\Python\Python37\python -m venv --prompt aoc .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
```

...or just run `aoc.bat`

(or manually: )

# Access multiple GitHub-accounts from 1 computer

**1. Create additional SSH-key**

```
ssh-keygen -t rsa -b 4096 -C my-email@address.com
```

Do not overwrite current. Save as new file (e.g., `~/.ssh/id_rsa-rt`).

**2. Add entry to SSH-config**

In the file `~/.ssh/config`, add entry for using this key for a certain alias ("github-rt"):

```
Host github-rt
  Hostname github.com
  IdentityFile ~/.ssh/id_rsa-rt
  IdentitiesOnly yes
```

**3. Clone repository with the new SSH-key**

```
git clone git@github-rt:relativisticturtle/aoc.git
```

*NOTE: mind the "github-rt" used for host (rather than "github.com")*
