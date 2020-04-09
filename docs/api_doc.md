**Settings**
----
  GET/POST json data about all settings.

* **URL**

  ``/api/v1/resources/settings``

* **Method:**

  `GET` | `POST`
  
* **Header:**
  
  Basic auth:
  ```javascript
  xhr.setRequestHeader("Authorization", "Basic " + btoa("user" + ":" + "password"))
  ```
* **GET Response:**

  * **Code:** 200 <br />
    **Content:** See file `config_muster.json`
 
* **POST Response:**
    * **Success Response:**

        * **Code:** 200 <br />
            **Content:** `{"status": "ok"}`
 
    * **Error Response:**

        * **Code:**  <br />
            **Content:** `{"status": "error_message_from_server"}`

* **Sample Call:**

  ```javascript
    const xhr = new XMLHttpRequest();
        const url = `http://127.0.0.1:5000/api/v1/resources/settings`
        xhr.open("GET", url);
        xhr.setRequestHeader("Authorization", "Basic " + btoa("user" + ":" + "password"))
        xhr.timeout = 2000
        xhr.send();

        xhr.onreadystatechange = (e) => {
            try {
                payload = JSON.parse(xhr.responseText)
                // do smt
            } catch (e) {
                // hm?
            }
        }
  ```
  <br>
----------------

**Getting/Posting word**
----
  GET/POST json data about single word.

* **URL**

  ``/api/v1/resources/dicts``

* **Method:**

  `GET` | `POST`
  
* **Header:**
  
  Basic auth:
  ```javascript
  xhr.setRequestHeader("Authorization", "Basic " + btoa("user" + ":" + "password"))
  ```
* **GET Request:**

  *  **Per URL:**<br>
      ``http://127.0.0.1:5000/api/v1/resources/dicts?dict_db=DE_FR&random=true``<br>
      ``http://127.0.0.1:5000/api/v1/resources/dicts?dict_db=DE_FR&id=1234``<br>
      Only support single word at once

  *  **Per JSON payload**:<br>
      ``http://127.0.0.1:5000/api/v1/resources/dicts``<br />
     **Payload JSON:**<br>
      ```json
      [
          {
              "dict_db": "DE_EN",
              "option": "",
              "ids": [
                  34,21
              ],
              "id_ranges": [
                  "10-25", "1000-1001"
              ],
              "id_random": 2
          },
          {
              "dict_db": "DE_FR",
              "option": "",
              "ids": [
                  3,11567,22,742,19346
              ],
              "id_ranges": [
                  "10-25", "1000-20000"
              ],
              "id_random": 0
          }
      ]
      ```

* **GET Response:**

  * **Code:** 200 <br />
    **Content:** <br>
    ``` json
    [
        {
            "dict_db": "DE_EN",
            "ids": [
                {
                    "id": 34,
                    "line": "word_34_for_DE_EN",
                    "note": "",
                    "description": "",
                    "date_created": "2020-04-09 11:38:01.888498",
                    "last_modified": "2020-04-09 11:38:01.888498"
                },
                {
                    "id": 21,
                    "line": "word_21_for_DE_EN",
                    "note": "",
                    "description": "",
                    "date_created": "2020-04-09 11:38:01.888498",
                    "last_modified": "2020-04-09 11:38:01.888498"
                }
            ],
            "id_ranges": {
              "1000-1001": [
                {
                    "id": 1000,
                    "line": "word_1000_for_DE_EN",
                    "note": "",
                    "description": "",
                    "date_created": "2020-04-09 11:38:01.888498",
                    "last_modified": "2020-04-09 11:38:01.888498"
                },
                {
                    "id": 1001,
                    "line": "word_1001_for_DE_EN",
                    "note": "",
                    "description": "",
                    "date_created": "2020-04-09 11:38:01.888498",
                    "last_modified": "2020-04-09 11:38:01.888498"
                }
              ],
              "10-25": ["....."]
            },
            "id_random": [
                {
                    "id": 65435,
                    "line": "word_65435_for_DE_EN",
                    "note": "",
                    "description": "",
                    "date_created": "2020-04-09 11:38:01.888498",
                    "last_modified": "2020-04-09 11:38:01.888498"
                },
                {
                    "id": 343,
                    "line": "word_343_for_DE_EN",
                    "note": "",
                    "description": "",
                    "date_created": "2020-04-09 11:38:01.888498",
                    "last_modified": "2020-04-09 11:38:01.888498"
                }
            ],
            "all": []
        }
    ]
    ```
 
* **POST Response:**
    * **Success Response:**

        * **Code:** 200 <br />
            **Content:** `{"status": "ok"}`
 
    * **Error Response:**

        * **Code:**  <br />
            **Content:** `{"status": "error_message_from_server"}`

* **Sample Call:**

  ```javascript
    const xhr = new XMLHttpRequest();
        const url = `http://127.0.0.1:5000/api/v1/resources/settings`
        xhr.open("GET", url);
        xhr.setRequestHeader("Authorization", "Basic " + btoa("user" + ":" + "password"))
        xhr.timeout = 2000
        xhr.send();

        xhr.onreadystatechange = (e) => {
            try {
                payload = JSON.parse(xhr.responseText)
                // do smt
            } catch (e) {
                // hm?
            }
        }
  ```