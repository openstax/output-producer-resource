# workflow-event-resource

## Examples

```yaml
resource_types:
  - name: workflow-events
    type: docker-image
    source:
      repository: openstax/workflow-event-resource

resources:
  - name: workflow-events-queued
    type: workflow-events
    source:
      api_root: https://cc1.cnx.org/api
      status_id: 1

  - name: event-update
    type: workflow-events
    source:
      api_root: https://cc1.cnx.org/api
```

## `get`: Get the latest events from service

### Files created

* `id`: The event id
* `collection_id`: The collection id for the event
* `event.json`: All the api data for the event

### Example

```yaml
plan:
  - get: workflow-events-queued
    trigger: true
    version: every
```

## `put`: Update the event through the web api

* `status_id`: The id of the status to change the event
* `pdf_url`: The url location of the pdf on S3

### Example

```yaml
- put: event-update
  params:
    id: workflow-events-queued/id
    status_id: "2"
```

## Configure Dev Environment

Change into the workflow-event-resource working directory

`cd ./workflow-event-resource`

Create a virtualenv:

`python3 -m venv .venv`

Install dependencies:

`pip install .[dev]`

### Run unit tests

`make test`

### Build the docker image for development

`make build-image`

### Build the docker image tagged latest

`make tag-latest`

### Release the versioned image to dockerhub

`make release`

### Release the latest image to dockerhub

`make release-latest`
