
# Browser Synthetic Monitoring

To test this script locally, the following prerequisite, steps need to be completed





## Prerequisite

- Python 3+ is needed
    
## Steps for Session 1 - Building your first Synthetic Script

- To run this script locally, do follow the instructions as per the comment on the script and the credentials used in this script are available on https://saucedemo.com/.  
- The credentails being used in the script are the standard username and password.  
- When uploading the script on Splunk Appdynamics Controller, please reference the key's from the Synthetic Vault.


```bash
  python3 -m venv ./env
  source ./env/bin/activate
  pip install -r requirements.txt
  python brum-syn.py
```

## Steps for Session 2 - Advanced BRUM Script Building

- To run this script locally, do follow the instructions as per the comment on the script and the credentials used in this script are available on https://saucedemo.com/.  
- The credentials being used in the script are standard, locked username and password.  
- When uploading the script on Splunk Appdynamics Controller, please reference the key's from the Synthetic Vault.  


```bash
  python brum-syn-adv.py
```

### Upload Script on Splunk AppDynamics controller
```
Copy the script and make the necessary changes as per the comments, remove any username, password and utilise the Synthetic Vault in the controller.
```

### Exit Python Virtual Environment
```
deactivate
```


## Author

- [@vikashgounder](https://www.github.com/vikashgounder)

