## Setup

- Install Docker or Docker Desktop
- Create Standalone Device on your site in Enapter Cloud
- Generate config for your Standalone device
- Copy it to `env.txt` file as `ENAPTER_VUCM_BLOB` value
- Verify that your LabVIEW program sends data as JSON over TCP connection. Only one message per connection is allowed.
- Take number of TCP port, to which  data is being sent from LabVIEW and set it to `LISTEN_TCP_PORT` variable in `env.list`.

## Run
- Copy `*_run.sh` script to directory with `env.txt`
- Open Terminal in Docker Desktop. Change working directory to the same as in previous step.
-  `./*_run.sh`


## Development
1. Run `*_build.sh`
2. `docker push  ...`
2. Notify colleagues to pull the latest image 