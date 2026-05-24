---
title: Event Stream Query Language
excerpt: ''
deprecated: false
hidden: false
metadata:
  title: ''
  description: ''
  robots: index
next:
  description: ''
---
## Overview

Once you have an Event Stream created, you may have a high volume of results to query. Follow this guide to learn our query language and how to use it to find what you need.

### General Principles

Using Event Streams, you can address any property of an object from an event like this:

```
property_name.property_name
```

Then it can be compared using the = sign:

```
property_name.property_name=value
```

It also supports multiple conditions separated by | (the idea is similar with pipe from linux):

```
property_name.property_name=value | property_name.property_name_2=another_value
```

### Examples

```
raw_data.coupon_code=RET300
data.partner_conversion_id=1761917939
event_time=2024-10-09T18:42:.*
raw_data.coupon_code=RET300 | event_time=2024-10-09T18.*
event_context.source_ips[0].address =93.175.44.65
$.event_context.source_ips[?('93.175.44.65' in @.address)]
$.person_profile.identity.steps[?(@.id == '123')] | $.type = .*_REWARD
```

### Query Language

A JSONPath expression specifies a path to an element (or a set of elements) in a JSON structure. 

Paths can use the dot notation:

```
$.store.book[0].title
```

Or the bracket notation:

```
$['store']['book'][0]['title']
```

Or a mix of dot and bracket notations:

```
$['store'].book[0].title
```

> 📘 Important notes
>
> * Dots are only used before property names not in brackets.
> * The leading `$` represents the root object or array and can be omitted. For example, `$.foo.bar` and `foo.bar` are the same, and so are `$[0].status` and `[0].status`.

#### Other syntax elements

<Table>
  <thead>
    <tr>
      <th>
        Expression
      </th>

      <th>
        Description
      </th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>
        `$`
      </td>

      <td>
        The root object or array.
      </td>
    </tr>

    <tr>
      <td>
        `.property`
      </td>

      <td>
        Selects the specified property in a parent object.
      </td>
    </tr>

    <tr>
      <td>
        `['property']`
      </td>

      <td>
        Selects the specified property in a parent object. Be sure to put single quotes around the property name.  

        Tip: Use this notation if the property name contains special characters such as spaces, or begins with a character other than `A..Za..z\_`.
      </td>
    </tr>

    <tr>
      <td>
        `[n]`
      </td>

      <td>
        Selects the n-th element from an array. Indexes are 0-based.
      </td>
    </tr>

    <tr>
      <td>
        `[index1,index2,…]`
      </td>

      <td>
        Selects array elements with the specified indexes. Returns a list.
      </td>
    </tr>

    <tr>
      <td>
        `..property`
      </td>

      <td>
        Recursive descent: Searches for the specified property name recursively and returns an array of all values with this property name. Always returns a list.
      </td>
    </tr>

    <tr>
      <td>
        `*`
      </td>

      <td>
        Wildcard selects all elements in an object or an array, regardless of their names or indexes. For example, `address._`means all properties of the address object, and `book[_]` means all items of the book array.
      </td>
    </tr>

    <tr>
      <td>
        `[start:end]`
      </td>

      <td>
        Selects array elements from the start index and up to, but not including, the end index. Returns a list.
      </td>
    </tr>

    <tr>
      <td>
        `[start:]`
      </td>

      <td>
        Selects array elements from the start index until the end of the array. If end is omitted, selects all elements from start until the end. Returns a list.
      </td>
    </tr>

    <tr>
      <td>
        `[:n]`
      </td>

      <td>
        Selects the first n elements of the array. Returns a list.
      </td>
    </tr>

    <tr>
      <td>
        `[-n:]`
      </td>

      <td>
        Selects the last n elements of the array. Returns a list.
      </td>
    </tr>

    <tr>
      <td>
        `[?(expression)]`
      </td>

      <td>
        Filter expression. Selects all elements in an object or array that match the specified filter. Returns a list.
      </td>
    </tr>

    <tr>
      <td>
        `[(expression)]`
      </td>

      <td>
        Script expressions can be used instead of explicit property names or indexes. An example is `[(@.length-1)]` which selects the last item in an array.  

        Here, length refers to the length of the current array rather than a JSON field named length.
      </td>
    </tr>

    <tr>
      <td>
        `@`
      </td>

      <td>
        Used in filter expressions to refer to the current node being processed.
      </td>
    </tr>
  </tbody>
</Table>

> 📘 Important Notes
>
> * JSONPath expressions, including property names and values, are case-sensitive.
> * Unlike XPath, JSONPath does not have operations for accessing parent or sibling nodes from the given node.

### Filters

Filters are logical expressions used to filter arrays. 

An example of a JSONPath expression with a filter is:

```
$.store.book[?(@.price < 10)]
```

Here, the `@` represents the current array item or object being processed. 

Filters can also use `$` to refer to the properties outside of the current object:

```
$.store.book[?(@.price < $.expensive)]
```

An expression that specifies just a property name, such as `[?(@.isbn)]`, matches all items that have this property, regardless of the value.

#### Operators that can be used in filters

