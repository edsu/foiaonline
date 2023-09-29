# foiaonline

This repository contains a utility for collecting data from [foiaonline.gov](https://foiaonline.gov) which has been slated for shut down effective September 30, 2023[^1]. Despite the fact that it came online in 2012, searching in the interface found that there were records going received as far as March 4, 2003.

The `pull.py` program will interact with the foiaonline.gov [Advanced Search Form] requesting one week's worth of records at a time, starting on March 1, 2003. It retrieves the JSON from the API that is provided for paging through results. The records retrieved are then written to a JSONL file `data.jsonl`.

## Run

```
$ poetry install
$ poetry run pull.py
```

[^1]: https://www.archives.gov/ogis/resources/foia-ombuds-observer/2023-01
[Advanced Search form]: https://foiaonline.gov/foiaonline/action/public/search/advancedSearch
