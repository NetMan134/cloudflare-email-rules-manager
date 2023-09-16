# Cloudflare e-mail rules manager
A simple Cloudflare e-mail routing rules manager script written in Python (made it because I didn't want to visit cloudflare.com each time to add/delete a rule), it can:
- List all rules
- Create new rules
- Delete existing rules

## Config
You have to prepare your:
- Global Cloudflare API key [here](https://dash.cloudflare.com/profile/api-tokens)<br>
- Zone ID (visit Cloudflare, choose your domain for managment, and on its overview page it'll be under the API tab/tile)
- Your e-mail address used for Cloudflare login
<br>
<strong>Also make sure E-mail routing is already enabled, and the Zone ID is equivalent to the domain you want to change e-mail rules for</strong><br><br>
Then, in the cloudflare-mail.py add your secrets, run "pip install -r requirements.txt" to download the necessary "requests" library, and run the code! (python cloudflare-mail.py)

## Info
If you create/update a rule and provide a destination address not used before, you need to go to the Cloudflare website, E-mail routing, and manually verify the destination address - otherwise Cloudflare displays "Destination address not found" in the E-mail routing > Custom addresses tile > Status column. Just click Edit on an affected rule, click on the destination address input, and choose it from the list again, then save - and on the destination e-mail you'll receive a message with a link, click it, and it'll be alright :)

## To-Do:
- [ ] Updating rules (catch-all and other, enabling, changing destination address)
- [ ] Better way of storing secrets

## License
This project is licensed under [The Unlicense](https://choosealicense.com/licenses/unlicense/)
