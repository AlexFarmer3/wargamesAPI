import json
import subprocess
import os
import boto3


def makeTables(uuid):
    name1 = "wargames"+str(uuid)
    name2 = "simulated-data-wargames"+str(uuid)
    dyn_resource = boto3.resource('dynamodb')

    params1 = {
        'TableName': name1,
        'KeySchema':[
            {'AttributeName' : 'SegID', 'KeyType': 'HASH'}
        ],
        'AttributeDefinitions':[
            {'AttributeName': 'SegID', 'AttributeType':'S'}
        ],
        'ProvisionedThroughput': {
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    }
    table = dyn_resource.create_table(**params1)
    print(f"Creating {name1}...")
    table.wait_until_exists()

    params2 = {
        'TableName': name2,
        'KeySchema':[
            {'AttributeName' : 'SegID', 'KeyType': 'HASH'}
        ],
        'AttributeDefinitions':[
        {'AttributeName' : 'SegID', 'AttributeType': 'S'},
        ],
        'ProvisionedThroughput': {
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    }
    table2 = dyn_resource.create_table(**params2)
    print(f"Creating {name2}...")
    table2.wait_until_exists()

def runSim(uuid):
    config = {
        "Route File": "../Data/Route/WSC/WSC_6000_smoothed_6.csv",
        "Weather File": "../Data/Weather/CA/T35416.csv",
        "Schedule File": "../Data/Schedule/Schedule2015.json",
        "Race Type": "WSC",
        "Car Name": "Electrum2019",
        "Car File": "../Data/Cars/Cars.json",
        "Array File": "../Data/Cars/Electrum2019/Array.json",
        "Battery Name": "I2_race",
        "Battery File": "../Data/Cars/Battery.json",
        "Motor File": "../Data/Motors/Motor_Marand.json",
        "OCV File": "../Data/OCV/I2_ocv.csv",
        "Units": "kph",
        "Battery Units": "Wh",
        "Aux Mode": "Full",
        "Sim Type": 1,
        "Set Speed": 110,
        "Start Time": "2015-10-18 08:30:00",
        "Weather Mult": 1,
        "Start SOC": 100,
        "Min SOC": 2,
        "Start Segment": 0,
        "End Segment": -1,
        "Advanced Tire Model": False,
        "Tire File": "../Data/Tires/4W_MichelinRadialX_95_80_R16.json",
        "TEG File": "../Data/Extra/Teg.json",
        "CdA File": "../Data/Cars/Electrum2019/static_cda.json"
    }

    # Write the output file
    out_file = open("./Simulator_v2/build/simConfig.json", "w")
    json.dump(config, out_file, indent=2)
    out_file.close()

    ########################
    #####   RUN SIM    #####
    ########################

    # change directory, run the simulator with simConfig.json, and then assign the sim a UUID
    os.chdir("./Simulator_v2/build")

    # Run the subprocess and retrieve its errors
    uuid_str = str(uuid)
    return subprocess.call(
        ["./simulator", "simConfig.json", uuid_str], stderr=subprocess.STDOUT)
