#!/bin/bash


# Retrieve user input from MongoDB
mongo_query="{ \"_id\": \"user_input\" }"
user_input=$(mongo HackKean --quiet --eval "db.inputs.findOne($mongo_query).input")

# Retrieve previous AQI from MongoDB
mongo_query="{ \"_id\": \"previous_aqi\" }"
previous_aqi=$(mongo HackKean --quiet --eval "db.aqis.findOne($mongo_query).aqi")

# Function to check AQI
function check_aqi {
    # Get current AQI
    current_aqi=$(python3 /Users/kyrollosgirgis/Documents/Coding/HackKean/script.WebScraping.py "$user_input")

    # Check if there is a jump of more than 50 in the AQI
    if (( $current_aqi - $previous_aqi > 50 )); then
        echo "Alert: AQI has jumped by more than 50 points."
    fi

    # Save current AQI as previous AQI in MongoDB
    mongo_query="{ \"_id\": \"previous_aqi\" }"
    mongo_update="{ \$set: { \"aqi\": $current_aqi } }"
    mongo HackKean --quiet --eval "db.aqis.updateOne($mongo_query, $mongo_update, { upsert: true })"
}

# Call function every 30 minutes
while true; do
    check_aqi
    sleep 1800
done
