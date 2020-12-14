# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Endpoints
- GET  `/categories`
- GET  `/questions`
- GET `/categories/< id >/question`
- POST `/questions`
- POST `/questions/search`
- POST `/quizzes`
- DELETE `/questions/< id  >`
----

### GET `/categories`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category

-  **Request Arguments**: None

-  **Returns**: An object with a single key, categories, that contains a object of id: category_string key:value pairs.
```JSON
{
'1' : "Science",

'2' : "Art",

'3' : "Geography",

'4' : "History",

'5' : "Entertainment",

'6' : "Sports"
}
```

### Get `/questions`

- Fetches a list of all the available questions in the database, pagenated for 10 questions.

- A question object contains `id, question, answer, category, difficulty`

- **Request Arguments**: An *optional* page number Query Parameters, ex: `/questions?page=2`

-  **Returns**: An object with a key:values pair:
-- `questions`, A list of 10 questions objects
--  `total_questions`, number of all questions
--  `categories`, A list of all available categories

 ```JSON
{"categories":
 
			{"1": "Science",
				...},

"questions": [

		{"answer": "Apollo 13",

		"category": 5,

		"difficulty": 4,

		"id": 2,

		"question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
		},

		...

]

"success": true,

"total_questions": 19

}
```
-  **Expected erorrs**: If a page rquested that is out of questions range(which is 10 per page) will return a *404 error*

 &nbsp;

### GET `/categories/<id>/questions`

- Fetches questions based on category

-  **Request Arguments**: None

-  **Returns**: An object with a key:values pair:
--  `questions`, A list of 10 questions objects
--  `total_questions`: number of all questions
--  `current_category`' id of the requested category

-  **Expected erorrs**:

 -- If a page rquested is out of questions range(which is 10 per page) will return a *404 error*

-- Worng category id will return a *404 error*
&nbsp;
###  POST `/questions`
- Inserts a new question to the database
-  **Request Arguments**: the request should have a the following keys:
--  `question`, question string
-- `answer`, Answer String
-- `category`, Category integer ID
-- `difficulty`, Difficulty integer ID
Request example:
```JSON
{

'question':  'new question',

'answer':  'new answer',

'difficulty':  1,

'category':  1

}

```
- **Returns**: An object with a key:value pair of `'success: True'`
-  **Expected erorrs**: Any missing data or key with no value will return  an *422 error*
&nbsp;
### POST `/questions/search`
- Fetch questions based on a search term
-  **Request Arguments**: A key:value, in which the key is `searchTerm`, Example
```JSON
{
'searchTerm':  'Tom Hanks'
}
```
- **Returns**: An object with a key:values pairs:
-- `questions `, A list of questions objects 
-- `total_questions` number of all questions in the list
-  **Expected erorrs**:  when search for questions in not found, a *404 error* will be returned
&nbsp;
### POST `/quizzes`
- get questions to play the quiz
-  **Request Arguments**: This endpoint should take category and previous question parameters, example:
```JSON
{

'previous_questions':  [],

'quiz_category':  {'type':  "click",  'id':  0}

}
```
Note that a zero id referes to all the categorize 
- **Returns**: An object with a key:values pair:
-- `question` , a random questions within the given category
-  **Expected erorrs**: If the request is missing a parameter, it will return a *404 error*
&nbsp;
### DELETE `/questions/<id>`
- DELETE question using a question ID
- **Request Arguments**: None
- **Returns** A object with a key:value pair : `'success':  True`
-  -  **Expected erorrs**: If the id is not related to any question in the database, it will return an *404 error*


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
