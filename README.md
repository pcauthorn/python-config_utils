# configutils

Allows for composable configs

```yaml
# yaml at somelocation/config.yaml
parser: xyz
timeout: 10
email: a@example.com
# ... 

```

```yaml
parser: abc
__ConfigUtil_Directive:
  Update: [somelocation/config.yaml] # could have multiple
```

Would create a config with default values from first file with the ```parser``` set to ```abc```

Code would look like:
```
config = yaml.load('file path'...)
updater = ConfigUpdater()
new_config = updater.update_config(config)
```

Will work with `json` or `yaml` files.



####Replace
Nested dictionaries are also updated unless the `Replace` directive is included.

```yaml
# yaml at somelocation/config.yaml
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
  Update: [somelocation/config.yaml]
  Replace: [['nested']] # list of list of key parameters 
```

In the updated config `nested` would be a `dict` just with the key `letter` not the default behavior of `letter` and `number`


####Other formats
To use other formats or to store somewhere besides the filesystem pass in 
a custom `resolver` which takes the string from `Update` and returns a `dict`
of the config

DynamoDB might look like this:
```
class DynamoResolver:
    dif __init__(self...):
        # initialize connection/get table
    def get(name):
        response = table.get_item(
            Key={
                'config_name': name
            }
        )
        return response['Item']

```
Could be used like this:
```
dynamo_resolver = DynamoResolver(...)
config =  dynamo_resolver.get(<config name>)
updater = ConfigUpdater(resolver=dynamo_resolver)
new_config = updater.update_config(config)


```

**NOTE:**

Best practice is for the production config to be fully expanded and be the golden copy.

Config updates can be made out of band and diffed to ensure all changes were expected.

