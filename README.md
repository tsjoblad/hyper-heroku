# hyper-heroku

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/tsjoblad/hyper-heroku/edit/master)


## Description:
This is a proof-of-concept set of code that leverages Tableau's Hyper API and Heroku to create and deploy a **very** simple web application that published a Data Source scraped from a RESTful GET request. It was built on a live-coding demonstration for Tableau's DataDevs (our awesome developer community). Currently, the GET request is set up to pull a set of NBA games from a free API endpoint called [Free NBA](https://rapidapi.com/theapiguy/api/free-nba) by *The API Guy*. The script also leverages Will Ayd and innobi's [pantab](https://pantab.readthedocs.io/en/latest/) library, which is amazing--check it out! You'll also notice that I'm not much of a front-end dev (I'm a PM that codes for crying out loud!) so kindly take that part of it with a grain of salt. It's just to get you started using the Hyper API and Heroku!


## Modifying the GET Request:
In our `app.py` file, the get_data() call will likely need to be significantly modified in order to fit other uses cases. This has less to do with Tableau or Hyper, however, so I'll leave it to you to figure out how to get and shape the data properly.

## Deploying to Heroku:
To see the app in action, simply click the `Deploy` button above. After logging in or creating a free account, it will prompt you to fill in the following environmental variables that serve both to authenticate and help with the script as it pulls data from the web:

| Config Var | ex. | purpose |
|-|-|-|
| headers | {"x-rapidapi-key": "8fc50d58c9mshff9e92e71286d41p14294bjsnfbae10247997","x-rapidapi-host": "free-nba.p.rapidapi.com"} | Provides additional data for the GET request (like keys or tokens). Must be structured like a python `Dict`. |
| hyper_name | nba_data.hyper | Names the `.hyper` file. Must have file extension. |
| json_object | data | Helps parse the data from the JSON output of the REST request. See below screenshot. |
| personal_access_token | asdfaaljkdfs=fWGz1TPAH7hs1OzgcmORTfsrT5 | Token value provided for Tableau Auth. (Ex. is obviously fake). |
| project_name | My Heroku Project | Name of Tableau Project to publish the data source. |
| rest_url | https://free-nba.p.rapidapi.com/games | URL for GET request. May include auth token if not provided in header. |
| server_address | https://10ax.online.tableau.com/ | Server or Online address to publish to. |
| site_id | mytableausite | Name of the Server or Online Site to publish to. |
| token_name | myToken | Name of the Tableau PAT to use for auth. |

These can be modified in Heroku's Settings -> Config Vars.

### json_object Example:
As you can see below, what we actually want to pull out of the response body lives in the `data` object, hence we set our `json_object = 'data'`.

**Ex. Response Body:**
```json
{
	"data":[
		0:{
			"id":47179
			"date":"2019-01-30T00:00:00.000Z"
			"home_team": {...}
			"home_team_score":126
			"period":4
			"postseason":false
			"season":2018
			"status":"Final"
			"time":" "
			"visitor_team": {...}
			"visitor_team_score":94
		}
	]
	"meta":{
		"total_pages":49747
		"current_page":1
		"next_page":2
		"per_page":1
		"total_count":49747
	}
}
```

### Example App Flow
For info on how the code functions, you can refer to this (slightly out of date) process flow:

![App Flow](/static/app_flow.png)



It should not be deployed in a production sense without modification.