<Table align={["left","left"]}>
  <thead>
    <tr>
      <th>
        Operator
      </th>

      <th>
        Description
      </th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>
        `==`
      </td>

      <td>
        Equals to. String values must be enclosed in single quotes (not double quotes): `[?(@.color=='red')]`.
      </td>
    </tr>

    <tr>
      <td>
        `!=`
      </td>

      <td>
        Not equal to. String values must be enclosed in single quotes: `[?(@.color!='red')]`.
      </td>
    </tr>

    <tr>
      <td>
        `>`
      </td>

      <td>
        Greater than.
      </td>
    </tr>

    <tr>
      <td>
        `>=`
      </td>

      <td>
        Greater than or equal to.
      </td>
    </tr>

    <tr>
      <td>
        `<`
      </td>

      <td>
        Less than.
      </td>
    </tr>

    <tr>
      <td>
        `<=`
      </td>

      <td>
        Less than or equal to.
      </td>
    </tr>

    <tr>
      <td>
        `=~`
      </td>

      <td>
        Matches a JavaScript regular expression. For example, `[?(@.description =~ /cat.*/i)]` matches items whose description starts with cat (case-insensitive).
      </td>
    </tr>

    <tr>
      <td>
        `!`
      </td>

      <td>
        Used to negate a filter: `[?(!@.isbn)]` matches items that do not have the isbn property.
      </td>
    </tr>

    <tr>
      <td>
        `&&`
      </td>

      <td>
        Logical AND, used to combine multiple filter expressions: `[?(@.category=='fiction' && @.price < 10)]`
      </td>
    </tr>

    <tr>
      <td>
        `|\|`
      </td>

      <td>
        Logical OR, used to combine multiple filter expressions:  

        `[?(@.category=='fiction' \|| @.price < 10)]`
      </td>
    </tr>

    <tr>
      <td>
        `in`
      </td>

      <td>
        Checks if the left-side value is present in the right-side list. Similar to the SQL IN operator. String comparison is case-sensitive.
      </td>
    </tr>

    <tr>
      <td>

      </td>

      <td>
        Examples: `[?(@.size in ['M', 'L'])]`, `[?('S' in @.sizes)]`
      </td>
    </tr>

    <tr>
      <td>
        `nin`
      </td>

      <td>
        Opposite of `in`. Checks that the left-side value is not present in the right-side list. String comparison is case-sensitive.
      </td>
    </tr>

    <tr>
      <td>

      </td>

      <td>
        Examples: `[?(@.size nin ['M', 'L'])]`, `[?('S' nin @.sizes)]`
      </td>
    </tr>

    <tr>
      <td>
        `subsetof`
      </td>

      <td>
        Checks if the left-side array is a subset of the right-side array. The actual order of array items does not matter. String comparison is case-sensitive. An empty left-side array always matches.
      </td>
    </tr>

    <tr>
      <td>

      </td>

      <td>
        Examples: `[?(@.sizes subsetof ['M', 'L'])]` – matches if sizes is `['M']`, `['L']`, or `['L', 'M']`. `[?(['M', 'L'] subsetof @.sizes)]` – matches if sizes contains at least 'M' and 'L'.
      </td>
    </tr>

    <tr>
      <td>
        `contains`
      </td>

      <td>
        Checks if a string contains the specified substring (case-sensitive), or an array contains the specified element.
      </td>
    </tr>

    <tr>
      <td>

      </td>

      <td>
        Examples: `[?(@.name contains 'Alex')]`, `[?(@.numbers contains 7)]`, `[?('ABCDEF' contains @.character)]`
      </td>
    </tr>

    <tr>
      <td>
        `size`
      </td>

      <td>
        Checks if an array or string has the specified length.  

        Example: `[?(@.name size 4)]`
      </td>
    </tr>

    <tr>
      <td>
        `empty true`
      </td>

      <td>
        Matches an empty array or string.  

        Example: `[?(@.name empty true)]`
      </td>
    </tr>

    <tr>
      <td>
        `empty false`
      </td>

      <td>
        Matches a non-empty array or string.  

        Example: `[?(@.name empty false)]`
      </td>
    </tr>
  </tbody>
</Table>

## Examples

For the following sample, we will use a modified version of JSON from [JSONPath - XPath for JSON](http://goessner.net/articles/JsonPath/index.html#e3).

```json
{
    "type": "STEP",
    "event_id": "7450517086735879321",
    "event_time": "2024-12-20T15:31:28.853Z",
    "request_time": "2024-12-20T15:31:28.866Z",
    "cause_event_id": "7450517084360984932",
    "root_event_id": "7450517084360984932",
    "event_sequence": 1,
    "schema_version": 25,
    "sandbox": {
        "sandbox_id": "production-production",
        "container": {
            "name": "production",
            "is_input_container": true
        },
        "sandbox_version": 0
    },
    "client_context": {
        "client_id": "123344",
        "client_short_name": "demo-client",
        "client_time_zone": "America/Chicago",
        "client_version": 76387
    },
    "client_domain_context": {
        "client_domain": "demo-client.extole.io",
        "client_domain_id": "f81241690d31beba7c250d95"
    },
    "event_context": {
        "input_event_type": "CONSUMER",
        "api_type": "CONSUMER",
        "device_id": {
            "id": "browser:7450512139203301734",
            "is_device_id_in_request": true
        },
        "page_id": {
            "id": "unspecified:7450517083409168381"
        },
        "user_id": null,
        "uri": "https://demo-client.extole.io/zone/bankable_rewards?email=earn_reward25@mailosaur.net&access_token=HASHED_SHA1(61dd1fe3ffaf9b763dc918b5855b471f01b27d3d)",
        "app_type": "Web",
        "app_data": {},
        "scopes": [
            "VERIFIED_CONSUMER",
            "UPDATE_PROFILE"
        ],
        "device_type": "Desktop",
        "device_os": "Unknown"
    },
    "data": {
        "source": "link:direct"
    },
    "log_messages": [
    ]
}
```

In all the expressions below, the leading $. is optional and can be omitted.

| Expression                                                    | Meaning                                           |
| :------------------------------------------------------------ | :------------------------------------------------ |
| `$.type = STEP`                                               | All events with type STEP                         |
| `$.name = advocate\_.\*`                                      | All events with name that starts with `advocate_` |
| `$.event_context.source_ips[?(@.address == '74.83.219.245')]` | All events originating from IP 74.83.112.245      |
