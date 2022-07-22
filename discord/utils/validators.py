guild_config = {
        "$jsonSchema": {
        "bsonType": "object",
        "description": "Document which describes a guilds configuration.",
        "required": ["_id"],
        "properties": {
            "messageLog": {
                "description": ""
            },
            "messageLogIgnore": {
                "description": 'Represents a list of channels that can be ignored. Must be an array',
                "bsonType": 'array'
            },
            "muteRole": {
                "description": 'Represents mute role. Must be an int or long.',
                "bsonType": [
                    'int',
                    'long'
                ]
            },
            "linksDelete": {
                "description": 'Represents whether or not links should be deleted. Must be a boolean.',
                "bsonType": 'bool'
            },
            "welcomeChannel": {
                "description": 'Represents the welcome channel. Must be an int or long.',
                "bsonType": 'long'
            },
            "welcomeGreeting": {
                "description": 'Represents welcome message, must be a string',
                "bsonType": 'string'
            }
        }
    }
}
