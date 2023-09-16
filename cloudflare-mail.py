#!/usr/bin/env python

# Configuration
ZONE_ID = "" # Your Zone ID
EMAIL_ADDRESS = "" # Your Cloudflare E-mail address
GLOBAL_API_KEY = "" # Your Global API Key



import requests, json, time

zone_id = ZONE_ID
header_list = {
    'X-Auth-Email': EMAIL_ADDRESS,
    'X-Auth-Key': GLOBAL_API_KEY,
    'Content-Type': 'application/json',
}

print('Welcome to Cloudflare simple e-mail routing rules manager')
print('Made by https://netman.ovh - 2023')

def list_rules():
    request = requests.get(f"https://api.cloudflare.com/client/v4/zones/{zone_id}/email/routing/rules", headers=header_list)
    if (request.status_code == "200" or request.status_code == 200):
        results = request.json()['result']
        rules = []
        if request.json()['success']:
            for result in results:
                if result["matchers"][0]["type"] != "all":
                    result_type = "normal"
                    result_get_email = f"get: {result['matchers'][0]['value']}"

                    if result['actions'][0]['type'] != "drop":
                        result_action = f"{result['actions'][0]['type']}: {result['actions'][0]['value'][0]}"
                    else:
                        result_action = "drop"
                    
                    if result['enabled']:
                        result_enabled = "enabled"
                    else:
                        result_enabled = "disabled"

                    if result['name'] == "":
                        result_name = "Unknown"
                    else:
                        result_name = result['name']

                    rules.append([
                        result_name,
                        result_type,
                        result_get_email,
                        result_action,
                        result_enabled,
                        result['tag'],
                    ])
        else:
            return ConnectionError, ConnectionError
        format = ["Name", "Type", "Catch", "Action", "Enabled"]
        end_result = ""
        iterate = 0
        for rule in rules:
            iterate += 1
            end_result += f"{iterate}) "
            for i in range(5):
                comma = ","
                if i == 4:
                    comma = ""
                end_result += f"{format[i]}: {rule[i]}{comma} "
            if iterate != len(rules):
                end_result += "\n"
        rule_ids = []
        for rule_id in rules:
            rule_ids.append(rule_id[5])
        return end_result, rule_ids
    else:
        return ConnectionError, ConnectionError

