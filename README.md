[![banner](https://raw.githubusercontent.com/nevermined-io/assets/main/images/logo/banner_logo.png)](https://nevermined.io)


# Nevermined Metadata Driver Filecoin

> Nevermined Driver allowing to connect to Filecoin as storage backend
> [nevermined.io](https://nevermined.io/)


[![PyPI](https://img.shields.io/pypi/v/nevermined-metadata-driver-filecoin.svg)](https://pypi.org/project/nevermined-metadata-driver-filecoin/)
[![Python package](https://github.com/nevermined-io/metadata-driver-filecoin/workflows/Python%20package/badge.svg)](https://github.com/nevermined-io/metadata-driver-filecoin/actions)


# metadata-driver-filecoin

Nevermined Driver allowing to connect to Filecoin as storage backend


## Testing

The following instructions assume you have installed [PowerGate CLI](https://docs.filecoin.io/build/powergate/). For more information visit the following page.
The PowerGate CLI needs to be connected to a testnet or mainnet.

```bash
## First we create a user
$ pow admin user create

$ export POW_TOKEN=583561b2-2ea5-421c-b926-e5d8538a38c8

$ pow data stage andromeda_galaxy_2-wallpaper-1920x1080.jpg 

{
  "cid": "QmW68jbcqSRtqSQb6xkukQ6tfonZGhu1VrZv9zAicNmovs"
}

$ pow config apply --watch QmW68jbcqSRtqSQb6xkukQ6tfonZGhu1VrZv9zAicNmovs

{
  "jobId": "eb33d324-2a0c-4624-b1a7-e083e20af827"
}
                 JOB ID                |       STATUS       | MINER  | PRICE  |    DEAL STATUS     
---------------------------------------+--------------------+--------+--------+--------------------
  eb33d324-2a0c-4624-b1a7-e083e20af827 | JOB_STATUS_SUCCESS |        |        |                    
                                       |                    | f01000 | 122070 | StorageDealActive  


$ pow data info QmW68jbcqSRtqSQb6xkukQ6tfonZGhu1VrZv9zAicNmovs

{
  "cidInfo": {
    "cid": "QmW68jbcqSRtqSQb6xkukQ6tfonZGhu1VrZv9zAicNmovs",
    "latestPushedStorageConfig": {
      "hot": {
        "enabled": true,
        "allowUnfreeze": false,
        "unfreezeMaxPrice": "0",
        "ipfs": {
          "addTimeout": "10"
        }
      },
      "cold": {
        "enabled": true,
        "filecoin": {
          "replicationFactor": "1",
          "dealMinDuration": "518400",
          "excludedMiners": [],
          "trustedMiners": [],
          "countryCodes": [],
          "renew": {
            "enabled": false,
            "threshold": "0"
          },
          "address": "f3sfmoqwikzcadyv2px5jkfp67alb265tcengexvdry3p5xvvgnpxfjqdqwyvmmhjs5d5aswdfsqwva6ats73q",
          "maxPrice": "0",
          "fastRetrieval": false,
          "dealStartOffset": "0",
          "verifiedDeal": false
        }
      },
      "repairable": false
    },
    "currentStorageInfo": {
      "jobId": "eb33d324-2a0c-4624-b1a7-e083e20af827",
      "cid": "QmW68jbcqSRtqSQb6xkukQ6tfonZGhu1VrZv9zAicNmovs",
      "created": "1616166426745925860",
      "hot": {
        "enabled": true,
        "size": "235411",
        "ipfs": {
          "created": "1616166354290043653"
        }
      },
      "cold": {
        "enabled": true,
        "filecoin": {
          "dataCid": "QmW68jbcqSRtqSQb6xkukQ6tfonZGhu1VrZv9zAicNmovs",
          "size": "262144",
          "proposals": [
            {
              "dealId": "2",
              "renewed": false,
              "duration": "521756",
              "startEpoch": "11702",
              "miner": "f01000",
              "epochPrice": "122070",
              "pieceCid": "baga6ea4seaqbddfgypcg46c6etayudbn2l2e333j5pgxou7ka27oustlfkatefq"
            }
          ]
        }
      }
    },
    "queuedStorageJobs": [],
    "executingStorageJob": null
  }
}


$ pow data get QmW68jbcqSRtqSQb6xkukQ6tfonZGhu1VrZv9zAicNmovs /tmp/image.jpg
> Success! Data written to /tmp/image.jpg



```

Automatic tests are setup via Github actions.
Our tests use the pytest framework.


## New Version

The `bumpversion.sh` script helps to bump the project version. You can execute
the script using as first argument {major|minor|patch} to bump accordingly the version.


## License

```text
Copyright 2020 Keyko GmbH

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```
