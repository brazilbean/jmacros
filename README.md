# JMacros
A tool for defining and evaluating macros for JSON

## Macros

```yaml
foo:
  schema:
    type: object
    required: [bar, baz]
    properties:
      bar: {type: object}
      baz: {type: string}
  properties:
    "%": ${.baz}
  template:
    bar: ${.bar}
    baz: "${.baz} is baz"
```
### Template

## Algorithm

A macro can:
- modify the parent
  - dict: the macro result is a dict and adds 
  key-values to the parent
  - list: the macro result is a list and adds 
  items to the parent
- replace the macro instance
  - return a value, list, or dict
  
How do we know whether a macro instance should 
replace the value versus extend the parent?
- `__macro!` extends the parent
- `__macro` replaces the instance

### Traversal
You have a token:
- Is it a macro?
  - evaluate the macro
  - return the result + extends_parent
- Is it a dict?
  - replace the dict with a new one
  - for each key-value, get a list of key-values and add them
  - return the dict 
- Is it a list?
  - replace the list with a new one
  - for each item, get a list of items and add them
  - return the list
- Is it a value?
  - return the value
  
### Evaluating a macro
- Load definition
- Check input against schema
  - If schema is missing, accept any input
- Populate properties
- Populate template

### Properties
- Usage
  - Used within the template
  - Used by other properties
  - Used within the document
- Naming?
  - Named by key?
    - this can't be globally unique - would only work within the
    namespace of the sibling keys
  - global path?
    - this could get cumbersome
  - perhaps absolute refs and local refs
- Reference?
  - not jq - jq is too powerful
  - jsonPointer vs jsonPath
    - JsonPointer is used in schemas. '#' gets cumbersome in yaml
    - use JsonPath
  - ${}?
    - `${$.foo.bar}` - absolute ref, looks awkward with two `$`
    - `${foo.bar}` - local ref
    - Use `${}` for both in-macro and in-document references?
      - `${}` is nice because it is not likely to interfere with
      yaml/markdown/json syntax
      
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
