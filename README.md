# celstash
Celery logging to logstash and sturctured log (JSON) file

Please submit bugs [here](https://github.com/CyberInt/celstash/issues).

# Usage

    import celstash
    import logging

    logger = celstash.new_logger('worker1', logstash_host='example.com')
    logger.setLevel(logging.INFO)
    logger.info('Money is the root of all evil, and man needs roots.')


# logstash setup

    input {
        udp {
            codec => json
        }
    }
    output {
        elasticsearch {
            host => localhost  # Change to your host
        }
    }

# License
MIT, see [LICENSE.txt](LICENSE.txt)
