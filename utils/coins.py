import requests
import discord


async def add_points(message, user, server, points, api_key, print_success = False, print_error = False):
    params = {'user_id':user,'server_id':server,'amount':points}
    headers = {'accept':'application/json','X-API-KEY':api_key}
    url = 'https://discordhub.com/api/points/add'
    r = requests.post(url, params=params, headers=headers)
    if r.status_code == 200:
        if print_success:
            await message.channel.send('Successful: Gave <@{}> {} points'.format(user, points))
            return True
        else:
            print("|> Gave {} - {} bonus points".format(user, points))
            return True
    else:
        if print_error:
            await message.channel.send('Unsuccessful: attempting to manually award the {} points'.format(points))
            return False
        else:
            print(params)
            print(r.url)
            print(r.status_code)
            return False




async def remove_points(message, user, server, points, api_key, print_success = False, print_error = False):
    params = {'user_id':user,'server_id':server,'amount':points}
    headers = {'accept':'application/json','X-API-KEY':api_key}
    url = 'https://discordhub.com/api/points/remove'
    r = requests.post(url, params=params, headers=headers)
    if r.status_code == 200:
        if print_success:
            await message.channel.send('Successful: Removed {} points from  <@{}>'.format(points, user))
            return True
        else:
            print("|> Gave {} - {} bonus points".format(user, points))
            return True
    else:
        if print_error:
            await message.channel.send('Unsuccessful: attempting to manually award the {} points'.format(points))
            return False
        else:
            print(params)
            print(r.url)
            print(r.status_code)
            return False



def check_points():
    pass
