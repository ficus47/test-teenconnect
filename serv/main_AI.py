from flask import Flask, request
import tensorflow as tf

from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras import layers

app = Flask()