RULES = {
    "OPEN_APPLICATION": [
        ["open", "<application>"],
        ["launch", "<application>"],
        ["start", "<application>"],
    ],

    "CLOSE_APPLICATION": [
        ["close", "<application>"],
        ["quit", "<application>"],
        ["exit", "<application>"],
    ],

    "SET_VOLUME": [
        ["set", "volume", "to", "<level>"],
        ["set", "volume", "<level>"],
        ["volume", "<level>"],
        ["volume", "to", "<level>"],

    ],

    "DECREASE_VOLUME": [
            ["decrease", "volume", "by", "<level>"],
            ["decrease", "volume", "<level>"],
    
        ],

    "INCREASE_VOLUME": [
            ["increase", "volume", "by", "<level>"],
            ["increase", "volume", "<level>"],
    
        ],

    "MUTE":[
        ["mute"],
        ["unmute"]
    ],

    "SET_BRIGHTNESS": [
            ["set", "brightness", "to", "<level>"],
            ["set", "brightness", "<level>"],
            ["brightness", "<level>"],
        ],

    "DECREASE_BRIGHTNESS": [
            ["decrease", "brightness", "by", "<level>"],
            ["decrease", "brightness", "<level>"],
    
        ],
    
    "INCREASE_BRIGHTNESS": [
            ["increase", "brightness", "by", "<level>"],
            ["increase", "brightness", "<level>"],
    
        ],

    "SYSTEM_POWER_CONTROL": [
        ["<command>","my","computer"],
        ["<command>","down","my","computer"],
        ["<command>","my","pc"],
        ["<command>","down","my","pc"],
        ["<command>","my","laptop"],
        ["<command>","down","my","laptop"],
        ["<command>","my","computer"],
        ["<command>","my","pc"],
        ["<command>","my","laptop"],
        ["put","my","computer","to","<command>"],
        ["put","my","pc","to","<command>"],
        ["put","my","laptop","to","<command>"],
        ["<command>","my","computer"],
        ["<command>","my","pc"],
        ["<command>","my","laptop"],

    ]

    # "WEB_SEARCH": [
    #     ["search", "<query>"],
    #     ["search", "for", "<query>"],
    # ],
}