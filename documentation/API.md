# REST API documentation

## POST /rest/readers/:reader_id/events

Log a new event recorded through a tag reader.

* Content-Type: application/json
* Accept: application/json
* Body:

  ```json(strict)
  {
    "timestamp": 1526291678,
    "tag_id": "243F4AD56",
    "signature": "9234E84CBA42"
  }
  ```

  * timestamp  
  The timestamp encoded as a [POSIX timestamp](1) (number of seconds since epoch).
  * tag_id  
  The ID of the RFID tag that was 
  * signature  
  The signature is derived from signing the character string `<reader_id>#<timestamp>#<tag_id>`.

### Successful response

* Status: 201 Created
* Content-Type: application/json
* Header:
  * Location: a URI pointing to the created event

[1]: https://en.wikipedia.org/wiki/Unix_time