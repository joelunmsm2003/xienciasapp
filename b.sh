

curl --header 'Access-Token: o.CkwgbghQdKuxqT5bxubgavgiCYMFhbeN' \
     --header 'Content-Type: application/json' \
     --data-binary '{"body":"'" $body"'","title":"'"$title"'","type":"note"}' \
     --request POST \
     https://api.pushbullet.com/v2/pushes
