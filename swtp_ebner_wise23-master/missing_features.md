# Missing features

This list contains features that might be added in future software versions.

- User management
  - Saving of self-created recipes in the database
  - Favorite recipes
  - User reviews for recipes
  - Shopping cart managed by the backend
- Glass management
  - Ability to choose the glass used for an order
  - Ability to disable the glass weight check
- Security
  - Encryption of user passwords in the database
  - Encrypted MQTT communication
- Code
  - Additional unit tests for the backend
  - Clean separation between database queries and communication
  - Use SQLAlchemy to create the database tables
    (remove redundant definition in 02_Database/sql/00_init_db.sql and use python definition from SQLAlchemy)
- LED control based on the current bottle capacities in the database
- Change behavior when creating a new bottle: Take only the parent_categoryID for bottle and not the categoryID, because every bottle needs to have a category with the same name anyway.
