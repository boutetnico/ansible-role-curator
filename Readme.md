[![tests](https://github.com/boutetnico/ansible-role-curator/workflows/Test%20ansible%20role/badge.svg)](https://github.com/boutetnico/ansible-role-curator/actions?query=workflow%3A%22Test+ansible+role%22)
[![Ansible Galaxy](https://img.shields.io/badge/galaxy-boutetnico.curator-blue.svg)](https://galaxy.ansible.com/boutetnico/curator)

ansible-role-curator
====================

This role installs and configures [Curator](https://github.com/elastic/curator).

Requirements
------------

Ansible 2.10 or newer.

Supported Platforms
-------------------

- [Debian - 11 (Bullseye)](https://wiki.debian.org/DebianBullseye)
- [Debian - 12 (Bookworm)](https://wiki.debian.org/DebianBookworm)
- [Ubuntu - 22.04 (Jammy Jellyfish)](http://releases.ubuntu.com/22.04/)
- [Ubuntu - 24.04 (Noble Numbat)](http://releases.ubuntu.com/24.04/)

Role Variables
--------------

| Variable                | Required | Default                    | Choices   | Comments                                     |
|-------------------------|----------|----------------------------|-----------|----------------------------------------------|
| curator_package         | true     | `elasticsearch-curator`    | string    |                                              |
| curator_package_version | true     | `8.0.15`                   | string    |                                              |
| curator_hosts           | true     | `[http://127.0.0.1:9200]`  | list      |                                              |
| curator_cloud_id        | true     |                            | string    |                                              |
| curator_ca_certs        | true     |                            | string    |                                              |
| curator_client_cert     | true     |                            | string    |                                              |
| curator_client_key      | true     |                            | string    |                                              |
| curator_verify_certs    | true     | `true`                     | bool      |                                              |
| curator_request_timeout | true     | `30`                       | int       |                                              |
| curator_master_only     | true     | `false`                    | bool      |                                              |
| curator_username        | true     |                            | string    | Username for basic auth.                     |
| curator_password        | true     |                            | string    | Password for basic auth.                     |
| curator_api_key         | true     |                            | string    |                                              |
| curator_api_key_id      | true     |                            | string    |                                              |
| curator_api_key_api_key | true     |                            | string    |                                              |
| curator_api_key_token   | true     |                            | string    |                                              |
| curator_log_file        | true     |                            | string    | Absolute file path or empty string (stdout). |
| curator_log_level       | true     | `INFO`                     | string    |                                              |
| curator_log_format      | true     | `default`                  | string    |                                              |
| curator_log_blacklist   | true     | `[elasticsearch, urllib3]` | list      |                                              |
| curator_config_path     | true     | `/etc/curator`             | string    |                                              |
| curator_systemd_config  | true     | `{}`                       | dict      |                                              |
| curator_actions         | true     | `actions: {}`              | dict      | Actions to perform. See `defaults/main.yml`. |

Dependencies
------------

None

Example Playbook
----------------

    - hosts: all
      roles:
        - role: ansible-role-curator
          curator_actions:
            actions:
              1:
                action: snapshot
                description: >-
                  Snapshot filebeat- prefixed indices older than 1 day and younger
                  than 15 days (based on index creation_date) with the default
                  snapshot name pattern of 'curator-%Y%m%d%H%M%S'.
                  Wait for the snapshot to complete.  Do not skip the repository
                  filesystem access check.  Use the other options to create the snapshot.
                options:
                  repository: my_backup
                  # Leaving name blank will result in the default 'curator-%Y%m%d%H%M%S'
                  name:
                  ignore_unavailable: false
                  include_global_state: true
                  partial: false
                  wait_for_completion: true
                  skip_repo_fs_check: false
                filters:
                  - filtertype: pattern
                    kind: prefix
                    value: filebeat-
                  - filtertype: age
                    source: creation_date
                    direction: older
                    unit: days
                    unit_count: 1
                  - filtertype: age
                    source: creation_date
                    direction: younger
                    unit: days
                    unit_count: 15
              2:
                action: delete_snapshots
                description: >-
                  Delete snapshots from the selected repository older than 7 days
                  (based on creation_date), for 'curator-' prefixed snapshots.
                options:
                  repository: my_backup
                  ignore_empty_list: true
                filters:
                  - filtertype: pattern
                    kind: prefix
                    value: curator-
                    exclude:
                  - filtertype: age
                    source: creation_date
                    direction: older
                    unit: days
                    unit_count: 7
              3:
                action: close
                description: >-
                  Close indices older than 30 days (based on index name), for filebeat-
                  prefixed indices.
                options:
                  delete_aliases: false
                  ignore_empty_list: true
                filters:
                  - filtertype: pattern
                    kind: prefix
                    value: filebeat-
                  - filtertype: age
                    source: name
                    direction: older
                    timestring: '%Y.%m.%d'
                    unit: days
                    unit_count: 30
              4:
                action: delete_indices
                description: >-
                  Delete indices older than 60 days (based on index name), for filebeat-
                  prefixed indices. Ignore the error if the filter does not result in an
                  actionable list of indices (ignore_empty_list) and exit cleanly.
                options:
                  ignore_empty_list: true
                filters:
                  - filtertype: pattern
                    kind: prefix
                    value: filebeat-
                  - filtertype: age
                    source: name
                    direction: older
                    timestring: '%Y.%m.%d'
                    unit: days
                    unit_count: 60

Testing
-------

    molecule test

License
-------

MIT

Author Information
------------------

[@boutetnico](https://github.com/boutetnico)
