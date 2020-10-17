# JMacros
A tool for defining and evaluating macros for JSON

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
  
### Getting a list of items/key-values
Is the item 

Macro:
```yaml
foobar:
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
