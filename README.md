# smart-lab-system
The Smart Lab System is a multi-agent Raspberry Pi project designed for demonstration purposes in an AIoT course.

# System State
The system state is stored in a python dictionary. The dictionary is serialized to a JSON file and passed between agents. The dictionary has the following structure:
```json
{
    "member": [
        {
            "id": "0", // unique id of the member
            "name": "Jerry", // name of the member
            "status": 0, // 0: out, 1: in, 2: seated
            "seat_id": 0, // every seat has a unique id
        },
        {
            "id": "1",
            "name": "Shawn ",
            "status": 0,
            "seat_id": 1,
        },
    ]
}
```