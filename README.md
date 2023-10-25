# foiaonline

This repository contains a utility that was used for collecting data from [foiaonline.gov](https://foiaonline.gov) which was shut down on September 30, 2023[^1]. Despite the fact that it came online in 2012, searching in the interface found that there were records received going back as far as March 4, 2003.

The `pull.py` program interacted with the foiaonline.gov [Advanced Search Form] by requesting one week's worth of records at a time, starting on March 1, 2003. This was to get around a result size limit of 10,000 records. It retrieved the JSON from the API that was provided for paging through results. The records retrieved are then written to a JSONL file `data.jsonl`, which was gzipped on completion, and is present here as well.

More about this process can be found in this post:

[https://inkdroid.org/2023/10/01/foiaonline/](https://inkdroid.org/2023/10/01/foiaonline/)

## Run

```
$ poetry install
$ poetry run pull.py
```

... wait a couple days

## Analysis

The resulting `data.jsonl.gz` is provided here for research purposes as it is in the [Public Domain](https://en.wikipedia.org/wiki/Copyright_status_of_works_by_the_federal_government_of_the_United_States). As an example some basic analysis of request frequency, agencies, and determinations can be found in the Jupyter Notebook:

```
$ poetry run jupyter lab Notebook.ipynb
```

Or you can [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/edsu/foiaonline/blob/main/Notebook.ipynb)

## Archive Team

The ArchiveTeam and Internet Archive have also done some collecting prior to shutdown which you can find described on [this wiki page](https://wiki.archiveteam.org/index.php/FOIAonline). The resulting WARC data that was collected can be found by [searching](https://archive.org/details/archiveteam-fire?query=foiaonline.gov) the ArchiveTeam Just In Time Grabs collection for "foiaonline.gov".

[Advanced Search form]: https://foiaonline.gov/foiaonline/action/public/search/advancedSearch

[^1]: https://www.archives.gov/ogis/resources/foia-ombuds-observer/2023-01
