host="http://localhost:5000"
power_resource=${host}/api/v1/power

state=$1
json_payload="{\"state\": \"${state}\"}"

echo ${power_resource}
echo ${json_payload}


curl -H "Content-Type: application/json" -X POST "${power_resource}" -d "${json_payload}"