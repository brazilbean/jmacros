# JMacros
A tool for defining and evaluating macros for JSON
   
## Use cases
- AWS Step Functions
- AWS Cloudformation
- Document generation
  - Root of document is a macro that joins array to yield a single string
- Any json/yaml DSL      

## Examples

Macro:
```yaml
foobar:
  schema: {type: object}
  template: {a: b, c: d}
listbar:
  template: [1, 2, 3]

```
Usage:
```yaml
foo: bar
baz: {__macro!: foobar}
quux: {__macro: foobar}
```  
Result:
```yaml
foo: bar
a: b
c: d
quux: {a: b, c: d} 
```
Usage:
```yaml
foo: [a, {__macro!: listbar}, c]
bar: [a, {__macro: listbar}, c]
```
Result:
```yaml
foo: [a, 1, 2, 3, c]
bar: [a, [1, 2, 3], c]
```
