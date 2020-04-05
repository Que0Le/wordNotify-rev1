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
  xhr.setRequestHeader("Authorization", "Basic " + btoa("user" + ":" + "password"))```
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
        const url = `http://127.0.0.1:5000//api/v1/resources/settings`
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