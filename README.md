# Case Study: Museum Visitors

## Project Description

The Liverpool Museum of Natural History (LMNH) hosts hundreds of thousands of visitors every year, coming to view award-winning exhibitions such as "Fossils of the Ancient Nile" and "Inordinately Fond: Biodiversity in Beetles".

LMNH's core mission is 'to provide value to the Liverpool community and the wider public'. As part of this mission, the museum regularly collects data on visitor satisfaction and wellbeing, which is then used to target exhibition development and maintenance. In the past, the museum has collected this data through written surveys and online reviews, but LMNH has recently secured funding for a new project focused on gathering immediate user feedback. This project is currently being trialled in several key exhibitions.

"Smiley Face Survey Kiosks" have been placed at the exits of the exhibitions; visitors are asked to rate their experience of the exhibition on a five-point scale (from 😡 to 😀). Each kiosk features two other buttons: an "assistance" button, for general enquiries, and an "emergency" button for immediate support.

This repository contains files that enable the extraction of live data recieved from these kiosks and placement of this data into a database.

## Repository Contents

stream_pipeline.py - This script establishes a connection to the kiosks data stream and an RDS instance.
Within this script, data arriving is also cleaned. Erroneous data is removed from the working dataset and logged into the text file erroneous_data.log.
Once the data is cleaned it is filtered as to which type of entry it is and then finally uploaded to the database.

erroneous_data.log - Log of all erroneous data received from the data stream

requirements.txt - file containing all necessary module requirements

schema.sql - sql schema that describes the construction of our database and how data is to be loaded into relevant database

## How to use

- To create or the database where the data will be input, run the bash script reset_database.sh (>>bash reset_database.sh)
- Simply running stream_pipeline.py triggers a connection to the stream that persists until the program is exited.
- To run the program as a background task, run the command (>> nohup python3 stream_pipeline.py &). To stop the process, lookup the PID of the program by entering (ps -ax) and run the command (>>kill -9 PIDnum)

## Environment Variables

The required environment variables in this project are:

- To enable a connection to the RDS:
  DATABASE_NAME,
  DATABASE_USERNAME,
  DATABASE_PASSWORD,
  DATABASE_IP,
  DATABASE_PORT

- To enable a connection to the data stream:
  BOOTSTRAP_SERVERS,
  SECURITY_PROTOCOL,
  SASL_MECHANISM,
  USERNAME,
  PASSWORD,
  GROUP,
  AUTO_OFFSET,
  TOPIC

## Installation

To install required modules for this project, please refer to requirements.txt