def programme():
    print('What would you like to do?' + "\n"
          + '1) List all e-mail routing rules' + "\n"
          + '2) Create a new e-mail routing rule' + "\n"
          + '3) Update an existing e-mail routing rule' + "\n"
          + '4) Delete an e-mail routing rule' + "\n"
          + '5) Get the e-mail catch-all rule' + "\n"
          + '6) Update the e-mail catch-all rule' + "\n"
          + '7) Exit this program')
    option = input('Select your option: ')
    try:
        match int(option):
            case 1:
                print('Listing all rules:')
                list_rule = list_rules()
                if list_rule[0] != ConnectionError:
                    print(list_rule[0])
                else:
                    print('Error, try again')
                input("Press Enter to continue... ")
                programme()
            case 2:
                def action():
                    print('Choose action:' + "\n"
                        + '1) Drop' + "\n"
                        + '2) Send to an e-mail' + "\n"
                        + '3) Send to a worker (does nothing for now)' + "\n"
                        + '4) Go back to the main menu')
                    action_option = input('Select your option: ')
                    try:
                        match int(action_option):
                            case 1:
                                drop_mail = input("Which e-mail would you like to drop mails from?\nHere: ")
                                
                                json_data = '''{
                                "actions": [
                                    {
                                    "type": "drop"
                                    }
                                ],
                                "enabled": true,
                                "matchers": [
                                    {
                                    "field": "to",
                                    "type": "literal",
                                    "value": "%s"
                                    }
                                ],
                                "name": "Drop %s",
                                "priority": 0
                                }''' % (drop_mail, drop_mail)

                                json_data_object = json.loads(json_data)

                                request = requests.post(f"https://api.cloudflare.com/client/v4/zones/{zone_id}/email/routing/rules",
                                                        headers=header_list, json=json_data_object)
                                if (request.status_code == "200" or request.status_code == 200):
                                    if request.json()['success']:
                                        print('Done!')
                                    else:
                                        print('Error, try again')
                                else:
                                    print('Error, try again')
                                input("Press Enter to continue... ")
                                programme()
                            case 2:
                                fwd_mail = input("Which e-mail would you like to forward mails FROM?\nHere: ")
                                dest_mail = input("Which e-mail would you like to forward mails TO?\nHere: ")
                                json_data = '''{
                                "actions": [
                                    {
                                    "type": "forward",
                                    "value": [
                                        "%s"
                                    ]
                                    }
                                ],
                                "enabled": true,
                                "matchers": [
                                    {
                                    "field": "to",
                                    "type": "literal",
                                    "value": "%s"
                                    }
                                ],
                                "name": "Fwd %s to %s",
                                "priority": 0
                                }''' % (dest_mail, fwd_mail, fwd_mail, dest_mail)
                                json_data_object = json.loads(json_data)
                                request = requests.post(f"https://api.cloudflare.com/client/v4/zones/{zone_id}/email/routing/rules",
                                                        headers=header_list, json=json_data_object)
                                if (request.status_code == "200" or request.status_code == 200):
                                    if request.json()['success']:
                                        print('Done!')
                                    else:
                                        print('Error, try again')
                                else:
                                    print('Error, try again')
                                input("Press Enter to continue... ")
                                programme()
                            case 3:
                                print('3')
                                input("Press Enter to continue... ")
                                programme()
                            case 4:
                                input("Press Enter to continue... ")
                                programme()
                            case _:
                                print('Incorrect option, try again')
                                input("Press Enter to continue... ")
                                action()
                    except ValueError:
                        print('Incorrect option, try again')
                        input("Press Enter to continue... ")
                        action()
                action()
            case 3:
                print('TO-DO: Update e-mail rules')
                # To-Do
                input("Press Enter to continue... ")
                programme()
            case 4:
                print('Which rule would you like to delete?')
                list_rule = list_rules()
                if list_rule[0] != ConnectionError:
                    def rule_del():
                        print(list_rule[0])
                        print(f"{len(list_rule[1])+1}) Go back to the main menu")
                        rule_del_option = input('Select your option: ')
                        try:
                            if (int(rule_del_option) == len(list_rule[1])+1):
                                programme()
                            elif (int(rule_del_option) > 0 and int(rule_del_option) < len(list_rule[1])+1):
                                request = requests.delete(f"https://api.cloudflare.com/client/v4/zones/{zone_id}/email/routing/rules/{list_rule[1][int(rule_del_option)-1]}",
                                                        headers=header_list)
                                if (request.status_code == "200" or request.status_code == 200):
                                    if request.json()['success']:
                                        print('Done!')
                                    else:
                                        print('Error, try again')
                                else:
                                    print('Error, try again')
                                input("Press Enter to continue... ")
                                programme()
                            else:
                                print("Incorrect option, try again")
                                input("Press Enter to continue... ")
                                rule_del()
                        except ValueError:
                            print('Incorrect option, try again')
                            input("Press Enter to continue... ")
                            rule_del()
                    rule_del()
                else:
                    print('Error, try again')
                input("Press Enter to continue..." )
                programme()
            case 5:
                print('Getting the catch-all rule')
                request = requests.get(f"https://api.cloudflare.com/client/v4/zones/{zone_id}/email/routing/rules/catch_all", headers=header_list)
                result = request.json()['result']
                if (request.status_code == "200" or request.status_code == 200):
                    if request.json()['success']:
                        if result['actions'][0]['type'] != "drop":
                            result_action = f"{result['actions'][0]['type']}: {result['actions'][0]['value'][0]}"
                        else:
                            result_action = "drop"
                                
                        if result['enabled']:
                            result_enabled = "enabled"
                        else:
                            result_enabled = "disabled"

                        print(f'Catch-all rule: Action: {result_action}, Enabled: {result_enabled}')
                        print('Done!')

                    else:
                        print('Error, try again')
                else:
                    print('Error, try again')
                input("Press Enter to continue... ")
                programme()
            case 6:
                print('TO-DO: Update catch-all e-mail rule')
                # To-Do
                input("Press Enter to continue... ")
                programme()
            case 7:
                print('Exiting...')
                exit()
            case _:
                print('Incorrect option, try again.')
                input("Press Enter to continue... ")
                programme()
    except ValueError:
        print('Incorrect option, try again')
        input("Press Enter to continue... ")
        programme()

programme()
