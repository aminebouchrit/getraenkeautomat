# SWTP_Ebner_WiSe23 Backend

## Description

This is the backend component of a drink machine project. It provides an interface for managing bottles, machines, recipes and orders in a drink machine system. It also supports communication with the drink machine hardware component to start the orders.

The system is built with Python, utilizing the SQLAlchemy library for database access and management, as well as MQTT for communication with the frontend and the drink machine hardware component. The database is managed with MariaDB, and the system is containerized with Docker for easy deployment and scaling. Additionally, phpMyAdmin is used for database management and monitoring.

The system allows clients to perform CRUD operations on bottles, recipes, machines, and inventory items.

## Requirements

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

All other dependencies are automatically installed when the container images are built.

## Technologies and libraries

- [Python](https://www.python.org)
- [Docker](https://www.docker.com/) for containerization
- [MariaDB](https://mariadb.org/) as the database management system
- [phpMyAdmin](https://www.phpmyadmin.net/) for database monitoring
- [SQLAlchemy](https://www.sqlalchemy.org/) for database queries in Python
- [Paho](https://www.eclipse.org/paho/) for MQTT communication
- [pySerial](https://pyserial.readthedocs.io/en/latest/pyserial.html) for serial communication with the Arduino
- [jsonschema](https://python-jsonschema.readthedocs.io/en/stable/) for validating JSON messages

## Frontend interface

A description can be found in the [frontend interface definition](05_Documentation/00_Interface-to-Frontend.md).

## Contributing

If you'd like to contribute to the drink machine backend, please follow these steps:

1. Fork the repository on GitLab
2. Clone the forked repository to your local machine
3. Create a new branch for your changes (`git checkout -b my-new-feature`)
4. Make your changes and commit them (`git commit -am 'feat: add some feature'`). The commit message should follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification
5. Push your changes to your fork on GitLab (`git push origin my-new-feature`)
6. Create a merge request on GitLab to merge your changes into the main repository

## Authors and acknowledgment

This project was created by Marvin Manderscheid, Nils te Poel and Mohammed Chaibi.

## License

This project is licensed under the MIT License.
