# Sudoku REST API

This project exposes [sudoku solver](https://github.com/navshaikh/sudoku) as a REST API. It is based on [Flask](https://flask.pocoo.org/).

The API currently exposes a single REST endpoint, which expects a POST request with sudoku input represented as an 81-character string. This API also supports batch request.

## Launching the API using Docker

The simplest way to launch the API is using [Docker](https:/www.docker.com/) as shown below.

```bash
git clone https://github.com/navshaikh/sudoku-api.git && cd sudoku-api
docker build -t sudoku-api .
```

Once the Docker image is built, launch the container:

`docker run -p 5000:5000 sudoku-api`

## Launching the API manually

This approach works best with [virtualenv](https://virtualenv.pypa.io/en/latest/). Follow the [installation](https://virtualenv.pypa.io/en/latest/installation/) section if you do not have virtualenv installed.

```
git clone https://github.com/navshaikh/sudoku-api.git sudoku-api && cd sudoku-api
git clone https://github.com/navshaikh/sudoku.git
virtualenv env
source env/bin/activate
pip install -r requirements.txt
flask run
```

## Resource URL

By default, the endpoint is exposed on the localhost at:

`http://127.0.0.1:5000`

## Resource Information
|&nbsp; | &nbsp;|
| ------------- |-------------|
| Verb   | POST |
| Format | JSON or Key-value |
| Content-Type | application/json or application/x-www-form-urlencoded |

## Example Requests

Let's work with this sudoku. Cells with clues are filled with digits [1-9] and empty cells have `.`.
```
9  7  1  |  5  .  .  |  8  4  2
.  .  6  |  9  .  .  |  .  1  .
.  .  .  |  8  .  2  |  .  .  9
--------------------------------
5  .  .  |  .  .  .  |  7  9  .
.  .  7  |  6  .  8  |  3  .  .
.  2  8  |  .  .  .  |  .  .  5
--------------------------------
7  .  .  |  1  .  5  |  .  .  .
.  4  .  |  .  .  9  |  1  .  .
8  1  9  |  .  .  7  |  2  5  4
```

The above sudoku can be represented as an 81-character string.
`9715..842..69...1....8.2..95.....79...76.83...28.....57..1.5....4...91..819..7254`

NOTE that *sudoku* is a mandatory *key* in all the following formats.

#### Form-based request

`curl -X POST -d "sudoku=9715..842..69...1....8.2..95.....79...76.83...28.....57..1.5....4...91..819..7254" http://127.0.0.1:5000`

#### JSON-based request

`curl -H 'Content-Type: application/json' -X POST -d '{"sudoku":["9715..842..69...1....8.2..95.....79...76.83...28.....57..1.5....4...91..819..7254"]}' http://127.0.0.1:5000`

#### Batch request
`curl -H 'Content-Type: application/json' -X POST -d '{"sudoku":["9715..842..69...1....8.2..95.....79...76.83...28.....57..1.5....4...91..819..7254", ".1...8...3.472169...6....1....9.253..421.378..358.6....9....1...213874.9...5...2."]}' http://127.0.0.1:5000`

#### File-based request
Assuming that sudoku puzzles are in a file location `data/easy_10_sudoku.json`

`curl -H 'Content-Type: application/json' -X POST -d @data/easy_10_sudoku.json http://127.0.0.1:5000`

## Example Responses

Response is always a JSON-based list. Each element of the list is the *input* puzzle, *solution* (set to None if not solved), *status* code (OK or ERROR) and *message* (if there is an error). If the client sends a bad request (e.g: missing Content-Type or missing sudoku key), the server sends a HTTP 400 (Bad Request) detailing the error.

#### Success response
```json
{
  "data":[
      {
        "puzzle":"9715..842..69...1....8.2..95.....79...76.83...28.....57..1.5....4...91..819..7254",
        "solution":"971536842286974513354812679563421798497658321128793465732145986645289137819367254",
        "status":"OK",
        "message":null
      }
  ]
}
```

#### Error scenario
```json
{
  "data":[
    {
      "puzzle":"9715..842..69...1....8.2..95.....79...76.83...28.....57..1.5....4...91..819..725",
      "solution":null,
      "status":"Error",
      "message":"Invalid sudoku. Input must be 81 chars (80 provided)"
    }
  ]  
}
```
