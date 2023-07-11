# Senao Technical Assessment

## User Guide for Running Docker Container

##### - The following files are needed to run the container

1. docker-compose.yml
    - This file pulls and runs docker images of MySQL, Redis and [alisonmjc/senao_app:0.2.0](https://hub.docker.com/layers/alisonmjc/senao_app/0.2.0/images/sha256-611b8a9a826f8b91b83e3ee303953ad093257db76d71ed9d42795e6a4b78f2b9?context=explore)
2. docker-entrypoint-initdb.d > init.sql
    - This script file inits the database by setting up the necessary tables for MySQL
3. docker.env
    - dockerenv_template is provided on Github, follow the template to make your own docker.env
        ```bash
        DB_PORT='your port, e.g. 3306'
        DB_NAME='your db name'
        DB_USER='your username'
        DB_PASSWORD='your password'
        REDIS_PORT='your port e.g. 6379'
        REDIS_PASSWORD='your password'
        ```
4. Dockerfile
    - This file would only be needed when docker-compose.yml fails to pull alisonmjc/senao_app:0.2.0 from Docker hub. Otherwise, it’s not a necessary file.

##### - You can choose to either download above files from Github, or use git clone to get all files in one command.

```bash
git clone git@github.com:alison-chuang/senao.git
```

##### - Make sure all files are ready, and then run the following command :

```bash
docker-compose up
```

##### - After execution, there would be three containers(MySQL, Redis, app), they are attaching together.

---

## API DOC

#### 1. Create Account API

-   **Description**: Creates a new user account with the provided username and password.
-   **Endpoint**: `/accounts`
-   **Method**: POST

-   **Request Body**:

| Field    | Type   | Requirement                                                                                                                                      |
| -------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| username | String | a minimum length of 3 characters and a maximum length of 32 characters                                                                           |
| password | String | a minimum length of 8 characters and a maximum length of 32 characters, containing at least 1 uppercase letter, 1 lowercase letter, and 1 number |

```json
example:
{
    "username": "alison",
    "password": "1234Qwer"
}
```

-   **Success Response: 201**

| Field   | Type    | Description |
| ------- | ------- | ----------- |
| success | Boolean | True        |

-   **Client Error Response: 400**

| Field   | Type    | Description   |
| ------- | ------- | ------------- |
| success | Boolean | False         |
| reason  | String  | Error message |

-   **Server Error Response: 500**

| Field   | Type    | Description   |
| ------- | ------- | ------------- |
| success | Boolean | False         |
| reason  | String  | Error message |

#### 2. Verify Account API

-   **Description**: Verifies the provided username and password.
-   **Endpoint**: `/accounts/verification`
-   **Method**: POST

-   **Request Body**:

```json
example
    {
    "username": "string",
    "password": "string"
    }
```

-   **Success Response: 200**

| Field   | Type    | Description |
| ------- | ------- | ----------- |
| success | Boolean | True        |

-   **Client Error Response (incorrect request body): 400**

| Field   | Type    | Description   |
| ------- | ------- | ------------- |
| success | Boolean | False         |
| reason  | String  | Error message |

-   **Client Error Response (Invalid username or password): 401**

| Field   | Type    | Description   |
| ------- | ------- | ------------- |
| success | Boolean | False         |
| reason  | String  | Error message |

-   **Client Error Response: 429**

| Field   | Type    | Description   |
| ------- | ------- | ------------- |
| success | Boolean | False         |
| reason  | String  | Error message |

-   **Server Error Response: 500**

| Field   | Type    | Description   |
| ------- | ------- | ------------- |
| success | Boolean | False         |
| reason  | String  | Error message |
