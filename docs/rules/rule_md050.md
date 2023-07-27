# # Rule - MD050

| Aliases |
| --- |
| `md050` |
| `refs-regex` |

## Summary

References should match the configured regexes.

## Reasoning

Larger projects or organisations may have rules and requirements regarding the
format or content of references. The markdown may need to be viewable offline 
or outside a company network.

## Examples

This rule fails whenever a reference doesn't match one of the configured regexes.
For instance, a regex that disallows all URIs using HTTP. 

Configuration:
```json
"md050": {
    "enabled": true,
    "regexes": {
        "1": {
            "regex": "^(https?:)?(\/\/)?",
            "errorMessage": "No external web links",
        }
    },
}

```


````Markdown
[some-image](https//example.com/funny-cat.jpg)

````

## Configuration

| Prefixes              |
|-----------------------|
| `plugins.md050.`      |
| `plugins.refs-regex.` |

| Value Name | Type             | Default     | Description                                                     |
|------------|------------------|-------------|-----------------------------------------------------------------|
| `enabled`  | `boolean`        | `false`     | Whether the plugin rule is enabled.                             |
| `regexes`  | dict (see below) | `undefined` | A dictionary of pairs of regex and corresponding error message. |

It's important to use sequential indices (1, 2, 3...) as the keys, otherwise the
config won't be parsed properly.

```json
"regexes": {
  "1": {
      "regex": "^(https?:)?(\/\/)?",
      "errorMessage": "No external web links",
  },
  "2": {
      "regex": "[0-9+]",
      "errorMessage": "No numbers",
  }
}
```
