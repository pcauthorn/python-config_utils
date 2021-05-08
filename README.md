# configutils

Allows for composable configs

Example, with two configs

# Merge
```yaml
# base.yaml
parser: xyz
timeout: 10
email: a@example.com
# ... 

```

```yaml
# A different config at abc.yaml

parser: abc
__ConfigUtil_Directive:
  Update: [base.yaml] 
```

To create a config with default values from first file with the ```parser``` overridden and set to ```abc``` code would look like:
```
updater = ConfigUpdater()
config = yaml.load('abc.yml')
new_config = updater.update_config(config)
# new_config yaml:
# parser: abc
# timeout: 10
# email: a@example.com

```

Will work with `json` or `yaml` files.

# Replace
Nested dictionaries are also merged unless the `Replace` directive is included.

```yaml
# yaml at base.yaml
parser: xyz
timeout: 10
email: a@example.com
nested:
  number: 42
    
# ... 

```

```yaml
parser: abc
nested:
  letter: k

__ConfigUtil_Directive:
  Update: [base.yaml]
  Replace: [['nested']] # list of list of key parameters 
```

In the updated config `nested` would be a `dict` just with the key `letter` not the default behavior of `letter` and `number`

**NOTE:**

Best practice is for the production config to be fully expanded and be the golden copy.

Config updates can be made out of band and diffed to ensure all changes were expected.

