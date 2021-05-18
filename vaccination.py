import json
import time
import ssl
import sys

from datetime import datetime
from urllib.request import urlopen
from urllib.request import Request

HDRS = {
  "accept": "application/json",
  "Accept-Language": "hi_IN",
  "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
}

def make_request(url, headers):
  ctx = ssl.create_default_context()
  ctx.check_hostname = False
  ctx.verify_mode = ssl.CERT_NONE
  req = Request(url=url, headers=headers)
  with urlopen(req, context=ctx) as resp:
    return json.loads(resp.read().decode('utf-8'))

def get_state_ids():
  STATES_URL = "https://cdn-api.co-vin.in/api/v2/admin/location/states"
  return [state["state_id"] for state in make_request(STATES_URL, HDRS)["states"]]

# get_state_ids()

def get_district_ids_for_state(state_id):
  DISTRICTS_URL_PREFIX = "https://cdn-api.co-vin.in/api/v2/admin/location/districts/{}"
  url = DISTRICTS_URL_PREFIX.format(state_id)
  return [district["district_id"] for district in make_request(url, HDRS)["districts"]]

def get_appt_locs_for_state_id(district_ids=[265, 276, 294], age=45, min_slots=0):
  APPT_URL_PATTERN = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}"
  today = datetime.now().strftime("%d-%m-%Y")

  if age is None:
    age = 45
  for district_id in district_ids:
    for center in make_request(APPT_URL_PATTERN.format(district_id, today), HDRS)["centers"]:
      for session in center["sessions"]:
        if session["min_age_limit"] <= age and session["available_capacity"] >= min_slots:
          print("Vaccine: {} available at {} in {}, {} with pincode {} on {} and {} slots are free. It is a {} slot".format(session["vaccine"], center["name"], center["district_name"], center["state_name"], center["pincode"], session["date"], session["available_capacity"], center["fee_type"]))

  # while True:
  #     get_appt_locs_for_state_id(state_id, 18)
  #     sys.stdout.flush()
  #     time.sleep(60)

if __name__ == '__main__':
  min_slots = int(sys.argv[2]) if len(sys.argv) > 2 else 0
  get_appt_locs_for_state_id(age=18, min_slots=min_slots)