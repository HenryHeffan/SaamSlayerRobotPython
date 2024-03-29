import pandas as pd
import tensorflow as tf
from data_loader import load_dataset

TRAIN_URL = "http://download.tensorflow.org/data/iris_training.csv"
TEST_URL = "http://download.tensorflow.org/data/iris_test.csv"

CSV_COLUMN_NAMES = ['SepalLength', 'SepalWidth',
					'PetalLength', 'PetalWidth', 'Species']
SPECIES = ['Setosa', 'Versicolor', 'Virginica']

def load_data(y_name='Species'):
	"""Returns the iris dataset as (train_x, train_y), (test_x, test_y)."""
	path_train  = "/home/henry/workspace/SSE3/neural_chesspiece/data/"
	dataset = load_dataset(path_train,one_hot=False)

	return dataset


def train_input_fn(dataset, batch_size):
	"""An input function for training"""
	# Convert the inputs to a Dataset.
	dataset = tf.data.Dataset.from_tensor_slices(({"x":dataset[0]},dataset[1]))

	# Shuffle, repeat, and batch the examples.
	dataset = dataset.shuffle(100).repeat().batch(batch_size)

	print( dataset)

	# Return the dataset.
	return dataset


def eval_input_fn(dataset, batch_size):
	"""An input function for evaluation or prediction"""
	# features=dict(features)
	# if labels is None:
	# 	# No labels, use only features.
	# 	inputs = features
	# else:
	# 	inputs = (features, labels)

	# # Convert the inputs to a Dataset.
	# dataset = tf.data.Dataset.from_tensor_slices(inputs)

	dataset = tf.data.Dataset.from_tensor_slices(({"x":dataset[0]},dataset[1]))
	# Batch the examples
	assert batch_size is not None, "batch_size must not be None"
	dataset = dataset.batch(batch_size)

	# Return the dataset.
	return dataset


# The remainder of this file contains a simple example of a csv parser,
#     implemented using a the `Dataset` class.

# `tf.parse_csv` sets the types of the outputs to match the examples given in
#     the `record_defaults` argument.
CSV_TYPES = [[0.0], [0.0], [0.0], [0.0], [0]]

def _parse_line(line):
	# Decode the line into its fields
	fields = tf.decode_csv(line, record_defaults=CSV_TYPES)

	# Pack the result into a dictionary
	features = dict(zip(CSV_COLUMN_NAMES, fields))

	# Separate the label from the features
	label = features.pop('Species')

	return features, label


def csv_input_fn(csv_path, batch_size):
	# Create a dataset containing the text lines.
	dataset = tf.data.TextLineDataset(csv_path).skip(1)

	# Parse each line.
	dataset = dataset.map(_parse_line)

	# Shuffle, repeat, and batch the examples.
	dataset = dataset.shuffle(1000).repeat().batch(batch_size)

	# Return the dataset.
	return dataset
