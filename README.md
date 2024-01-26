# *Arr Cleaner

*Arr Cleaner is a Python script designed to clean stalled downloads in Sonarr and Radarr. 
It periodically checks the download queue for stalled items and removes them.

Original code is from [MattDGTL](https://github.com/MattDGTL/sonarr-radarr-queue-cleaner).

## Prerequisites

Before running the script, ensure you have the following prerequisites installed:

- Docker *(to run the script in a container, no Python needed)*
- Python 3.9 or higher *(to run the script directly, Python needed)*

## Getting Started

To get started with ***Arr Cleaner**, follow these steps:

1. Clone this repository to your local machine.

### (option 1): Using Docker:

2. edit the docker compose file and make sure to replace "your_sonarr_url", "your_radarr_url", "your_sonarr_api_key", and "your_radarr_api_key" with your actual Sonarr and Radarr URLs and API keys. (See example values below in the python guide)

3. Start a docker container:

```sh
docker-compose up --build
```

### (option 2): Run directly using python:

2. Set up your environment variables by creating a `.env` file in the project directory. Here's an example `.env` file:

```env
SONARR_URL="http://sonarr:8989"
RADARR_URL="http://radarr:7878"
SONARR_API_KEY="abcd123456"
RADARR_API_KEY="abcd123456"
API_TIMEOUT="600" # seconds (600 sec = 10 min)
```

3. Run the script directly:
```sh
python main.py
```

or

```sh
python3 main.py
```

## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
