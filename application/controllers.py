from flask import Flask, render_template, request, flash, redirect, url_for
from flask import current_app as hospital_app
from .models import *

