from flask import Flask, request, abort, Response, send_file
import os
import requests
import json
import sys
from datetime import datetime, timedelta
from base64 import b64encode
import csv
from dateutil.parser import parse as parse_date

# Verificação de variáveis de ambiente obrigatórias
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
MERCADOPAGO_TOKEN = os.getenv("MERCADOPAGO_TOKEN")
STATUS_USERNAME = "ElitePlay"
STATUS_PASSWORD = "Camisa1@@"
...
