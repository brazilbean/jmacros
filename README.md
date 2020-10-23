# JMacros
A tool for defining and evaluating macros for JSON
   
## Use cases
- AWS Step Functions
- AWS Cloudformation
- Document generation
  - Root of document is a macro that joins array to yield a single string
- Any json/yaml DSL      

## Installation

```bash
pip install git+https://github.com/brazilbean/jmacros.git
```

*TODO: get this into pypi*

**Requires `jq` to be available on the PATH.**  
In theory (not tested yet, but the code is there),
you can also `pip install jq` for a more efficient performance.

## Usage
*A cleaner API is coming. For now, you get to use `traverse` directly.*

```python
from jmacros import traversal, macros
macro_defs = {
  "hello": {
    "template": "Hello ${.name}!"
  }
}
macros = [
  macros.ClassMacro(macro_defs)
]
obj = {
  "foo": {"__macro": "hello", "name": "World"}
}
result, _ = traversal.traverse(obj, macros, [])
assert result == {"foo": "Hello World!"}
```

## Built-in Macros

*More are coming.*
- File import (as text, as object)
- Properties on class macros

### Class Macro

You define the class macro definitions. 
These are templates that can reference inputs with
`jq` expressions in 
`${}` string interpolation
or `{"__jq":"<jq expr>"` syntax.

The class macro definition can include a schema 
(defined in **json-schema**) that describes the
inputs to the macro.

For example, given a macro definition:
```yaml
example:
  schema:
    type: object
    required: [name, number, stuff]
    properties: 
      name: {type: string}
      number: {type: number}
      stuff: {type: object}
  template:
    name: The name is ${.name}
    number: The number is ${.number}
    stuff: {__jq: .stuff}
```
The following:
```yaml
doc: {__macro: example, name: Bob, number: 7, stuff: {foo: bar}}
```
becomes:
```yaml
doc:
  name: The name is Bob
  number: The number is 7
  stuff:
    foo: bar
```

## Examples

*See also: [the tests](/tests)*

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
