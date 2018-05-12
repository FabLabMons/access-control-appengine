# REST API documentation

## Log tag seen

```
POST /rest/reader/<reader_id>/events
{
    "timestamp": "2018-05-12T10:25:32Z",
    "tag_id": "243F4AD56",
    "signature": "9234E84CBA42"
}
```

The signature is derived from signing the character string `<reader_id>#<timestamp>#<tag_id>`.
