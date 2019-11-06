#!/usr/bin/env python3
import csv
import getopt
import sys

from rocketreach.gateway import Gateway, GatewayConfig
from rocketreach.person import Person


def usage(cmd):
    return '%s -i <inputfile> -o <outputfile> -k <api key>' % cmd


def main(cmd, argv):
    try:
        opts, args = getopt.getopt(argv, 'hi:o:k:e:', ['input=', 'output=', 'key=', 'environment='])
    except getopt.GetoptError:
        print(usage(cmd))
        sys.exit(1)

    input_filename = ''
    output_filename = ''
    api_key = None
    env = 'production'
    for opt, arg in opts:
        if opt == '-h':
            print(usage(cmd))
            sys.exit(0)
        elif opt in ('-i', '--input'):
            input_filename = arg
        elif opt in ('-o', '--output'):
            output_filename = arg
        elif opt in ('-k', '--key'):
            api_key = arg
        elif opt in ('e', '--env'):
            env = arg

    rr_gateway = Gateway(GatewayConfig(api_key, env))
    with open(output_filename, 'w') as csv_output_file:
        csv_writer = csv.writer(csv_output_file)
        with open(input_filename, 'r') as csv_input_file:
            csv_reader = csv.reader(csv_input_file, delimiter=',')
            csv_writer.writerow(next(csv_reader))
            for row in csv_reader:
                name, employer = row[0], row[1]
                result = rr_gateway.person.lookup(extras={'name': name, 'current_employer': employer})
                if result.is_success:
                    person = result.person
                    csv_writer.writerow([
                        name, employer, '', 'found' if person.found else 'not found',
                        person.id, person.first_name, person.last_name,
                        person.emails['current_work'], person.emails['current_personal'],
                        person.emails['other'], person.phones,
                        person.current_title, person.current_employer, person.linkedin_url
                    ])


if __name__ == '__main__':
    main(sys.argv[0], sys.argv[1:])
