# *Arr Cleaner

*Arr Cleaner is a Python script designed to clean stalled downloads in Sonarr and Radarr. 
It periodically checks the download queue for stalled items and removes them using CRUD requests.

Original code forked from [MattDGTL](https://github.com/MattDGTL/sonarr-radarr-queue-cleaner).

## Prerequisites

Before running the script, ensure you have the following prerequisites installed:

- Docker *(to run the script in a container, no Python needed)*
- Python 3.9 or higher *(to run the script directly, Python needed)*

## Getting Started

To get started with ***Arr Cleaner**, follow these steps:

1. Clone this repository to your local machine.

2. Clone `example.env` in to a new file called `.env` and edit its contents.

### (option 1): Using Docker:

3. Start a docker container:

```sh
docker-compose up -d --build
```

### (option 2): Run directly using python:

3. Run the script directly:
```sh
python main.py
```

## Installing updates

1. Run `git pull` in the root folder
2. Use whatever method you used to start the script from the previous section

## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
