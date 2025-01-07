""" SWTP_Ebner_WiSe23_Getraenkemaschine
Frontend JSON schema definitions

Version 0.1
Licence: MIT
"""

import enum

class SCHEMA(enum.Enum):

    # ---- get ----

    get_bottle = {
        "type" : "object",
        "properties" : {
            "bottleID" : {
                "type": "array",
                "items": {
                    "type": "integer",
                    "exclusiveMinimum": 0
                },
                "minItems": 1
            },
            "categoryID" : {
                "type": "array",
                "items": {
                    "type": "integer",
                    "exclusiveMinimum": 0
                },
                "minItems": 1
            },
            "machineID" : {
                "type": "array",
                "items": {
                    "type": "integer",
                    "exclusiveMinimum": 0
                },
                "minItems": 1
            },
            "includeAlc" : {
                "type": "boolean"
            }
        }
    }

    get_machine = {
        "type" : "object",
        "properties" : {
            "machineID" : {
                "type": "array",
                "items": {
                    "type": "integer",
                    "exclusiveMinimum": 0
                },
                "minItems": 1
            }
        }
    }

    get_category = {
        "type" : "object",
        "properties" : {
            "parent_categoryID" : {
                "type": "integer",
                "exclusiveMinimum": 0
            }
        }
    }

    get_recipe = {
        "type" : "object",
        "properties" : {
            "categoryID" : {
                "type": "array",
                "items": {
                    "type": "integer",
                    "exclusiveMinimum": 0
                },
                "minItems": 1
            },
            "contains_categoryID" : {
                "type": "array",
                "items": {
                    "type": "integer",
                    "exclusiveMinimum": 0
                },
                "minItems": 1
            },
            "producable_by_machineID" : {
                "type": "integer",
                "exclusiveMinimum": 0
            },
            "includeAlc" : {
                "type": "boolean"
            }
        }
    }

    get_glass = {
        "type": "object",
        "properties": {
            # no filter options yet
        }
    }


    # ---- create ----

    create_order = {
        "type" : "object",
        "properties" : {
            "machineID" : {
                "type": "integer",
                "exclusiveMinimum": 0
            },
            "recipeID" : {
                "type": "integer",
                "exclusiveMinimum": 0
            }
        },
        "required": [
		"machineID", "recipeID"
	    ]
    }

    create_customorder = {
        "type" : "object",
        "properties" : {
            "machineID" : {
                "type": "integer",
                "exclusiveMinimum": 0
            },
            "value" : {
                "type": "array",
                "items" : {
                    "type": "object",
                    "properties": {
                        "bottleID": {
                            "type": "integer",
                            "exclusiveMinimum": 0
                        },
                        "amount_ml": {
                            "type": "integer",
                            "exclusiveMinimum": 0
                        }
                    },
                    "required": [
                        "bottleID", "amount_ml"
                    ]
                },
                "minItems": 1
            },
        },
        "required": [
		"machineID", "value"
	    ]
    }

    create_bottle = {
        "type" : "object",
        "properties" : {
            "value" : {
                "type" : "object",
                "properties" : {
                    "categoryID" : {
                        "type": "integer",
                        "exclusiveMinimum": 0
                    },
                    "name" : {
                        "type": "string"
                    },
                    "density" : {
                        "type": "number",
                        "exclusiveMinimum": 0
                    },
                    "max_capacity" : {
                        "type": "integer",
                        "exclusiveMinimum": 0
                    },
                    "alcohol_percentage" : {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 100
                    },
                    "price" : {
                        "type": "number",
                        "minimum": 0
                    },
                    "pic_url" : {
                        "type": "string"
                    }
                },
                "required": [
                    "categoryID", "name", "density", "max_capacity", "alcohol_percentage", "price", "pic_url"
                ]
            }
        },
        "required": [
		"value"
	    ]
    }

    create_machine = {
        "type": "object",
        "properties": {
            "value": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string"
                    },
                    "bottle_items": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "position_cm": {
                                    "type": "integer"
                                },
                                "pump_pin": {
                                    "type": "integer"
                                },
                                "led_pin": {
                                    "type": "integer"
                                },
                                "bottleID": {
                                    "type": "integer",
                                    "exclusiveMinimum": 0
                                },
                                "current_capacity": {
                                    "type": "integer",
                                    "minimum": 0
                                }
                            },
                            "required": [
                                "position_cm", "pump_pin", "led_pin", "current_capacity", "bottleID"
                            ]
                        },
                        "minItems": 1
                    }
                },
                "required": [
                    "name"
                ]
            }
        },
        "required": [
            "value"
        ]
    }

    create_category = {
        "type": "object",
        "properties": {
            "value": {
                "type": "object",
                "properties": {
                    "parent_categoryID": {
                        "type": "integer",
                        "exclusiveMinimum": 0
                    },
                    "name": {
                        "type": "string"
                    }
                },
                "required": [
                    # parent_categoryID is not required because not every category is a sub-category
                    "name"
                ]
            }
        },
        "required": [
		"value"
	    ]
    }

    create_recipe = {
        "type": "object",
        "properties": {
            "value": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string"
                    },
                    "price": {
                        "type": "number",
                        "minimum": 0
                    },
                    "pic_url": {
                        "type": "string"
                    },
                    "categoryID": {
                        "type": "integer",
                        "exclusiveMinimum": 0
                    },
                    "glassID": {
                        "type": "integer",
                        "exclusiveMinimum": 0
                    },
                    "recipe_items": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "categoryID": {
                                    "type": "integer",
                                    "exclusiveMinimum": 0
                                },
                                "amount_ml": {
                                    "type": "integer",
                                    "exclusiveMinimum": 0
                                }
                            },
                            "required": [
                                "categoryID", "amount_ml"
                            ]
                        },
                        "minItems": 1
                    }
                },
                "required": [
                    "name", "price", "pic_url", "categoryID", "glassID", "recipe_items"
                ]
            }
        },
        "required": [
            "value"
        ]
    }

    create_rating = {
        "type": "object",
        "properties": {
            "recipeID": {
                "type": "integer",
                "exclusiveMinimum": 0
            },
            "rating_value": {
                "type": "integer",
                "minimum": 1,
                "maximum": 5
            }
        },
        "required": [
            "recipeID", "rating_value"
        ]
    }

    create_glass = {
        "type": "object",
        "properties": {
            "value": {
                "type": "object",
                "properties": {
                    "amount_ml": {
                        "type": "integer",
                        "exclusiveMinimum": 0
                    },
                    "weight_g": {
                        "type": "integer",
                        "exclusiveMinimum": 0
                    }
                },
                "required": [
                    "amount_ml", "weight_g"
                ]
            }
        },
        "required": [
		"value"
	    ]
    }


    # ---- update ----

    update_bottle = {
        "type" : "object",
        "properties" : {
            "bottleID": {
                "type": "integer",
                "exclusiveMinimum": 0
            },
            "value" : {
                "type" : "object",
                "properties" : {
                    "categoryID" : {
                        "type": "integer",
                        "exclusiveMinimum": 0
                    },
                    "name" : {
                        "type": "string"
                    },
                    "density" : {
                        "type": "number",
                        "exclusiveMinimum": 0
                    },
                    "max_capacity" : {
                        "type": "integer",
                        "exclusiveMinimum": 0
                    },
                    "alcohol_percentage" : {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 100
                    },
                    "price" : {
                        "type": "number",
                        "minimum": 0,
                    },
                    "pic_url" : {
                        "type": "string"
                    }
                },
                "minProperties": 1
            }
        },
        "required": [
		"bottleID", "value"
	    ]
    }

    update_machine = {
        "type" : "object",
        "properties" : {
            "machineID": {
                "type": "integer",
                "exclusiveMinimum": 0
            },
            "value" : {
                "type" : "object",
                "properties" : {
                    "name" : {
                        "type": "string"
                    },
                    "bottle_items": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "position_cm": {
                                    "type": "integer"
                                },
                                "pump_pin": {
                                    "type": "integer"
                                },
                                "led_pin": {
                                    "type": "integer"
                                },
                                "bottleID": {
                                    "type": "integer",
                                    "exclusiveMinimum": 0
                                },
                                "current_capacity": {
                                    "type": "integer",
                                    "minimum": 0
                                }
                            },
                            "required": [
                                "position_cm"
                            ]
                        },
                        "minItems": 1
                    }
                },
                "minProperties": 1
            }
        },
        "required": [
		    "machineID", "value"
	    ]
    }

    update_category = {
        "type": "object",
        "properties": {
            "categoryID": {
                "type": "integer",
                "exclusiveMinimum": 0
            },
            "value": {
                "type": "object",
                "properties": {
                    "parent_categoryID": {
                        # can be an integer (parent id) or null (to remove the parent relation)
                        "anyOf": [
                            {
                                "type": "integer",
                                "exclusiveMinimum": 0
                            },
                            {
                                "type": "null"
                            }
                        ]
                    },
                    "name": {
                        "type": "string"
                    }
                },
                "minProperties": 1
            }
        },
        "required": [
		"categoryID", "value"
	    ]
    }

    update_recipe = {
        "type": "object",
        "properties": {
            "recipeID": {
                "type": "integer",
                "exclusiveMinimum": 0
            },
            "value": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string"
                    },
                    "price": {
                        "type": "number",
                        "minimum": 0
                    },
                    "pic_url": {
                        "type": "string"
                    },
                    "categoryID": {
                        "type": "integer",
                        "exclusiveMinimum": 0
                    },
                    "glassID": {
                        "type": "integer",
                        "exclusiveMinimum": 0
                    },
                    "recipe_items": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "categoryID": {
                                    "type": "integer",
                                    "exclusiveMinimum": 0
                                },
                                "amount_ml": {
                                    "type": "integer",
                                    "exclusiveMinimum": 0
                                }
                            },
                            "required": [
                                "categoryID", "amount_ml"
                            ]
                        },
                        "minItems": 1
                    }
                },
                "minProperties": 1
            }
        },
        "required": [
           "recipeID", "value"
        ]
    }

    update_glass = {
        "type" : "object",
        "properties" : {
            "glassID": {
                "type": "integer",
                "exclusiveMinimum": 0
            },
            "value" : {
                "type" : "object",
                "properties" : {
                    "amount_ml" : {
                        "type": "integer",
                        "exclusiveMinimum": 0
                    },
                    "weight_g" : {
                        "type": "integer",
                        "exclusiveMinimum": 0
                    }
                },
                "minProperties": 1
            }
        },
        "required": [
		"glassID", "value"
	    ]
    }


    # ---- delete ----

    delete_bottle = {
        "type": "object",
        "properties": {
            "bottleID": {
                "type": "integer",
                "exclusiveMinimum": 0
            }
        },
        "required": [
            "bottleID"
        ]
    }

    delete_machine = {
        "type": "object",
        "properties": {
            "machineID": {
                "type": "integer",
                "exclusiveMinimum": 0
            }
        },
        "required": [
            "machineID"
        ]
    }

    delete_category = {
        "type": "object",
        "properties": {
            "categoryID": {
                "type": "integer",
                "exclusiveMinimum": 0
            }
        },
        "required": [
            "categoryID"
        ]
    }

    delete_recipe = {
        "type": "object",
        "properties": {
            "recipeID": {
                "type": "integer",
                "exclusiveMinimum": 0
            }
        },
        "required": [
            "recipeID"
        ]
    }

    delete_glass = {
        "type": "object",
        "properties": {
            "glassID": {
                "type": "integer",
                "exclusiveMinimum": 0
            }
        },
        "required": [
            "glassID"
        ]
    }


    # ---- check credentials as internal schema ----

    check_credentials = {
        "type": "object",
        "properties": {
            "name": {
                "type": "string"
            },
            "password": {
                "type": "string"
            }
        },
        "required": [
            "name", "password"
        ]
    }