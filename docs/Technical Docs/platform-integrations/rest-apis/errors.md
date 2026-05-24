---
title: "Errors"
excerpt: "Brush up on common errors returned by our APIs.\n"
---

## Overview

[//]: # "I received an error, what should I do?"

This page offers an introduction to the most common errors you may encounter. In our API References, each endpoint lists all of its potential errors. If you receive an error that is not listed here, please look at the specific endpoint for more thorough documentation or reach out to [support@extole.com](mailto:support@extole.com).

[//]: ___

## Error Structure

[//]: # "What is Extole's error structure?"

The basic structure of an error response from Extole is that it will return a different HTTP code than “200”, typically in the 4xx or 500 range.

[//]: ___

## Standard Error Parameters

[//]: # "What are Extole's standard error parameters?"

<Table align={["left","left"]}>
  <thead>
    <tr>
      <th>
        Field   
      </th>

      <th>
        Description
      </th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>
        `unique_id`
      </td>

      <td>
        A unique error identifier from Extole that can be used by Extole to correlate this with the Extole error log.
      </td>
    </tr>

    <tr>
      <td>
        `http_status_code`  
      </td>

      <td>
        The HTTP status code that was returned.  In an error scenario it will be 4xx or 500 error.
      </td>
    </tr>

    <tr>
      <td>
        `code ` 
      </td>

      <td>
        A string enum for the error code:\
        `access_denied`\
        `missing_access_token`
      </td>
    </tr>

    <tr>
      <td>
        `message` 
      </td>

      <td>
        A human-readable error message.
      </td>
    </tr>

    <tr>
      <td>
        `parameters.reason`  
      </td>

      <td>
        Sub error: A string enum for an error condition.
      </td>
    </tr>

    <tr>
      <td>
        `parameters.description`  
      </td>

      <td>
        Sub error: A human-readable description of the error condition.
      </td>
    </tr>
  </tbody>
</Table>

[//]: ___

## Common Errors

[//]: # "What does this error mean?"

Each endpoint has unique errors, but below are several of the most common error conditions that are returned.

```json
{
  "unique_id": "6941047907334948670",
  "http_status_code": 400,
  "code": "validation_error",
  "message": "Validation failed",
  "parameters": {
    "description": "must not be null"
  }
}

```

```json
{
  "unique_id": "6941049359794271324",
  "http_status_code": 403,
  "code": "missing_access_token",
  "message": "No access_token was provided with this request.",
  "parameters": {}
}

```

```json
{
  "unique_id": "6928128588868954308",
  "http_status_code": 400,
  "code": "invalid_json",
  "message": "JSON is invalid",
  "parameters": {}
}

```

## 429 Too Many Requests

[//]: # "What is Extole's 429 error?"

| API          | Description                                                                                                                                                                                                                                       |
| :----------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Admin API    | If you are making too many requests too quickly we will start returning 429 requests. It is up to the API caller to retry these requests.                                                                                                         |
| Customer API | A 429 will be returned if more than 100 requests are made in one minute by a single IP address or token. We also cannot guarantee support above 10 requests per second per identified person. It is up to the API caller to retry these requests. |
