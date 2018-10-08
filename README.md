# celstash
Celery logging to logstash and structured log (JSON) file

Please submit bugs [here](https://github.com/CyberInt/celstash/issues).

# Usage

    import celstash
    import logging

    celstash.configure(logstash_host='logstash', logstash_port=9999)
    logger = celstash.new_logger('worker1')
    logger.setLevel(logging.INFO)
    logger.info('Money is the root of all evil, and man needs roots.')


# logstash setup

    input {
        udp {
            codec => json
            'port' => "9999"
        }
    }
    output {
        elasticsearch {
            host => localhost  # Change to your host
        }
    }

# License
MIT, see [LICENSE.txt](LICENSE.txt)
